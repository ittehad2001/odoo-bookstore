#!/bin/bash
set -euo pipefail

TEMPLATE=/etc/bookstore/default.conf.template
TARGET=/etc/nginx/conf.d/default.conf

export ODOO_UPSTREAM="${ODOO_UPSTREAM:-web:8069}"
export ODOO_DB_NAME="${ODOO_DB_NAME:-odoo_dev}"

envsubst '${ODOO_UPSTREAM} ${ODOO_DB_NAME}' < "$TEMPLATE" > "$TARGET"
