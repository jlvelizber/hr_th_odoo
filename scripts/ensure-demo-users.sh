#!/usr/bin/env bash
# Crea o actualiza usuarios demo de perfiles TH (consultora) en una BD existente.
set -euo pipefail
DB="${1:-hr_th_dev}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export MSYS_NO_PATHCONV=1

docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf -d "$DB" --no-http <<'PY'
env = env
Users = env["res.users"].with_context(no_reset_password=True)
password = "demoth"

profiles = [
    ("th.usuario@consultora.demo", "Ana Usuario TH", "hr_service_management.group_hr_th_user"),
    ("th.responsable@consultora.demo", "Carlos Responsable TH", "hr_service_management.group_hr_th_manager"),
    ("th.nomina@consultora.demo", "Lucia Nomina TH", "hr_service_management.group_hr_th_payroll"),
    ("th.comercial@consultora.demo", "Pedro Comercial TH", "hr_service_management.group_hr_th_commercial"),
]

created = []
for login, name, group_xmlid in profiles:
    group = env.ref(group_xmlid)
    user = Users.search([("login", "=", login)], limit=1)
    vals = {
        "name": name,
        "login": login,
        "password": password,
        "email": login,
        "groups_id": [(6, 0, [group.id])],
        "active": True,
    }
    if user:
        user.write(vals)
        created.append(f"updated:{login}")
    else:
        Users.create(vals)
        created.append(f"created:{login}")

# Asignar responsables en contratos demo si existen
Contract = env["hr.service.contract"]
nomina = Users.search([("login", "=", "th.nomina@consultora.demo")], limit=1)
usuario = Users.search([("login", "=", "th.usuario@consultora.demo")], limit=1)
payroll = Contract.search([("service_kind", "=", "payroll"), ("partner_id.vat", "=", "1791234567001")], limit=1)
recruit = Contract.search([("service_kind", "=", "recruitment"), ("partner_id.vat", "=", "1791234567001")], limit=1)
if payroll and nomina:
    payroll.write({"user_id": nomina.id})
if recruit and usuario:
    recruit.write({"user_id": usuario.id})

env.cr.commit()
print("OK perfiles TH:", ", ".join(created))
print("Password demo:", password)
PY
