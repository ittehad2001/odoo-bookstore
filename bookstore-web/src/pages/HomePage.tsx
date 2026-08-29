import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchBooks } from '../api/client'
import type { Book } from '../types'

function money(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export function HomePage() {
  const [books, setBooks] = useState<Book[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    fetchBooks()
      .then((data) => {
        if (alive) setBooks(data)
      })
      .catch((err: Error) => {
        if (alive) setError(err.message)
      })
      .finally(() => {
        if (alive) setLoading(false)
      })
    return () => {
      alive = false
    }
  }, [])

  return (
    <main>
      <section className="hero">
        <p className="eyebrow">Neighborhood books</p>
        <h1 className="brand-hero">Ink &amp; Spine</h1>
        <p className="lede">
          Browse the shelf, fill a cart, and check out as a guest — orders land
          straight in Odoo.
        </p>
        <a className="cta" href="#shelf">
          Browse the shelf
        </a>
      </section>

      <section id="shelf" className="shelf">
        <h2>On the shelf</h2>
        {loading && <p className="muted">Loading books…</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && books.length === 0 && (
          <p className="muted">No books yet. Add some in the Odoo Bookstore app.</p>
        )}
        <ul className="book-grid">
          {books.map((book) => (
            <li key={book.id}>
              <Link to={`/books/${book.id}`} className="book-tile">
                <span className="book-title">{book.name}</span>
                <span className="book-meta">
                  {book.author?.name || 'Unknown author'}
                </span>
                <span className="book-price">{money(book.price)}</span>
                <span className="book-stock">
                  {book.qty_available > 0
                    ? `${book.qty_available} in stock`
                    : 'Out of stock'}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
