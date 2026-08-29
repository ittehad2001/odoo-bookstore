{
    "name": "Bookstore Account",
    "version": "1.0",
    "summary": "Create customer invoices when bookstore sales are confirmed",
    "description": """
        Link module between Bookstore and Accounting.
        When a sale is confirmed, creates a customer invoice from the sale lines.
    """,
    "author": "Ittehad",
    "category": "Sales",
    "depends": ["bookstore", "account"],
    "data": [
        "views/bookstore_sale_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
