import { useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useCart } from '../cart/CartContext'
import type { CheckoutResult } from '../types'

function money(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export function SuccessPage() {
  const location = useLocation()
  const { clear } = useCart()
  const result = location.state as CheckoutResult | null

  useEffect(() => {
    if (result?.sale?.id) {
      clear()
    }
    // Clear once when landing on a successful order.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result?.sale?.id])

  if (!result?.sale) {
    return (
      <main className="page">
        <h1>No order to show</h1>
        <Link to="/" className="cta">
          Back to shelf
        </Link>
      </main>
    )
  }

  return (
    <main className="page success">
      <h1>Order placed</h1>
      <p className="lede">
        Thanks, {result.customer.name}. Your books are on the way into Odoo.
      </p>
      <dl className="success-meta">
        <div>
          <dt>Reference</dt>
          <dd>{result.sale.name}</dd>
        </div>
        <div>
          <dt>Total</dt>
          <dd>{money(result.sale.amount_total)}</dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>{result.sale.state}</dd>
        </div>
        {result.sale.invoice_name && (
          <div>
            <dt>Invoice</dt>
            <dd>{result.sale.invoice_name}</dd>
          </div>
        )}
      </dl>
      <Link to="/" className="cta">
        Keep browsing
      </Link>
    </main>
  )
}
