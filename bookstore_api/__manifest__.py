{
    "name": "Bookstore API",
    "version": "1.0",
    "summary": "Public JSON API for the Bookstore React storefront",
    "description": """
        Exposes read-only book endpoints and a gated guest checkout
        that creates and confirms bookstore.sale records.
    """,
    "author": "Ittehad",
    "category": "Sales",
    "depends": ["bookstore"],
    "data": [
        "data/ir_config_parameter_data.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
