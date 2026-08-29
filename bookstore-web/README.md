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

Requires Odoo running with `bookstore_api` installed (`VITE_API_BASE_URL`).

## Env

| Variable | Purpose |
|----------|---------|
| `VITE_API_BASE_URL` | Odoo origin, e.g. `http://127.0.0.1:8069` |
| `VITE_ODOO_DB` | Database name (`X-Odoo-Database` header) |
| `VITE_CHECKOUT_API_KEY` | Must match Odoo `bookstore_api.checkout_key` |
