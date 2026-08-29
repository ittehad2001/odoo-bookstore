from odoo import api, fields, models
from odoo.exceptions import UserError


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

    def action_confirm(self):
        for sale in self:
            if sale.state != "draft":
                raise UserError("Only draft sales can be confirmed.")
            if not sale.line_ids:
                raise UserError("Add at least one line before confirming.")
            sale.state = "confirmed"

    def action_cancel(self):
        for sale in self:
            if sale.state == "canceled":
                raise UserError("This sale is already canceled.")
            if sale.state == "confirmed":
                # Allow cancel from confirmed for v1.1; stock later can tighten this.
                pass
            sale.state = "canceled"

    def action_draft(self):
        for sale in self:
            if sale.state != "canceled":
                raise UserError("Only canceled sales can be reset to draft.")
            sale.state = "draft"
