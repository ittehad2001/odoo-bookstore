{
    "name": "Estate",
    "version": "1.0",
    "summary": "Manage real estate properties",
    "description": """
        A simple real estate management application.
    """,
    "author": "Ittehad",
    "category": "Real Estate",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/res_users_views.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
