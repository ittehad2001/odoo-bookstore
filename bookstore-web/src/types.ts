export type Author = {
  id: number
  name: string
}

export type Book = {
  id: number
  name: string
  isbn: string
  price: number
  qty_available: number
  author: Author | null
}

export type CartItem = {
  book: Book
  quantity: number
}

export type CheckoutResult = {
  sale: {
    id: number
    name: string
    state: string
    amount_total: number
    invoice_id: number | null
    invoice_name: string | null
  }
  customer: {
    id: number
    name: string
    email: string
  }
}
