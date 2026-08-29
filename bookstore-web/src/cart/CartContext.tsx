import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import type { Book, CartItem } from '../types'

const STORAGE_KEY = 'inkspine.cart.v1'

type CartContextValue = {
  items: CartItem[]
  itemCount: number
  subtotal: number
  addItem: (book: Book, quantity?: number) => void
  setQuantity: (bookId: number, quantity: number) => void
  removeItem: (bookId: number) => void
  clear: () => void
}

const CartContext = createContext<CartContextValue | null>(null)

function loadCart(): CartItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw) as CartItem[]
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>(() => loadCart())

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  }, [items])

  const value = useMemo<CartContextValue>(() => {
    const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
    const subtotal = items.reduce(
      (sum, item) => sum + item.quantity * item.book.price,
      0,
    )

    return {
      items,
      itemCount,
      subtotal,
      addItem(book, quantity = 1) {
        setItems((current) => {
          const existing = current.find((item) => item.book.id === book.id)
          if (existing) {
            return current.map((item) =>
              item.book.id === book.id
                ? { ...item, book, quantity: item.quantity + quantity }
                : item,
            )
          }
          return [...current, { book, quantity }]
        })
      },
      setQuantity(bookId, quantity) {
        setItems((current) =>
          current
            .map((item) =>
              item.book.id === bookId ? { ...item, quantity } : item,
            )
            .filter((item) => item.quantity > 0),
        )
      },
      removeItem(bookId) {
        setItems((current) => current.filter((item) => item.book.id !== bookId))
      },
      clear() {
        setItems([])
      },
    }
  }, [items])

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used within CartProvider')
  return ctx
}
