#!/usr/bin/env bash
# Git Bash: evita convertir /etc/odoo/... a C:/Program Files/Git/...
set -euo pipefail
cd "$(dirname "$0")/.."
DB="${1:-hr_th_dev}"
export MSYS_NO_PATHCONV=1
docker compose exec odoo odoo -c /etc/odoo/odoo.conf -d "$DB" \
  -i hr_service_management,recruitment_service --stop-after-init
docker compose restart odoo
echo "Listo. Módulos instalados en $DB"
