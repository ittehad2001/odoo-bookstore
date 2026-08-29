from odoo import fields, models


class BookstoreBook(models.Model):
    _name = "bookstore.book"
    _description = "Bookstore Book"
    _order = "name"

    name = fields.Char(string="Title", required=True)
    isbn = fields.Char(string="ISBN")
    # belongsTo(Author)
    author_id = fields.Many2one(
        "bookstore.author",
        string="Author",
        ondelete="restrict",
    )
    price = fields.Float(string="Price")
    active = fields.Boolean(default=True)
