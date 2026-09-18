# Manual de usuario — Nómina TH

**Perfil:** operación de nómina por cliente (períodos, novedades, roles de pago e informes).  
**Grupo Odoo:** `Nómina TH` (`group_hr_th_payroll`) — incluye Usuario TH.  
**Demo:** `th.nomina@consultora.demo` / `demoth`

## 1. Para qué sirve este perfil

Gestionar el ciclo mensual (u otro período) de nómina de los clientes: abrir períodos, registrar novedades, calcular roles parametrizados, imprimir PDF y actualizar estados. También usa el **Panel** y menús operativos de Usuario TH.

## 2. Cómo entrar

1. http://localhost:8072 → iniciar sesión.
2. **Talento Humano → Nómina**.

## 3. Menú Nómina

| Opción | Uso |
|--------|-----|
| **Períodos** | Cabecera del ciclo por cliente (fechas, estado, contrato de nómina, proyecto checklist). |
| **Novedades** | Horas extra, bonos, descuentos, etc., ligados al período y colaborador. |
| **Roles de pago** | Resultado del cálculo por empleado (`hr.ec.payroll.payslip`) e impresión PDF. |

También dispone de **Panel**, clientes, colaboradores, documentos y reclutamiento operativo (como Usuario TH).

**No configura** tipos de novedad ni % IESS (eso es **Responsable TH**), salvo que también le den ese grupo.

## 4. Flujo mensual recomendado

```text
Abrir período → Recopilar novedades → Confirmar novedades → Calcular roles → Revisar → Entregar / Cerrar
```

### 4.1 Abrir o localizar el período

1. **Nómina → Períodos**.
2. Cree un período: **Cliente**, fechas, contrato de tipo nómina (activo).
3. Opcional: vincular el **proyecto checklist** del mes (si se creó desde el wizard de período mensual).
4. Avance el **estado** del período según su proceso interno (pendiente → recopilación → proceso → revisión → aprobada → entregada → cerrada).

### 4.2 Colaboradores y salario base

1. **Colaboradores clientes** del cliente del período.
2. Verifique que estén marcados como trabajadores del cliente y con **salario base** (`th_wage`) si el cálculo lo usa.
3. Sin salario/novedades, el rol puede salir incompleto o en cero en conceptos.

### 4.3 Registrar novedades

1. Desde el período (líneas) o **Nómina → Novedades**.
2. Indique tipo, empleado, montos/cantidades y confirme cuando estén validadas.
3. Solo las novedades en estado adecuado entran al cálculo (según reglas del módulo).

### 4.4 Calcular roles

1. En el período, pulse **Calcular roles**.
2. El sistema genera/actualiza roles con ingresos, novedades e IESS % definido en la compañía.
3. Abra **Roles de pago** (stat o menú) y revise cada colaborador.
4. Imprima el **PDF** del rol cuando corresponda.

### 4.5 Cierre y entrega

1. Pase el período a *Aprobada* / *Entregada* según política interna.
2. Coordine con el cliente: en el **portal** solo verá el **estado del período**, no los montos ni el PDF de rol (entregables sensibles por el canal acordado).
3. Al terminar, **Cerrada** (bloquea nuevos cálculos según la lógica del módulo).

## 5. Panel: KPIs de nómina

En **Panel → Resumen** (con el módulo de nómina) verá indicadores de períodos abiertos y roles en borrador/calculados, con acceso rápido a esas listas.

## 6. Buenas prácticas

- Un período por cliente y rango de fechas; no mezclar clientes.
- Confirme novedades **antes** de calcular.
- Si los % IESS o tipos de novedad están mal, pida ajuste al **Responsable TH**.
- Guarde/imprima roles antes de cerrar el período.

## 7. Límites

- No es el motor legal completo de Ecuador (décimos, fondos de reserva, liquidaciones pueden estar pendientes según fase).
- No ve configuración de secciones documentales ni plantillas de reclutamiento (Responsable).
- El cliente portal **no** sustituye la entrega formal de roles.
