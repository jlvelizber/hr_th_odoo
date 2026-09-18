# Plataforma TH sobre Odoo 17

Gestión de servicios de Talento Humano para consultora (clientes, contratos, proyectos, reclutamiento, nómina operativa).
Estrategia: Odoo estándar → configuración → módulos custom.

## Inicio rápido

```bash
cd C:/laragon/www/hr-th-odoo
cp .env.example .env
# Alinear config/odoo.conf (db_password) con POSTGRES_PASSWORD del .env
docker compose up -d
```

La primera vez, el contenedor instala los módulos en `ODOO_INIT_MODULES` (por defecto: `hr_service_management`, `recruitment_service`, `hr_ec_payroll`, `l10n_ec_th_edi`) y dependencias (`l10n_ec`, Proyecto, Reclutamiento, etc.) en `POSTGRES_DB`. Ver logs: `docker compose logs -f odoo`.

Variables en `.env`: `ODOO_AUTO_BOOTSTRAP`, `ODOO_WITH_DEMO`, `ODOO_INIT_MODULES`, `ODOO_UPDATE_ON_START` (actualizar en cada arranque, solo dev).

Abrir http://localhost:8072 — detalle en **[docs/INSTALL.md](docs/INSTALL.md)**.

Módulos custom: `hr_service_management`, `recruitment_service`, `hr_ec_payroll`, `l10n_ec_th_edi`, `hr_th_portal`. Demo: **Empresa XYZ S.A.** Portal demo: `portal@empresaxyz.demo` / `portalxyz`.

## Comandos útiles

En **Git Bash** (MINGW), las rutas tipo `/etc/...` se reescriben a `C:/Program Files/Git/etc/...` y Odoo falla. Usa **`MSYS_NO_PATHCONV=1`** delante del comando, o ejecuta desde **PowerShell/CMD**.

```bash
docker compose down
docker compose logs -f odoo

# Primera instalación de módulos custom (Git Bash) — usa -i, no -u
MSYS_NO_PATHCONV=1 docker compose exec odoo odoo -c /etc/odoo/odoo.conf -d hr_th_dev \
  -i hr_service_management,recruitment_service --stop-after-init
docker compose restart odoo

# O: bash scripts/odoo-install-modules.sh hr_th_dev

# Actualizar tras cambios en código (módulos ya instalados)
MSYS_NO_PATHCONV=1 docker compose exec odoo odoo -c /etc/odoo/odoo.conf -d hr_th_dev \
  -u hr_service_management,recruitment_service --stop-after-init
```

PowerShell (sin conversión de rutas):

```powershell
docker compose exec odoo odoo -c /etc/odoo/odoo.conf -d hr_th_dev -u hr_service_management,recruitment_service --stop-after-init
```

## Backup

```bash
docker compose exec -T db pg_dump -U odoo -Fc hr_th_dev > backups/hr_th_dev_$(date +%F).dump
```

Restaurar: crear BD vacía y `pg_restore -U odoo -d hr_th_dev backups/hr_th_dev.dump`.

## Documentación

| Archivo | Contenido |
|---------|-----------|
| [docs/INSTALL.md](docs/INSTALL.md) | Instalación Fase 1 |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Decisiones aprobadas |
| [docs/roadmap.md](docs/roadmap.md) | Fases del proyecto |
| [docs/modules.md](docs/modules.md) | Mapa de módulos |
