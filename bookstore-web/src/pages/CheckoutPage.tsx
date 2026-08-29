import { type FormEvent, useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { checkout } from '../api/client'
import { useCart } from '../cart/CartContext'

function money(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export function CheckoutPage() {
  const { items, subtotal, clear } = useCart()
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  if (items.length === 0) {
    return <Navigate to="/cart" replace />
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setError('')
    setBusy(true)
    try {
      const result = await checkout({
        customer: { name, email, phone: phone || undefined },
        lines: items.map((item) => ({
          book_id: item.book.id,
          quantity: item.quantity,
        })),
      })
      clear()
      navigate('/success', { state: result })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Checkout failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="page">
      <h1>Guest checkout</h1>
      <p className="muted">Subtotal {money(subtotal)}</p>
      <form className="checkout-form" onSubmit={onSubmit}>
        <label>
          Name
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoComplete="name"
          />
        </label>
        <label>
          Email
          <input
            required
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
          />
        </label>
        <label>
          Phone <span className="muted">(optional)</span>
          <input
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            autoComplete="tel"
          />
        </label>
        {error && <p className="error">{error}</p>}
        <div className="actions">
          <button type="submit" className="cta" disabled={busy}>
            {busy ? 'Placing order…' : 'Place order'}
          </button>
          <Link to="/cart" className="text-link">
            Back to cart
          </Link>
        </div>
      </form>
    </main>
  )
}
