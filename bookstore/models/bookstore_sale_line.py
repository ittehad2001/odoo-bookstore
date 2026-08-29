from odoo import api, fields, models


class BookstoreSaleLine(models.Model):
    _name = "bookstore.sale.line"
    _description = "Bookstore Sale Line"
    _order = "id"

    sale_id = fields.Many2one(
        "bookstore.sale",
        string="Sale",
        required=True,
        ondelete="cascade",
    )
    book_id = fields.Many2one(
        "bookstore.book",
        string="Book",
        required=True,
        ondelete="restrict",
    )
    quantity = fields.Float(string="Quantity", default=1.0, required=True)
    price_unit = fields.Float(string="Unit Price")
    price_subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_price_subtotal",
        store=True,
    )

    @api.depends("quantity", "price_unit")
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = (line.quantity or 0.0) * (line.price_unit or 0.0)

    @api.onchange("book_id")
    def _onchange_book_id(self):
        if self.book_id:
            self.price_unit = self.book_id.price
