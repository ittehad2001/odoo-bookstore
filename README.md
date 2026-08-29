# Odoo Bookstore (custom addons)

Custom Odoo **19** modules, a React storefront, and a **prod-like Docker** kit.

This repo is **not** the full Odoo framework. Think Laravel: this is your `app/` + packages, not the framework core or `.env` secrets.

| In this repo | Not in this repo |
|--------------|------------------|
| `estate/`, `bookstore*`, `bookstore-web/` | Odoo core source |
| Docker + nginx same-URL layout | Real production secrets |

## Quick start — prod-like (same URL)

Needs: Docker + Compose (v1 or v2).

```bash
git clone git@github.com:ittehad2001/odoo-bookstore.git
cd odoo-bookstore

cp .env.example .env
cp config/odoo.conf.example config/odoo.conf
# Edit BOTH files: set matching DB password + admin_passwd (never commit real secrets).

docker compose up -d --build
# or: docker-compose up -d --build
```

Open **http://127.0.0.1:8080**

| Path | What |
|------|------|
| `/` | React storefront (Ink & Spine) |
| `/api/...` | Bookstore JSON API (proxied to Odoo) |
| `/odoo` or `/web` | Odoo admin / login |

First boot:

1. Open http://127.0.0.1:8080/web/database/manager  
2. Create DB named exactly `ODOO_DB_NAME` from `.env` (default `odoo_dev`) using `admin_passwd` from `config/odoo.conf`.  
3. Apps → **Update Apps List** → install **Bookstore**, **Bookstore Account**, **Bookstore API** (and Estate if you want).  
4. Set System Parameter `bookstore_api.checkout_key` = `BOOKSTORE_CHECKOUT_KEY` from `.env` (or keep the module default and match `.env`).

Stop:

```bash
docker compose down
```

Odoo is **not** published on host `:8069` in this layout (only nginx `:8080`). That matches production: app behind a reverse proxy.

### Laravel map

| Laravel prod | This kit |
|--------------|----------|
| nginx → PHP-FPM + public/ | nginx → static SPA + Odoo |
| `/` app, `/admin` Filament | `/` shop, `/odoo` backend |
| `/api` routes | `/api/bookstore/...` |

## Local source install (Odoo from git + Vite)

Use when developing against Odoo **source** + venv (like `/www/odoo-dev`):

1. Run Odoo on `:8069` with this repo on `addons_path`.  
2. `cd bookstore-web && cp .env.example .env && npm install && npm run dev` → http://127.0.0.1:5173 (Vite proxies `/api`).

## Modules

| Module / folder | Purpose |
|-----------------|---------|
| `bookstore` | Sales + stock + User/Admin security |
| `bookstore_account` | Invoice on sale confirm |
| `bookstore_api` | Public JSON API for the storefront |
| `bookstore-web/` | Vite React storefront |
| `estate` / `estate_account` | Server framework 101 learning track |
| `deploy/` | nginx + multi-stage proxy image |

## Production notes

- Change every password/key in `.env` and `config/odoo.conf` before any public host.  
- Real TLS: put another proxy (Caddy/Cloudflare) in front of `:8080` or terminate HTTPS on nginx.  
- Pin image tags, back up Postgres + filestore volumes before upgrades.  
- This kit is **prod-like topology**, not a full hardened checklist (WAF, backups, workers, monitoring).

## License

Module licenses are declared per addon in each `__manifest__.py`.
