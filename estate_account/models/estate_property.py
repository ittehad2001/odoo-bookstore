from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        """Laravel: after marking sold, create an Invoice for the buyer."""
        res = super().action_sold()
        AccountMove = self.env["account.move"]
        for prop in self:
            if not prop.buyer_id:
                raise UserError(
                    "You cannot sell a property without a buyer "
                    "(accept an offer first)."
                )
            AccountMove.create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": f"6% of selling price — {prop.name}",
                                "quantity": 1.0,
                                "price_unit": prop.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
            )
        return res
