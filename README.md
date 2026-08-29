# Odoo Bookstore (custom addons)

Custom Odoo **19** modules and a small **dev kit** so others can run them.

This repo is **not** the full Odoo framework. Think Laravel: this is your `app/` + packages, not the framework core or `.env` secrets.

| In this repo | Not in this repo |
|--------------|------------------|
| `estate/` (learning module) | Odoo core (`odoo/odoo`) |
| future `bookstore/` | Python venv |
| Docker + example configs | Real passwords / production `.env` |

## Quick start (Docker — easiest clone → run)

Needs: Docker + `docker-compose` (v1 or v2).

```bash
git clone git@github.com:ittehad2001/odoo-bookstore.git
cd odoo-bookstore

cp .env.example .env
cp config/odoo.conf.example config/odoo.conf

docker-compose up -d
# If you have Compose V2: docker compose up -d
```

Open http://localhost:8069

1. Create a database (master password = `admin` from the example config — **change it**).
2. Apps → **Update Apps List**.
3. Install **Estate** (and later **Bookstore**).

Stop:

```bash
docker-compose down
```

Data lives in Docker volumes (`odoo-web-data`, `odoo-db-data`).

## Local source install (this machine / contributors)

Use when you develop against Odoo **source** + venv (like `/www/odoo-dev`):

1. Clone [Odoo 19](https://github.com/odoo/odoo/tree/19.0) and create a venv; install `requirements.txt`.
2. Clone **this** repo (or put it on `addons_path`).
3. Copy `odoo.conf.example` → your real `odoo.conf` (outside git or gitignored).
4. Point `addons_path` at Odoo’s `addons` **and** this repo root, e.g.:

   ```ini
   addons_path = /path/to/odoo/addons,/path/to/odoo-bookstore
   ```

5. Start Odoo, update apps list, install modules.

Example start:

```bash
python odoo-bin -c /path/to/odoo.conf
```

After Python/XML changes: **restart** (for Python) and/or **Upgrade** the module.

## Modules

| Module | Purpose |
|--------|---------|
| `estate` | Real-estate learning app — **Server framework 101 complete** (Ch.1–15 + PDF reports) |
| `estate_account` | Link module: invoice buyer when property is Sold (+ report inherit) |
| `bookstore` | Portfolio module — v1.2: Book, Author, Sale + stock qty on confirm |

## Production notes

- Do **not** deploy with example passwords (`admin` / `odoo`).
- Typical production: Odoo service or containers + managed PostgreSQL + **this repo** (or a release tarball) on `addons_path`.
- Pin Odoo minor version and back up the DB before upgrades.
- This kit is a starting point, not a hardened prod checklist (TLS, backups, workers, limitting `admin_passwd`, etc.).

## License

Module licenses are declared per addon in each `__manifest__.py` (Estate: LGPL-3).
