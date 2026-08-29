from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    # Laravel accessor: getTotalAreaAttribute() — not a DB column by default
    total_area = fields.Integer(
        string="Total Area",
        compute="_compute_total_area",
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    # belongsTo(PropertyType) — FK column property_type_id
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    # status enum on the model (not a free-text Char)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        default="new",
        copy=False,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    def action_offer_received(self):
        """Laravel: $property->update(['state' => 'offer_received'])"""
        for record in self:
            record._check_not_final()
            record.state = "offer_received"
        return True

    def action_offer_accepted(self):
        for record in self:
            record._check_not_final()
            record.state = "offer_accepted"
        return True

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            record.state = "canceled"
        return True

    def _check_not_final(self):
        self.ensure_one()
        if self.state in ("sold", "canceled"):
            raise UserError("This property is already sold or canceled.")
