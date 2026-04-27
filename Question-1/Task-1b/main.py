"""
Question 1 Task 1b:
Download all linked PDF files, save them into a sub-directory, rename files
to remove spaces, and include the local file path in updated JSON records.
"""

from __future__ import annotations

import json
import re
import ssl
import argparse
import random
import time
from pathlib import Path
from typing import Any
from http.client import InvalidURL
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse, unquote, urlunparse
from urllib.request import Request, urlopen


BASE_URL = "https://www.cbn.gov.ng"
INPUT_JSON = Path(__file__).resolve().parent.parent / "Task-1a" / "cbn_circulars.json"
OUTPUT_JSON = Path(__file__).resolve().parent / "cbn_circulars_with_pdfs.json"
PDF_DIR = Path(__file__).resolve().parent / "downloaded_pdfs"


def load_records(path: Path) -> list[dict[str, Any]]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Input JSON must be a list of records.")
    return [record for record in records if isinstance(record, dict)]


def sanitize_filename(value: str) -> str:
    # Remove spaces.
    cleaned = re.sub(r"\s+", "", value)
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", cleaned)
    return cleaned or "file.pdf"


def candidate_filename(record: dict[str, Any], pdf_url: str, used_names: set[str]) -> str:
    link = str(record.get("link") or "")
    parsed_name = unquote(Path(urlparse(pdf_url).path).name)
    raw_name = parsed_name or unquote(Path(link).name) or f"circular_{record.get('id', 'unknown')}.pdf"

    if not raw_name.lower().endswith(".pdf"):
        raw_name = f"{raw_name}.pdf"

    base = sanitize_filename(raw_name[:-4]) or f"circular_{record.get('id', 'unknown')}"
    ext = ".pdf"
    final_name = f"{base}{ext}"
    counter = 1
    while final_name in used_names:
        final_name = f"{base}_{counter}{ext}"
        counter += 1

    used_names.add(final_name)
    return final_name


def normalize_pdf_url(link: str) -> str:
    raw = link if link.lower().startswith("http") else urljoin(BASE_URL, link)
    parsed = urlparse(raw)
    encoded_path = quote(unquote(parsed.path), safe="/-._~")
    encoded_query = quote(unquote(parsed.query), safe="=&-._~")
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            encoded_path,
            parsed.params,
            encoded_query,
            parsed.fragment,
        )
    )


def download_pdf(
    pdf_url: str,
    destination: Path,
    timeout_seconds: int,
    retries: int,
    backoff_seconds: float,
) -> tuple[bool, str | None]:
    request = Request(
        pdf_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/pdf,*/*;q=0.8",
            "Referer": "https://www.cbn.gov.ng/Documents/circulars.html",
            "Connection": "keep-alive",
        },
    )

    context = ssl._create_unverified_context()
    attempts = max(1, retries + 1)
    last_error: str | None = None

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=timeout_seconds, context=context) as response:
                data = response.read()
                if not data:
                    last_error = "empty_response"
                else:
                    destination.write_bytes(data)
                    return True, None
        except HTTPError as error:
            last_error = f"http_{error.code}"
        except (URLError, TimeoutError, InvalidURL) as error:
            last_error = type(error).__name__.lower()

        if attempt < attempts:
            delay = backoff_seconds * (2 ** (attempt - 1))
            delay += random.uniform(0, 0.5)  # small jitter to avoid burst retries
            time.sleep(delay)

    return False, (last_error or "unknown_error")


def process_records(
    records: list[dict[str, Any]],
    pdf_dir: Path,
    timeout_seconds: int,
    retries: int,
    backoff_seconds: float,
    max_records: int | None,
) -> list[dict[str, Any]]:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    used_names: set[str] = set()
    output: list[dict[str, Any]] = []

    selected_records = records if max_records is None else records[:max_records]

    for index, record in enumerate(selected_records, start=1):
        updated = dict(record)
        link = str(updated.get("link") or "").strip()

        if not link:
            updated["source_pdf_url"] = None
            updated["local_pdf_path"] = None
            updated["download_status"] = "skipped_no_link"
            updated["download_error"] = None
            output.append(updated)
            continue

        pdf_url = normalize_pdf_url(link)
        filename = candidate_filename(updated, pdf_url, used_names)
        destination = pdf_dir / filename

        if destination.exists():
            success = destination.stat().st_size > 0
            error_message = None if success else "existing_file_empty"
        else:
            success, error_message = download_pdf(
                pdf_url=pdf_url,
                destination=destination,
                timeout_seconds=timeout_seconds,
                retries=retries,
                backoff_seconds=backoff_seconds,
            )

        updated["source_pdf_url"] = pdf_url
        updated["local_pdf_path"] = str(destination) if success else None
        updated["download_status"] = "downloaded" if success else "failed"
        updated["download_error"] = None if success else error_message
        output.append(updated)

        if index % 25 == 0:
            print(f"Processed {index}/{len(selected_records)} records...", flush=True)

    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Download CBN circular PDFs and update JSON records.")
    parser.add_argument("--max-records", type=int, default=None, help="Optional max number of records to process.")
    parser.add_argument("--timeout", type=int, default=20, help="Timeout (seconds) for each file download.")
    parser.add_argument("--retries", type=int, default=3, help="Retries per file after initial attempt.")
    parser.add_argument("--backoff", type=float, default=1.5, help="Base seconds for exponential backoff.")
    args = parser.parse_args()

    try:
        records = load_records(INPUT_JSON)
    except Exception as error:
        print(f"Unable to load input JSON: {error}")
        return

    updated_records = process_records(
        records=records,
        pdf_dir=PDF_DIR,
        timeout_seconds=args.timeout,
        retries=args.retries,
        backoff_seconds=args.backoff,
        max_records=args.max_records,
    )
    OUTPUT_JSON.write_text(
        json.dumps(updated_records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    downloaded = sum(1 for item in updated_records if item.get("download_status") == "downloaded")
    failed = sum(1 for item in updated_records if item.get("download_status") == "failed")
    skipped = sum(1 for item in updated_records if item.get("download_status") == "skipped_no_link")

    print(f"Saved updated records to: {OUTPUT_JSON}")
    print(f"PDF directory: {PDF_DIR}")
    print(f"Downloaded: {downloaded} | Failed: {failed} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
