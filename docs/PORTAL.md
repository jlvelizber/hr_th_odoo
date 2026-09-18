# Portal cliente (Fase 4)

Modulo: `hr_th_portal`. Dependencias: `portal`, `website`, `website_payment` (evita error 500 en login si el sitio referencia snippets de pago).

**Idioma:** por defecto `es_EC` (`ODOO_DEFAULT_LANG` en `.env`). BD ya existente: `bash scripts/ensure-lang-es-ec.sh hr_th_dev`.

## Usuario demo (BD de desarrollo)

Tras instalar el modulo, si el usuario demo no existe (datos demo con `noupdate`), ejecutar:

```bash
bash scripts/ensure-portal-demo.sh hr_th_dev
```

Credenciales:

| Login | Password |
|-------|----------|
| `portal@empresaxyz.demo` | `portalxyz` |

Entrada: http://localhost:8072/web/login → luego http://localhost:8072/my

## Invitar un contacto desde backoffice

1. Iniciar sesion como administrador / responsable TH.
2. **Talento Humano → Clientes** → abrir **Empresa XYZ S.A.** (o cualquier cliente empresa).
3. Clic en el boton inteligente **Portal** (icono usuario).
4. En el asistente aparecen la empresa y sus **contactos** con email.
5. Corregir email si hace falta (debe ser unico en Odoo).
6. **Grant Access** en la fila del contacto → Odoo envia invitacion por correo (si el servidor de correo esta configurado).
7. El contacto inicia sesion en `/web/login` con el enlace del correo o la clave que defina.

Para revocar: misma pantalla → **Revoke Access**.

## Que ve el cliente en `/my`

- **Servicios TH** → contratos activos
- **Expediente documental** → listado y carga de archivos pendientes
- **Nomina** → estado del periodo (sin montos ni roles de pago)
- **Vacantes** → procesos de seleccion de su empresa
- Facturas: enlace estandar **Invoices** de Contabilidad (si aplica)

Multicliente: cada usuario portal solo ve registros de su `commercial_partner_id` (reglas de registro).
