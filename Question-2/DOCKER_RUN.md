# Odoo + Docker (Question 2)

## 1) Start containers
From `Question-2` directory:

```bash
docker compose up -d
```

## 2) Open Odoo
- URL: `http://localhost:8069`
- Master password: `admin` (default Odoo UI prompt)
- Database name: `school_mgmt_db`
- Email/password: any admin credentials you choose in the setup form

## 3) Install your module
In Odoo UI:
1. Go to **Apps**
2. Search for `School Management` (or `school_mgmt`)
3. Click **Install**

If the app does not appear:
1. Turn on developer mode
2. Apps -> **Update Apps List**
3. Search again and install

## 4) Upgrade after code changes
```bash
docker compose exec odoo odoo -d school_mgmt_db -u school_mgmt --stop-after-init
```

Then refresh browser.

## 5) Stop containers
```bash
docker compose down
```

To remove DB data too:
```bash
docker compose down -v
```
