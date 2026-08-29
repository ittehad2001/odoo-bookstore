import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchBook } from '../api/client'
import { useCart } from '../cart/CartContext'
import type { Book } from '../types'

function money(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export function BookPage() {
  const { id } = useParams()
  const { addItem } = useCart()
  const [book, setBook] = useState<Book | null>(null)
  const [error, setError] = useState('')
  const [added, setAdded] = useState(false)

  useEffect(() => {
    const bookId = Number(id)
    if (!bookId) {
      setError('Invalid book')
      return
    }
    let alive = true
    fetchBook(bookId)
      .then((data) => {
        if (alive) setBook(data)
      })
      .catch((err: Error) => {
        if (alive) setError(err.message)
      })
    return () => {
      alive = false
    }
  }, [id])

  if (error) {
    return (
      <main className="page">
        <p className="error">{error}</p>
        <Link to="/">Back to shelf</Link>
      </main>
    )
  }

  if (!book) {
    return (
      <main className="page">
        <p className="muted">Loading…</p>
      </main>
    )
  }

  const canBuy = book.qty_available > 0

  return (
    <main className="page detail">
      <Link to="/" className="back">
        ← Shelf
      </Link>
      <h1>{book.name}</h1>
      <p className="detail-author">{book.author?.name || 'Unknown author'}</p>
      {book.isbn && <p className="muted">ISBN {book.isbn}</p>}
      <p className="detail-price">{money(book.price)}</p>
      <p className="muted">
        {canBuy ? `${book.qty_available} available` : 'Out of stock'}
      </p>
      <div className="actions">
        <button
          type="button"
          className="cta"
          disabled={!canBuy}
          onClick={() => {
            addItem(book, 1)
            setAdded(true)
          }}
        >
          {canBuy ? 'Add to cart' : 'Unavailable'}
        </button>
        {added && (
          <Link to="/cart" className="text-link">
            View cart
          </Link>
        )}
      </div>
    </main>
  )
}
