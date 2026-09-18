# Manual de usuario — Usuario TH

**Perfil:** operación diaria de la consultora (servicios, proyectos, documentos, reclutamiento operativo).  
**Grupo Odoo:** `Usuario TH` (`group_hr_th_user`).  
**Demo:** `th.usuario@consultora.demo` / `demoth`

## 1. Para qué sirve este perfil

Ejecutar el trabajo del día a día con los clientes: dar seguimiento a servicios contratados, proyectos y tareas, mantener el expediente documental y avanzar vacantes/candidatos. **No** configura el sistema ni calcula roles de pago.

## 2. Cómo entrar

1. Abrir http://localhost:8072 (o la URL de su instancia).
2. Iniciar sesión con su usuario.
3. En el menú principal, abrir **Talento Humano**.

## 3. Menú que verá

### Panel

| Opción | Uso |
|--------|-----|
| **Resumen** | Contadores: clientes activos, servicios, vacantes, tareas, documentos pendientes, facturas borrador. Filtrar por cliente o responsable y pulsar **Actualizar**. |
| **Clientes** | Empresas cliente (estado TH, contadores, expediente). |
| **Servicios activos** | Contratos `hr.service.contract` (nómina, reclutamiento, etc.). |
| **Proyectos** | Proyectos ligados a servicios TH. |
| **Tareas de servicios** | Tareas de esos proyectos (Kanban / lista). |
| **Nóminas en proceso** | Proyectos marcados como período de nómina (checklist), no el motor de cálculo. |
| **Colaboradores clientes** | Empleados marcados como trabajadores del cliente. |
| **Documentos** | Expediente estructurado (secciones + adjunto + estado). |

### Reclutamiento

| Opción | Uso |
|--------|-----|
| **Vacantes** | Puestos con cliente TH. |
| **Candidatos** | Pipeline de selección por cliente. |

**No verá:** Configuración TH, tipos de novedad, menú **Nómina** (períodos/roles), plantillas de perfil.

## 4. Flujos habituales

### 4.1 Revisar el panel

1. **Talento Humano → Panel → Resumen**.
2. Elija un **Cliente** si quiere acotar.
3. Use los botones **Ver** junto a cada indicador para abrir la lista filtrada.

### 4.2 Atender un servicio / proyecto

1. **Servicios activos** → abra el contrato del cliente.
2. Revise estado, fechas y responsable.
3. Desde el cliente o **Proyectos**, entre al proyecto y complete las **tareas** (p. ej. checklist mensual).

### 4.3 Documentos del cliente

1. Abra el **Cliente** → botones de documentos, o menú **Documentos**.
2. Estados típicos: *Pendiente* → *Cargado* → *Verificado*.
3. Suba el archivo en el campo correspondiente y cambie el estado cuando corresponda.

### 4.4 Reclutamiento operativo

1. **Vacantes** → cree o abra una vacante y asigne el **cliente**.
2. **Candidatos** → avance etapas (entrevista, etc.).
3. Las plantillas de perfil las define el **Responsable TH**; usted las usa si ya existen.

### 4.5 Colaboradores del cliente

1. **Colaboradores clientes** → alta o edición.
2. Marque que es colaborador de cliente y elija la empresa.
3. Use el expediente documental del colaborador cuando el proceso lo pida.

## 5. Buenas prácticas

- Trabaje siempre desde el **cliente** o el **contrato** para no mezclar empresas.
- No deje documentos en *Pendiente* sin seguimiento; use el panel.
- Si necesita calcular roles de pago o cerrar parámetros de nómina, escale a **Nómina TH** o **Responsable TH**.

## 6. Límites de este perfil

- Sin menú **Configuración** (secciones documentales, tipos de novedad, IESS %).
- Sin acceso al menú **Nómina** (períodos / novedades / roles calculados).
- Sin CRM/Ventas completo (eso es **Comercial TH**), salvo lo que el sistema le muestre por otros grupos.
