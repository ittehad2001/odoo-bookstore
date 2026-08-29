from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property tag with this name already exists.",
    )

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
