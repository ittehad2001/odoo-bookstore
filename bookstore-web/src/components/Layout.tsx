import { Link, NavLink, Outlet } from 'react-router-dom'
import { useCart } from '../cart/CartContext'

export function Layout() {
  const { itemCount } = useCart()

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand-mark">
          Ink &amp; Spine
        </Link>
        <nav className="nav">
          <NavLink to="/" end>
            Shelf
          </NavLink>
          <NavLink to="/cart">
            Cart{itemCount > 0 ? ` (${itemCount})` : ''}
          </NavLink>
        </nav>
      </header>
      <Outlet />
      <footer className="footer">
        <p>Guest checkout · powered by Odoo Bookstore</p>
      </footer>
    </div>
  )
}
