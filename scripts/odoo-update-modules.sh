#!/usr/bin/env bash
# Actualiza módulos ya instalados (-u). Para primera vez use odoo-install-modules.sh
set -euo pipefail
cd "$(dirname "$0")/.."
DB="${1:-hr_th_dev}"
export MSYS_NO_PATHCONV=1
docker compose exec odoo odoo -c /etc/odoo/odoo.conf -d "$DB" \
  -u hr_service_management,recruitment_service --stop-after-init
docker compose restart odoo
