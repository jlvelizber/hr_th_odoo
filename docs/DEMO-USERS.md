# Usuarios demo — perfiles TH

Password unificada (solo desarrollo): **`demoth`**

| Perfil | Login | Grupo |
|--------|-------|--------|
| Usuario TH | `th.usuario@consultora.demo` | `group_hr_th_user` |
| Responsable TH | `th.responsable@consultora.demo` | `group_hr_th_manager` |
| Nomina TH | `th.nomina@consultora.demo` | `group_hr_th_payroll` |
| Comercial TH | `th.comercial@consultora.demo` | `group_hr_th_commercial` |
| Portal cliente XYZ | `portal@empresaxyz.demo` | `base.group_portal` (password: `portalxyz`) |

BD ya existente:

```bash
bash scripts/ensure-demo-users.sh hr_th_dev
bash scripts/ensure-portal-demo.sh hr_th_dev
```

Instalacion nueva con `ODOO_WITH_DEMO=1`: se cargan desde `demo/demo_users.xml` y `hr_th_portal/demo/demo_portal.xml`.

## Manuales por perfil

Indice: [manuales/README.md](manuales/README.md)

