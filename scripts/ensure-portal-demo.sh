#!/usr/bin/env bash
# Crea o actualiza usuario portal demo Empresa XYZ (Fase 4).
set -euo pipefail
DB="${1:-hr_th_dev}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export MSYS_NO_PATHCONV=1

docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf -d "$DB" --no-http <<'PY'
env = env
xyz = env.ref("hr_service_management.demo_partner_empresa_xyz", raise_if_not_found=False)
if not xyz:
    raise SystemExit("Falta demo Empresa XYZ: instale modulos con demo (ODOO_WITH_DEMO=1).")
Partner = env["res.partner"]
Users = env["res.users"]
portal_group = env.ref("base.group_portal")

def ensure_user(email, name, password):
    contact = Partner.search([("email", "=", email)], limit=1)
    if not contact:
        contact = Partner.create(
            {"name": name, "parent_id": xyz.id, "email": email, "type": "contact"}
        )
    user = Users.search([("login", "=", email)], limit=1)
    if not user:
        user = Users.with_context(no_reset_password=True).create(
            {
                "name": name,
                "login": email,
                "password": password,
                "partner_id": contact.id,
                "groups_id": [(6, 0, [portal_group.id])],
            }
        )
    else:
        user.write({"password": password, "active": True, "partner_id": contact.id})
        user.write({"groups_id": [(4, portal_group.id)]})
    return user

ensure_user("portal@empresaxyz.demo", "Portal Empresa XYZ", "portalxyz")
env.cr.commit()
print("OK: portal@empresaxyz.demo / portalxyz")
PY
