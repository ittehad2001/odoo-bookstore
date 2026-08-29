{
    "name": "Bookstore",
    "version": "1.0",
    "summary": "Manage books and authors",
    "description": """
        Portfolio bookstore module (slice v1: Book + Author).
    """,
    "author": "Ittehad",
    "category": "Sales",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
