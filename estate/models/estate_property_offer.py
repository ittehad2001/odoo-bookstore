from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    _check_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            start = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.context_today(offer)
            )
            offer.date_deadline = start + relativedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            start = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.context_today(offer)
            )
            offer.validity = (offer.date_deadline - start).days if offer.date_deadline else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price") is not None:
                prop = self.env["estate.property"].browse(vals["property_id"])
                if prop.offer_ids:
                    max_offer = max(prop.offer_ids.mapped("price"))
                    if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                        raise UserError(
                            "The offer must be higher than existing offers "
                            f"(current best: {max_offer})."
                        )
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"
        return offers

    def action_accept(self):
        """Accept offer → set property selling price + buyer (docs Ch.9)."""
        for offer in self:
            if offer.property_id.state in ("sold", "canceled"):
                raise UserError("Cannot accept an offer on a sold or canceled property.")
            accepted = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o.id != offer.id
            )
            if accepted:
                raise UserError("Only one offer can be accepted for a property.")
            offer.status = "accepted"
            (offer.property_id.offer_ids - offer).write({"status": "refused"})
            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer_id": offer.partner_id.id,
                    "state": "offer_accepted",
                }
            )
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("An accepted offer cannot be refused directly.")
            offer.status = "refused"
        return True
