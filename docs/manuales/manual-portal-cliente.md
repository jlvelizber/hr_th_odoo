# Manual de usuario — Portal cliente

**Perfil:** contacto de la empresa cliente con acceso web limitado a los datos de su compañía.  
**Grupo Odoo:** `Portal` (`base.group_portal`).  
**Demo:** `portal@empresaxyz.demo` / `portalxyz`  
**Entrada:** http://localhost:8072/web/login → luego http://localhost:8072/my

## 1. Para qué sirve este perfil

Consultar el estado de los servicios contratados con la consultora, cargar documentos pendientes, ver el avance de períodos de nómina (**sin montos ni roles**) y revisar vacantes abiertas de su empresa. No es un usuario interno de Odoo.

## 2. Cómo obtener acceso

1. Su empresa debe ser cliente activo en la plataforma.
2. Un contacto suyo (con email válido y único) es invitado desde la ficha del cliente → botón **Portal** → **Grant Access**.
3. Recibirá correo de invitación (si el servidor de correo está configurado) o le entregarán usuario/clave por el canal acordado.
4. Inicie sesión en `/web/login` y abra **Mi cuenta** / `/my`.

Detalle para la consultora: [PORTAL.md](../PORTAL.md).

## 3. Qué verá en `/my` (Mi portal)

| Acceso | Qué puede hacer |
|--------|-----------------|
| **Servicios TH** | Listar y abrir contratos de servicio de **su** empresa. |
| **Expediente documental** | Ver documentos; **subir o reemplazar** archivo si está pendiente/cargado. |
| **Nómina** | Ver períodos y su **estado** (pendiente, en proceso, entregada…). **Sin** roles de pago ni valores. |
| **Vacantes** | Ver procesos de selección abiertos de su empresa. |
| **Facturas** (estándar Odoo) | Si existen facturas a su nombre, el portal de Contabilidad las muestra. |

Solo aparecen datos de su **empresa comercial** (`commercial_partner_id`). No ve otros clientes.

## 4. Flujos habituales

### 4.1 Revisar servicios contratados

1. `/my` → **Servicios TH** (o `/my/th/contracts`).
2. Abra un contrato para ver servicio, tipo y estado.
3. Para cambios contractuales, contacte a su responsable en la consultora (no se editan desde el portal).

### 4.2 Subir un documento pendiente

1. `/my/th/documents`.
2. Abra el ítem en estado pendiente o cargado.
3. Elija el archivo → **Enviar**.
4. La consultora verificará el documento (estado *Verificado*).

### 4.3 Seguir la nómina del mes

1. `/my/th/payroll`.
2. Consulte el período y su estado.
3. Los **roles de pago y montos** no se muestran aquí; la entrega formal la coordina la consultora.

### 4.4 Consultar vacantes

1. `/my/th/jobs`.
2. Revise puestos en proceso para su empresa.
3. Avance de candidatos: canal con su contacto de reclutamiento en la consultora.

## 5. Seguridad y privacidad

- No comparta su usuario.
- Si cambia de correo o deja la empresa, pida **Revoke Access** al responsable TH.
- No verá salarios, roles PDF ni datos de otras empresas.

## 6. Problemas frecuentes

| Situación | Qué hacer |
|-----------|-----------|
| No ve menús TH en `/my` | Confirme que su contacto está bajo la empresa cliente correcta y con grupo Portal. |
| Error al iniciar sesión / página en blanco | Avise a la consultora (a veces faltan módulos website). |
| No puede subir archivo | El documento puede estar ya *Verificado* o sin permiso de escritura; contacte a operaciones. |
| No aparecen períodos | La consultora aún no creó el período o no está ligado a su empresa. |

## 7. Límites

- Solo lectura en contratos, períodos y vacantes (salvo carga de documentos).
- Sin Panel interno, sin CRM, sin cálculo de nómina.
- Sin acceso a configuración ni a usuarios de la consultora.
