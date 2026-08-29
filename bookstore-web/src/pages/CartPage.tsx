import { Link } from 'react-router-dom'
import { useCart } from '../cart/CartContext'

function money(value: number) {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export function CartPage() {
  const { items, subtotal, setQuantity, removeItem } = useCart()

  if (items.length === 0) {
    return (
      <main className="page">
        <h1>Cart</h1>
        <p className="muted">Your cart is empty.</p>
        <Link to="/" className="cta">
          Browse the shelf
        </Link>
      </main>
    )
  }

  return (
    <main className="page">
      <h1>Cart</h1>
      <ul className="cart-list">
        {items.map((item) => (
          <li key={item.book.id} className="cart-row">
            <div>
              <Link to={`/books/${item.book.id}`} className="book-title">
                {item.book.name}
              </Link>
              <p className="muted">{money(item.book.price)} each</p>
            </div>
            <label className="qty">
              Qty
              <input
                type="number"
                min={1}
                max={Math.max(1, item.book.qty_available)}
                value={item.quantity}
                onChange={(e) =>
                  setQuantity(item.book.id, Number(e.target.value) || 1)
                }
              />
            </label>
            <p className="cart-line-total">
              {money(item.quantity * item.book.price)}
            </p>
            <button
              type="button"
              className="text-button"
              onClick={() => removeItem(item.book.id)}
            >
              Remove
            </button>
          </li>
        ))}
      </ul>
      <div className="cart-footer">
        <p className="subtotal">Subtotal {money(subtotal)}</p>
        <Link to="/checkout" className="cta">
          Checkout
        </Link>
      </div>
    </main>
  )
}
