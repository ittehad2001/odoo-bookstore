from odoo import Command, fields, models
from odoo.exceptions import UserError


class BookstoreSale(models.Model):
    _inherit = "bookstore.sale"

    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
        copy=False,
        readonly=True,
    )

    def action_confirm(self):
        """Laravel: after confirming the order, create an Invoice for the customer."""
        res = super().action_confirm()
        AccountMove = self.env["account.move"]
        for sale in self:
            if sale.invoice_id:
                continue
            if not sale.partner_id:
                raise UserError("You cannot confirm a sale without a customer.")
            move = AccountMove.create(
                {
                    "partner_id": sale.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_origin": sale.name,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": line.book_id.display_name,
                                "quantity": line.quantity,
                                "price_unit": line.price_unit,
                            }
                        )
                        for line in sale.line_ids
                    ],
                }
            )
            sale.invoice_id = move.id
        return res

    def action_cancel(self):
        for sale in self:
            invoice = sale.invoice_id
            if invoice and invoice.state == "posted":
                raise UserError(
                    "You cannot cancel a sale whose invoice is already posted. "
                    "Cancel or reverse the invoice first."
                )
            if invoice and invoice.state == "draft":
                invoice.button_cancel()
        return super().action_cancel()
