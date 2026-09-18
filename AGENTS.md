# Guía para agentes — hr-th-odoo

## Objetivo

Plataforma de servicios de Talento Humano (consultora Ecuador) sobre **Odoo 17 Community**: clientes → contratos → proyectos/tareas → documentos → facturación.

## Documentación

| Archivo | Contenido |
|---------|-----------|
| [docs/DECISIONS.md](docs/DECISIONS.md) | Decisiones aprobadas |
| [docs/roadmap.md](docs/roadmap.md) | Fases 0–4 |
| [docs/modules.md](docs/modules.md) | Mapa módulos Odoo + custom |
| [docs/INSTALL.md](docs/INSTALL.md) | Docker, bootstrap, troubleshooting |
| [docs/functional-analysis.md](docs/functional-analysis.md) | Análisis funcional |
| [docs/technical-analysis.md](docs/technical-analysis.md) | Análisis técnico |
| [docs/DEMO-USERS.md](docs/DEMO-USERS.md) | Usuarios demo |
| [docs/manuales/README.md](docs/manuales/README.md) | Manuales por perfil |

## Módulos custom

- `hr_service_management` — contratos, clientes TH, documentos, panel, nómina mensual vía proyectos
- `recruitment_service` — vacantes/candidatos por cliente, plantillas perfil
- `hr_ec_payroll` — Fase 2: períodos, novedades, roles de pago, PDF, KPIs panel
- `l10n_ec_th_edi` — Fase 3 base: trazabilidad SRI en facturas (XML/firma real pendiente)
- `hr_th_portal` — Fase 4: portal multicliente por `partner_id`

## Reglas Cursor

Ver `.cursor/rules/` (`hr-th-platform.mdc` siempre activa).

## Fase actual

**Fases 2–4 (MVP):** nómina, SRI base y portal cliente (`hr_th_portal`). Idioma por defecto **`es_EC`** (bootstrap + `scripts/ensure-lang-es-ec.sh`). Siguiente: normativa nómina profunda, FE SRI real, mejoras portal.
