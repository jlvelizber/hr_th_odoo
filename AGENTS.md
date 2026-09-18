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

## Módulos custom

- `hr_service_management` — contratos, clientes TH, documentos, panel, nómina mensual vía proyectos
- `recruitment_service` — vacantes/candidatos por cliente, plantillas perfil
- `hr_ec_payroll` — Fase 2: períodos, novedades, roles de pago, PDF, KPIs panel
- `l10n_ec_th_edi` — Fase 3 base: trazabilidad SRI en facturas (XML/firma real pendiente)

## Reglas Cursor

Ver `.cursor/rules/` (`hr-th-platform.mdc` siempre activa).

## Fase actual

**Fases 2–3 (MVP):** `hr_ec_payroll` v3 (roles, IESS parametrizado, informe) + `l10n_ec_th_edi` instalado. Siguiente: normativa nómina profunda y FE SRI offline real. **Fase 4:** portal.
