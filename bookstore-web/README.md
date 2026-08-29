# Ink & Spine (bookstore-web)

React storefront for the Odoo **Bookstore** backend.

## Stack

- Vite + React + TypeScript
- Cart in `localStorage`
- Guest checkout → `POST /api/bookstore/checkout` (Bearer API key)

## Setup

```bash
cp .env.example .env
npm install
npm run dev
```

Open http://127.0.0.1:5173

Locally, Vite proxies `/api/*` → Odoo and injects `X-Odoo-Database`, so the browser stays same-origin (no CORS pain).

Requires Odoo running with `bookstore_api` installed.

## Env

| Variable | Purpose |
|----------|---------|
| `VITE_API_BASE_URL` | Leave empty for Vite proxy; or set Odoo origin for direct calls |
| `VITE_ODOO_DB` | Database name for proxy / direct `X-Odoo-Database` |
| `VITE_ODOO_PROXY_TARGET` | Odoo origin used by the Vite proxy |
| `VITE_CHECKOUT_API_KEY` | Must match Odoo `bookstore_api.checkout_key` |
