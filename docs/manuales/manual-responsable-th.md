# Manual de usuario — Responsable TH

**Perfil:** coordinación y configuración de la operación TH.  
**Grupo Odoo:** `Responsable TH` (`group_hr_th_manager`) — incluye Usuario TH y capacidades de vendedor.  
**Demo:** `th.responsable@consultora.demo` / `demoth`

## 1. Para qué sirve este perfil

Supervisar la operación, parametrizar la app Talento Humano, definir plantillas de reclutamiento y tipos de novedad, y (si aplica) acompañar ventas. También puede usar el menú **Nómina** y gestionar el acceso **portal** de los clientes.

## 2. Cómo entrar

1. http://localhost:8072 → iniciar sesión.
2. Menú **Talento Humano** (tiene todo lo del Usuario TH **más** Configuración y Nómina).

## 3. Menú adicional respecto al Usuario TH

| Área | Opciones |
|------|----------|
| **Configuración** | Secciones documentales; tipos de novedad (bajo Configuración nómina). |
| **Nómina** | Períodos, novedades, roles de pago (misma app que Nómina TH). |
| **Reclutamiento** | **Perfiles plantilla** (además de vacantes y candidatos). |
| **Compañía** | Pestaña nómina Ecuador (IESS %, notas legales) — Ajustes / Compañías. |
| **Portal** | Botón **Portal** en la ficha del cliente empresa. |

También puede usar menús de **Ventas / CRM** según grupos Odoo implícitos.

## 4. Flujos habituales

### 4.1 Alta o activación de un cliente

1. **Panel → Clientes** → crear empresa (`es compañía`).
2. Complete **Estado TH**, nombre comercial, RUC (`l10n_ec`), contactos.
3. Pulse **Inicializar expediente documental** (o cree secciones/ítems según política).
4. Cree **servicios activos** (contratos) ligados a productos del catálogo.
5. Asigne **responsable** en el contrato (Usuario / Nómina según el servicio).

### 4.2 Configurar secciones documentales

1. **Talento Humano → Configuración → Secciones documentales**.
2. Defina nombre, código y ámbito (cliente, colaborador, proyecto, nómina).
3. Evite duplicar secciones; son la base del expediente de todos los clientes.

### 4.3 Plantillas de reclutamiento

1. **Reclutamiento → Perfiles plantilla**.
2. Cree perfiles reutilizables (requisitos, descripción).
3. Al abrir vacantes, el equipo operativo las aplica al cliente correspondiente.

### 4.4 Parámetros de nómina (compañía)

1. Ajustes → **Compañías** (o ficha de su compañía).
2. Pestaña **Nómina Ecuador (TH)**.
3. Configure % IESS empleado/empleador y notas legales (valores parametrizables; no hardcodear leyes en código).
4. **Configuración → Tipos de novedad** para horas extra, bonos, descuentos, etc.

### 4.5 Supervisar un ciclo de nómina

1. **Nómina → Períodos** (o wizard desde proyectos mensuales).
2. Confirme novedades → **Calcular roles** → revise PDF / estados.
3. Coordine entrega con el cliente (portal solo muestra **estado**, no montos).

Detalle operativo paso a paso: [manual-nomina-th.md](manual-nomina-th.md).

### 4.6 Invitar al portal del cliente

1. Abra el **cliente empresa**.
2. Botón inteligente **Portal**.
3. Asegure que los contactos tengan **email único**.
4. **Grant Access** / **Revoke Access** según corresponda.

Guía ampliada: [PORTAL.md](../PORTAL.md) y [manual-portal-cliente.md](manual-portal-cliente.md).

### 4.7 Usar el panel de supervisión

1. **Panel → Resumen** → filtre por cliente o responsable.
2. Atienda picos: documentos pendientes, tareas vencidas, nóminas abiertas, roles en borrador.

## 5. Buenas prácticas

- Separe **configuración** (pocas veces) de **operación** (diaria).
- Un solo responsable claro por contrato.
- Antes de producción: revise % IESS y tipos de novedad con el área legal/contable.
- No comparta usuarios admin; use este perfil o Nómina TH según la función.

## 6. Límites

- No es administrador técnico de Odoo (módulos, usuarios del sistema, contabilidad avanzada): eso es **Administración**.
- El cálculo legal ecuatoriano completo (décimos, liquidaciones, etc.) puede estar parcial según la fase del proyecto.
