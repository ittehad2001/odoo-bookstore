from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )

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
    # belongsTo(PropertyType)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    # buyer = Contact (res.partner); salesperson = User
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    # belongsToMany(Tag)
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    # hasMany(Offer)
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )
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

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        # Form-only helper (like livewire/alpine UX) — not server business logic
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_offer_received(self):
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

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        """Selling price cannot be lower than 90% of expected (docs Ch.10)."""
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_rounding=0.01) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
