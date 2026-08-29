from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property type with this name already exists.",
    )

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        string="# Offers",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
