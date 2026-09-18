#!/usr/bin/env bash
# Activa es_EC y lo deja como idioma por defecto (usuarios, compañías, website).
set -euo pipefail
DB="${1:-hr_th_dev}"
LANG_CODE="${2:-es_EC}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export MSYS_NO_PATHCONV=1

docker compose exec -T odoo odoo -c /etc/odoo/odoo.conf -d "$DB" --load-language="$LANG_CODE" --stop-after-init

docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf -d "$DB" --no-http <<PY
from odoo.addons.hr_service_management.hooks import ensure_default_lang
ensure_default_lang(env, "${LANG_CODE}")
env.cr.commit()
print("OK: idioma por defecto", env["ir.config_parameter"].sudo().get_param("hr_th.default_lang"))
PY
