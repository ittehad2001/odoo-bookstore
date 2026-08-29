import json
import logging

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)

CHECKOUT_KEY_PARAM = "bookstore_api.checkout_key"


class BookstoreAPIController(http.Controller):
    """Laravel feel: routes/api.php controllers for the React storefront."""

    def _cors_headers(self):
        return [
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
            (
                "Access-Control-Allow-Headers",
                "Origin, Content-Type, Accept, Authorization, X-Odoo-Database",
            ),
            ("Access-Control-Max-Age", "86400"),
        ]

    def _json(self, data, status=200):
        return request.make_json_response(
            data,
            headers=dict(self._cors_headers()),
            status=status,
        )

    def _json_error(self, message, status=400):
        return self._json({"error": message}, status=status)

    def _options(self):
        return request.make_response("", headers=self._cors_headers())

    def _book_payload(self, book):
        return {
            "id": book.id,
            "name": book.name,
            "isbn": book.isbn or "",
            "price": book.price,
            "qty_available": book.qty_available,
            "author": {
                "id": book.author_id.id,
                "name": book.author_id.name,
            }
            if book.author_id
            else None,
        }

    def _check_checkout_key(self):
        expected = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param(CHECKOUT_KEY_PARAM)
        )
        auth = request.httprequest.headers.get("Authorization", "")
        if not expected:
            return False
        return auth == f"Bearer {expected}"

    @http.route(
        "/api/bookstore/books",
        type="http",
        auth="public",
        methods=["GET", "OPTIONS"],
        csrf=False,
    )
    def books_list(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return self._options()
        books = (
            request.env["bookstore.book"]
            .sudo()
            .search([("active", "=", True)], order="name")
        )
        return self._json({"books": [self._book_payload(book) for book in books]})

    @http.route(
        "/api/bookstore/books/<int:book_id>",
        type="http",
        auth="public",
        methods=["GET", "OPTIONS"],
        csrf=False,
    )
    def books_detail(self, book_id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return self._options()
        book = request.env["bookstore.book"].sudo().browse(book_id)
        if not book.exists() or not book.active:
            return self._json_error("Book not found", status=404)
        return self._json({"book": self._book_payload(book)})

    @http.route(
        "/api/bookstore/checkout",
        type="http",
        auth="public",
        methods=["POST", "OPTIONS"],
        csrf=False,
    )
    def checkout(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return self._options()
        if not self._check_checkout_key():
            return self._json_error("Unauthorized", status=401)

        try:
            payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._json_error("Invalid JSON body")

        customer = payload.get("customer") or {}
        lines = payload.get("lines") or []
        name = (customer.get("name") or "").strip()
        email = (customer.get("email") or "").strip()
        phone = (customer.get("phone") or "").strip()

        if not name or not email:
            return self._json_error("Customer name and email are required")
        if not lines:
            return self._json_error("Cart is empty")

        Partner = request.env["res.partner"].sudo()
        partner = Partner.search([("email", "=ilike", email)], limit=1)
        if partner:
            vals = {}
            if name and partner.name != name:
                vals["name"] = name
            if phone and partner.phone != phone:
                vals["phone"] = phone
            if vals:
                partner.write(vals)
        else:
            partner = Partner.create(
                {
                    "name": name,
                    "email": email,
                    "phone": phone or False,
                }
            )

        Book = request.env["bookstore.book"].sudo()
        sale_lines = []
        for line in lines:
            book_id = line.get("book_id")
            qty = float(line.get("quantity") or 0)
            if not book_id or qty <= 0:
                return self._json_error("Each line needs book_id and quantity > 0")
            book = Book.browse(int(book_id))
            if not book.exists() or not book.active:
                return self._json_error(f"Book {book_id} not found", status=404)
            sale_lines.append(
                (
                    0,
                    0,
                    {
                        "book_id": book.id,
                        "quantity": qty,
                        "price_unit": book.price,
                    },
                )
            )

        Sale = request.env["bookstore.sale"].sudo()
        try:
            sale = Sale.create(
                {
                    "partner_id": partner.id,
                    "line_ids": sale_lines,
                    "note": "Created from React storefront (guest checkout).",
                }
            )
            sale.action_confirm()
        except UserError as err:
            return self._json_error(str(err), status=409)
        except Exception:
            _logger.exception("bookstore checkout failed")
            return self._json_error("Checkout failed", status=500)

        invoice = getattr(sale, "invoice_id", False)
        return self._json(
            {
                "sale": {
                    "id": sale.id,
                    "name": sale.name,
                    "state": sale.state,
                    "amount_total": sale.amount_total,
                    "invoice_id": invoice.id if invoice else None,
                    "invoice_name": invoice.display_name if invoice else None,
                },
                "customer": {
                    "id": partner.id,
                    "name": partner.name,
                    "email": partner.email,
                },
            },
            status=201,
        )
