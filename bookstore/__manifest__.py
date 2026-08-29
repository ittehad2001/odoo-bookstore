{
    "name": "Bookstore",
    "version": "1.2",
    "summary": "Manage books, authors, and sales",
    "description": """
        Portfolio bookstore module.
        Slice v1: Book + Author.
        Slice v1.1: Sale + lines with res.partner customer (draft/confirm/cancel).
        Slice v1.1.1: Unique ISBN constraint on books.
        Slice v1.2: Quantity on hand; decrease on confirm, restore on cancel.
    """,
    "author": "Ittehad",
    "category": "Sales",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/views.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
