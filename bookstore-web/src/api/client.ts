import type { Book, CheckoutResult } from '../types'

const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')
const CHECKOUT_KEY = import.meta.env.VITE_CHECKOUT_API_KEY || ''
const ODOO_DB = import.meta.env.VITE_ODOO_DB || ''

function apiHeaders(extra: HeadersInit = {}): HeadersInit {
  const headers: Record<string, string> = {
    ...(extra as Record<string, string>),
  }
  // Only needed when calling Odoo directly (not via Vite proxy).
  if (ODOO_DB && API_BASE) {
    headers['X-Odoo-Database'] = ODOO_DB
  }
  return headers
}

async function readJson<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const message =
      typeof data === 'object' && data && 'error' in data
        ? String((data as { error: string }).error)
        : `Request failed (${response.status})`
    throw new Error(message)
  }
  return data as T
}

export async function fetchBooks(): Promise<Book[]> {
  const res = await fetch(`${API_BASE}/api/bookstore/books`, {
    headers: apiHeaders(),
  })
  const data = await readJson<{ books: Book[] }>(res)
  return data.books
}

export async function fetchBook(id: number): Promise<Book> {
  const res = await fetch(`${API_BASE}/api/bookstore/books/${id}`, {
    headers: apiHeaders(),
  })
  const data = await readJson<{ book: Book }>(res)
  return data.book
}

export async function checkout(payload: {
  customer: { name: string; email: string; phone?: string }
  lines: { book_id: number; quantity: number }[]
}): Promise<CheckoutResult> {
  const res = await fetch(`${API_BASE}/api/bookstore/checkout`, {
    method: 'POST',
    headers: apiHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${CHECKOUT_KEY}`,
    }),
    body: JSON.stringify(payload),
  })
  return readJson<CheckoutResult>(res)
}
