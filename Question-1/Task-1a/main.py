"""
Question 1:
Write a Python script to extract all feeds from the URL below:

URL: https://www.cbn.gov.ng/Documents/circulars.html
"""

"""
Task 1a:
Fetch CBN circular items from the API endpoint and save them as JSON.
"""

from __future__ import annotations

import json
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://www.cbn.gov.ng/api/GetAllCirculars?format=json"
OUTPUT_FILE = Path(__file__).with_name("cbn_circulars.json")


def fetch_circulars(api_url: str) -> list[dict]:
    """Fetch circular records from CBN API."""
    request = Request(
        api_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    context = ssl._create_unverified_context()
    with urlopen(request, timeout=60, context=context) as response:
        payload = response.read().decode("utf-8")

    data = json.loads(payload)
    if not isinstance(data, list):
        raise ValueError("Unexpected API response: expected a JSON list.")

    normalized: list[dict] = []
    for item in data:
        if isinstance(item, dict):
            normalized.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "refNo": item.get("refNo"),
                    "author": item.get("author"),
                    "documentDate": item.get("documentDate"),
                    "description": item.get("description"),
                    "link": item.get("link"),
                    "filesize": item.get("filesize"),
                    "keywords": item.get("keywords"),
                    "clickCount": item.get("clickCount"),
                }
            )

    return normalized


def save_to_json(records: list[dict], output_path: Path) -> None:
    """Write records to disk as pretty JSON."""
    output_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    try:
        circulars = fetch_circulars(API_URL)
        save_to_json(circulars, OUTPUT_FILE)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as error:
        print(f"Failed to fetch circulars: {error}")
        return

    print(f"Saved {len(circulars)} circular items to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
