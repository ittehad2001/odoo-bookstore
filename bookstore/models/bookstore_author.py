from odoo import fields, models


class BookstoreAuthor(models.Model):
    _name = "bookstore.author"
    _description = "Bookstore Author"
    _order = "name"

    name = fields.Char(required=True)
    bio = fields.Text(string="Biography")
    # hasMany(Book)
    book_ids = fields.One2many(
        "bookstore.book",
        "author_id",
        string="Books",
    )
