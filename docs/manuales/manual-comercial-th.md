# Manual de usuario — Comercial TH

**Perfil:** captación y venta de servicios TH (CRM y ventas).  
**Grupo Odoo:** `Comercial TH` (`group_hr_th_commercial`) — implica vendedor Odoo; **no** incluye por defecto Usuario TH.  
**Demo:** `th.comercial@consultora.demo` / `demoth`

## 1. Para qué sirve este perfil

Gestionar prospectos, cotizaciones y pedidos de servicios (nómina, reclutamiento, gestión TH, asesoría). Tras confirmar la venta, la operación la toman **Usuario / Responsable / Nómina TH**.

## 2. Cómo entrar

1. http://localhost:8072 → iniciar sesión.
2. Use los menús estándar **CRM** y **Ventas** (y Contactos/Facturación según permisos de vendedor).

**Nota:** Este perfil **no** abre el menú **Talento Humano** hasta que le agreguen también `Usuario TH` o `Responsable TH`. En la demo pura comercial, trabaje por CRM/Ventas y contactos.

## 3. Menús principales

| Menú | Uso |
|------|-----|
| **CRM** | Leads / oportunidades de empresas potenciales. |
| **Ventas** | Cotizaciones y pedidos; productos de tipo servicio (p. ej. administración de nómina, selección). |
| **Contactos** | Empresas y contactos (RUC con `l10n_ec`). |
| **Facturación** (si aplica) | Facturas de cliente derivadas de ventas. |

## 4. Flujos habituales

### 4.1 Prospecto → cliente

1. Cree un **Lead** u **oportunidad** en CRM con la empresa.
2. Cualifique necesidad (nómina, reclutamiento, etc.).
3. Convierta a **oportunidad / contacto** según el flujo estándar Odoo.
4. En el contacto empresa, si ya es cliente operativo, el equipo TH completará **Estado TH** y contratos; coordine el traspaso.

### 4.2 Cotizar un servicio

1. **Ventas → Cotizaciones** → Nueva.
2. Cliente = empresa.
3. Líneas con productos de catálogo (demo: *Administración de nómina mensual*, *Proceso de selección*).
4. Envíe la cotización y haga seguimiento en CRM.

### 4.3 Confirmar pedido y traspaso a operaciones

1. Confirme el pedido de venta.
2. Avise a **Responsable TH** / operaciones para:
   - Activar **Estado TH** en el partner.
   - Crear **contrato de servicio** (`hr.service.contract`) ligado al producto/pedido.
   - Inicializar expediente y responsables.
3. En demo, los contratos pueden vincularse al pedido (`sale_order_id`); verifique con operaciones que el vínculo exista.

### 4.4 Facturación

1. Desde el pedido, genere la **factura** según política (anticipo, mensual, por hito).
2. Use localización Ecuador (`l10n_ec`) en identificación del cliente.
3. La trazabilidad SRI electrónica (si está activa) la sigue Contabilidad / módulo EDI; no es el foco diario del comercial.

## 5. Relación con otros perfiles

| Quién | Qué hace después de su venta |
|-------|------------------------------|
| Responsable TH | Configura cliente, contratos, portal, plantillas. |
| Usuario TH | Ejecuta proyectos, documentos, reclutamiento. |
| Nómina TH | Corre períodos y roles. |
| Portal cliente | El cliente ve servicios/estado; usted no gestiona el portal salvo que tenga permisos extras. |

## 6. Buenas prácticas

- Use siempre productos del **catálogo de servicios**, no líneas libres sin control.
- Deje claro en la oportunidad el **tipo de servicio** y periodicidad.
- No prometa cálculos legales o plazos de nómina sin validar con Nómina/Responsable.
- Si necesita ver el Panel TH, solicite el grupo **Usuario TH** además de Comercial.

## 7. Límites

- Sin menú Talento Humano (en perfil solo comercial).
- Sin períodos, novedades ni roles de pago.
- Sin configuración de secciones documentales ni plantillas de perfil.
