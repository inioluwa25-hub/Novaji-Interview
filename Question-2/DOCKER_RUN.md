# school_mgmt Quick Test Guide

## 1) Start runtime
```bash
brew install docker docker-compose colima qemu
colima start
cd "/Users/mac/Documents/Novaji Interview/Question-2"
docker compose up -d
```

## 2) Open Odoo
- URL: `http://localhost:8069`
- Create database: `school_mgmt_db`

## 3) Install module
- In Odoo: **Apps** -> (Update Apps List if needed) -> search `School Management` -> **Install**

## 4) Verify tasks 2a-2e
1. Open **School -> Students**
2. Create student (required field: `name`)
3. Open the student form
4. Click **Deactivate Student**
5. Confirm `active` becomes `False`
6. Confirm `age` field is hidden on form

## 5) Upgrade after edits
```bash
docker compose exec odoo odoo -d school_mgmt_db -u school_mgmt --stop-after-init
```

## 6) Stop runtime
```bash
docker compose down
```
