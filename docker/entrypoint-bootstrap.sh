#!/bin/bash
# Instala módulos TH al arrancar si la BD no existe o aún no están instalados.
set -euo pipefail

ODOO_DB="${ODOO_DB:-hr_th_dev}"
ODOO_INIT_MODULES="${ODOO_INIT_MODULES:-hr_service_management,recruitment_service}"
ODOO_AUTO_BOOTSTRAP="${ODOO_AUTO_BOOTSTRAP:-1}"
ODOO_WITH_DEMO="${ODOO_WITH_DEMO:-1}"
ODOO_UPDATE_ON_START="${ODOO_UPDATE_ON_START:-0}"
ODOO_CONF="${ODOO_CONF:-/etc/odoo/odoo.conf}"

HOST="${HOST:-db}"
USER="${USER:-odoo}"
PASSWORD="${PASSWORD:-odoo}"

module_state() {
    python3 <<PY
import os
import sys

try:
    import psycopg2
except ImportError:
    sys.exit(2)

db = os.environ.get("ODOO_DB", "hr_th_dev")
conn_args = dict(
    host=os.environ.get("HOST", "db"),
    user=os.environ.get("USER", "odoo"),
    password=os.environ.get("PASSWORD", "odoo"),
)

try:
    conn = psycopg2.connect(dbname=db, **conn_args)
except psycopg2.OperationalError:
    print("no_database")
    sys.exit(0)

cur = conn.cursor()
cur.execute(
    "SELECT state FROM ir_module_module WHERE name = %s LIMIT 1",
    ("hr_service_management",),
)
row = cur.fetchone()
print(row[0] if row else "missing")
PY
}

if [[ "${ODOO_AUTO_BOOTSTRAP}" == "1" ]]; then
    export ODOO_DB HOST USER PASSWORD
    state="$(module_state || true)"
    if [[ "${state}" == "no_database" || "${state}" != "installed" ]]; then
        demo_args=(--without-demo=all)
        if [[ "${ODOO_WITH_DEMO}" == "1" ]]; then
            demo_args=()
        fi
        echo "[hr-th-odoo] Instalando módulos (${ODOO_INIT_MODULES}) en BD ${ODOO_DB} (estado previo: ${state})..."
        wait-for-psql.py --db_host "${HOST}" --db_port "${PORT:-5432}" --db_user "${USER}" --db_password "${PASSWORD}" --timeout=60
        odoo -c "${ODOO_CONF}" -d "${ODOO_DB}" -i "${ODOO_INIT_MODULES}" "${demo_args[@]}" --stop-after-init
        echo "[hr-th-odoo] Instalación inicial completada."
    else
        echo "[hr-th-odoo] Módulos ya instalados en ${ODOO_DB}; omitiendo -i."
    fi
fi

if [[ "${ODOO_UPDATE_ON_START}" == "1" ]]; then
    echo "[hr-th-odoo] Actualizando módulos (${ODOO_INIT_MODULES})..."
    wait-for-psql.py --db_host "${HOST}" --db_port "${PORT:-5432}" --db_user "${USER}" --db_password "${PASSWORD}" --timeout=60
    odoo -c "${ODOO_CONF}" -d "${ODOO_DB}" -u "${ODOO_INIT_MODULES}" --stop-after-init
fi

exec /entrypoint.sh odoo -c "${ODOO_CONF}" "$@"
