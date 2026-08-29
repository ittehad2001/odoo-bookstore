from collections import defaultdict

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class BookstoreSale(models.Model):
    _name = "bookstore.sale"
    _description = "Bookstore Sale"
    _order = "id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        default="New",
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
    )
    date_order = fields.Date(
        string="Order Date",
        default=fields.Date.context_today,
        required=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="draft",
        required=True,
        copy=False,
    )
    line_ids = fields.One2many(
        "bookstore.sale.line",
        "sale_id",
        string="Order Lines",
    )
    amount_total = fields.Float(
        string="Total",
        compute="_compute_amount_total",
        store=True,
    )
    note = fields.Text(string="Notes")

    @api.depends("line_ids.price_subtotal")
    def _compute_amount_total(self):
        for sale in self:
            sale.amount_total = sum(sale.line_ids.mapped("price_subtotal"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("bookstore.sale") or "New"
                )
        return super().create(vals_list)

    def _quantities_by_book(self):
        """Sum line quantities per book (Laravel: groupBy book_id → sum qty)."""
        self.ensure_one()
        qty_by_book = defaultdict(float)
        for line in self.line_ids:
            if line.book_id:
                qty_by_book[line.book_id] += line.quantity or 0.0
        return qty_by_book

    def _apply_stock(self, sign):
        """sign=-1 on confirm (outbound), sign=+1 on cancel from confirmed (return)."""
        for sale in self:
            for book, qty in sale._quantities_by_book().items():
                if float_compare(qty, 0.0, precision_rounding=0.01) <= 0:
                    continue
                if sign < 0 and float_compare(
                    book.qty_available, qty, precision_rounding=0.01
                ) < 0:
                    raise UserError(
                        f"Not enough stock for '{book.name}'. "
                        f"Available: {book.qty_available}, needed: {qty}."
                    )
                book.qty_available = book.qty_available + (sign * qty)

    def action_confirm(self):
        for sale in self:
            if sale.state != "draft":
                raise UserError("Only draft sales can be confirmed.")
            if not sale.line_ids:
                raise UserError("Add at least one line before confirming.")
            sale._apply_stock(-1)
            sale.state = "confirmed"

    def action_cancel(self):
        for sale in self:
            if sale.state == "canceled":
                raise UserError("This sale is already canceled.")
            if sale.state == "confirmed":
                sale._apply_stock(+1)
            sale.state = "canceled"

    def action_draft(self):
        for sale in self:
            if sale.state != "canceled":
                raise UserError("Only canceled sales can be reset to draft.")
            sale.state = "draft"
