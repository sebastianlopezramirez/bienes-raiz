# 🏢 Viviendo Grupo Inmobiliario — CRM Blueprint v1.0

> **Documento maestro de arquitectura funcional**
> Propósito: Definir los módulos, flujos y pantallas del panel administrativo CRM propio para Viviendo, con capacidad de publicación multiportal (tipo Wasi) y gestión integral de propiedades en renta.

---

## 📌 ÍNDICE

1. [Visión General del Sistema](#1-visión-general-del-sistema)
2. [Roles y Usuarios del Sistema](#2-roles-y-usuarios-del-sistema)
3. [Módulos del CRM](#3-módulos-del-crm)
4. [Motor de Publicación Multiportal](#4-motor-de-publicación-multiportal)
5. [Panel Administrativo — Pantallas y Vistas](#5-panel-administrativo--pantallas-y-vistas)
6. [Flujo de Trabajo Principal](#6-flujo-de-trabajo-principal)
7. [Base de Datos — Entidades Clave](#7-base-de-datos--entidades-clave)
8. [Integraciones Externas](#8-integraciones-externas)
9. [Diferenciadores vs Wasi](#9-diferenciadores-vs-wasi)
10. [Stack Tecnológico Sugerido](#10-stack-tecnológico-sugerido)
11. [Fases de Desarrollo](#11-fases-de-desarrollo)

---

## 1. Visión General del Sistema

### ¿Qué es este sistema?
Un CRM inmobiliario **privado y propietario** para Viviendo Grupo Inmobiliario que centraliza:

- La **gestión de propiedades** (captación, publicación, seguimiento)
- La **relación con prospectos, inquilinos y propietarios**
- La **publicación automática** en portales externos (Mercado Libre, Vivanuncios, Lamudi, etc.)
- La **administración de contratos y pagos de renta**
- El **seguimiento comercial** (pipeline de leads)

### Problema que resuelve
| Sin CRM | Con CRM Viviendo |
|---|---|
| Propiedades en hojas de cálculo | Base de datos centralizada con fotos y docs |
| Leads perdidos en WhatsApp/email | Pipeline visual por etapas |
| Publicación manual en cada portal | Un clic → todos los portales |
| Sin historial del cliente | 360° del prospecto/inquilino |
| Contratos en papel | Contratos digitales con alertas de vencimiento |

---

## 2. Roles y Usuarios del Sistema

```
SUPER ADMIN (Gerencia Viviendo)
    ├── ADMIN (Coordinador de oficina)
    │       ├── AGENTE COMERCIAL (Asesores de renta)
    │       └── AGENTE CAPTADOR (Captación de propiedades)
    ├── PROPIETARIO (Portal externo lectura)
    └── INQUILINO (Portal externo pagos/comunicación)
```

### Permisos por Rol

| Módulo | Super Admin | Admin | Agente Comercial | Agente Captador | Propietario | Inquilino |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Propiedades (CRUD) | ✅ | ✅ | 👁 | ✅ | 👁 | ❌ |
| Publicar en portales | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Ver leads / CRM | ✅ | ✅ | ✅ propio | ❌ | ❌ | ❌ |
| Contratos | ✅ | ✅ | 👁 | ❌ | 👁 propio | 👁 propio |
| Pagos y cobranza | ✅ | ✅ | ❌ | ❌ | 👁 propio | ✅ propio |
| Reportes | ✅ | ✅ | parcial | ❌ | ❌ | ❌ |
| Configuración | ✅ | parcial | ❌ | ❌ | ❌ | ❌ |

---

## 3. Módulos del CRM

### 3.1 MÓDULO: Propiedades (Inventario)

**¿Qué hace?** Centraliza todo el inventario de inmuebles disponibles para rentar.

**Campos por propiedad:**
```
INFORMACIÓN GENERAL
├── Código interno (autogenerado: VIV-2024-001)
├── Tipo: Vivienda / Oficina / Local comercial / Bodega
├── Operación: Renta (fijo) | puede expandirse a Venta
├── Estado: Disponible / Rentada / En revisión / Suspendida
├── Propietario vinculado (FK → Módulo Propietarios)
└── Agente responsable (FK → Usuarios)

UBICACIÓN
├── Dirección completa
├── Colonia / Fraccionamiento
├── Ciudad / Estado
├── Código postal
└── Geolocalización (lat/lng para mapa)

CARACTERÍSTICAS FÍSICAS
├── Superficie total (m²)
├── Superficie construida (m²)
├── Recámaras / Baños / Medios baños
├── Estacionamientos
├── Pisos del inmueble
├── Antigüedad
├── Nivel/Piso (en caso de departamento)
├── Amenidades: [Jardín, Alberca, Gimnasio, Seguridad 24h, ...]
└── Extras: [Amueblado, Mascotas permitidas, Fumadores, ...]

ECONÓMICO
├── Precio de renta mensual (MXN)
├── Depósito en garantía
├── Meses de anticipo solicitados
├── Comisión agencia (%)
└── Precio administración mensual (%)

MULTIMEDIA
├── Fotos (hasta 30, ordenables con drag & drop)
├── Videos / Tour virtual (URL YouTube/Matterport)
├── Planos (PDF)
└── Documentos del inmueble (escrituras, predial, agua)

PUBLICACIÓN
├── Título del anuncio
├── Descripción larga (editor de texto enriquecido)
├── Palabras clave (SEO)
└── Portales activos: [Mercado Libre, Vivanuncios, Lamudi, ...]
```

---

### 3.2 MÓDULO: Prospectos / Leads (CRM Pipeline)

**¿Qué hace?** Gestiona todos los contactos interesados en rentar, desde el primer contacto hasta el cierre.

**Pipeline de etapas:**
```
[NUEVO LEAD] → [CONTACTADO] → [VISITA AGENDADA] → [VISITA REALIZADA] → [PROPUESTA ENVIADA] → [NEGOCIACIÓN] → [CONTRATO FIRMADO] → [CERRADO ❌ / GANADO ✅]
```

**Ficha del prospecto:**
```
DATOS PERSONALES
├── Nombre completo
├── Teléfono / WhatsApp
├── Email
├── RFC / CURP (para expediente)
└── Fuente del lead: [Portal web, Mercado Libre, Referido, Walk-in, Redes sociales]

NECESIDAD
├── Tipo de inmueble buscado
├── Zona preferida
├── Presupuesto máximo (renta mensual)
├── Fecha requerida de entrada
├── Número de ocupantes
├── Mascotas / Fumador
└── Notas especiales

SEGUIMIENTO
├── Historial de actividades (llamadas, emails, WhatsApp)
├── Propiedades mostradas (vinculadas)
├── Próxima acción + fecha recordatorio
├── Agente asignado
└── Prioridad: Alta / Media / Baja
```

**Acciones rápidas desde el lead:**
- 📞 Registrar llamada (con resultado)
- 📅 Agendar visita (vincula con Google Calendar)
- 🏠 Vincular propiedades sugeridas
- 📧 Enviar email con ficha técnica (template)
- 💬 Abrir chat WhatsApp directo
- 📄 Convertir a Inquilino (al cerrar contrato)

---

### 3.3 MÓDULO: Propietarios

**¿Qué hace?** Gestiona la relación con los dueños de las propiedades en administración.

```
DATOS DEL PROPIETARIO
├── Nombre / Razón social
├── RFC (persona física o moral)
├── Datos de contacto: tel, email, WhatsApp
├── Datos bancarios: banco, CLABE interbancaria
└── Dirección fiscal

PROPIEDADES VINCULADAS
└── Lista de inmuebles del propietario (con estado y ocupación actual)

PORTAL PROPIETARIO (acceso externo)
├── Ver estado de sus propiedades
├── Historial de pagos recibidos
├── Documentos descargables (contratos, comprobantes)
└── Estado de cuenta mensual PDF
```

---

### 3.4 MÓDULO: Inquilinos

**¿Qué hace?** Gestiona a todos los inquilinos activos con su propiedad asignada y contrato vigente.

```
EXPEDIENTE DIGITAL DEL INQUILINO
├── Datos personales + CURP + RFC
├── Documentos cargados: [ID, Comprobante domicilio, Comprobante ingresos, Aval, Fiador]
├── Score / Calificación crediticia (si aplica)
└── Historial de rentas anteriores (referencia)

CONTRATO ACTIVO
├── Propiedad rentada (FK)
├── Fecha inicio / fin de contrato
├── Monto mensual acordado
├── Depósito entregado
├── Fecha de pago acordada (día del mes)
└── Incremento anual pactado (%)

PORTAL INQUILINO
├── Ver estado de su contrato
├── Historial de pagos
├── Descargar recibos de pago
├── Solicitar mantenimiento (tickets)
└── Comunicarse con la administración
```

---

### 3.5 MÓDULO: Contratos

**¿Qué hace?** Centraliza todos los contratos de arrendamiento con alertas automáticas.

```
DATOS DEL CONTRATO
├── Número de contrato (autogenerado)
├── Tipo: Arrendamiento residencial / comercial / oficina
├── Propietario + Inquilino + Propiedad (FKs)
├── Vigencia: fecha inicio → fecha fin
├── Monto mensual
├── Depósito en garantía
├── Cláusulas especiales (texto libre)
└── Documento firmado (PDF upload / firma electrónica)

ALERTAS AUTOMÁTICAS
├── ⚠️ 90 días antes del vencimiento → notif. al agente
├── ⚠️ 60 días antes → notif. al propietario e inquilino
├── ⚠️ 30 días antes → recordatorio urgente
└── 📅 Fecha de incremento anual → aviso con nuevo monto

ESTADOS DEL CONTRATO
Activo → Por vencer → Renovado → Rescindido → Vencido
```

---

### 3.6 MÓDULO: Pagos y Cobranza

**¿Qué hace?** Registra y controla los pagos de renta mensuales.

```
REGISTRO DE PAGO
├── Contrato asociado (FK)
├── Período (mes/año)
├── Monto esperado vs monto pagado
├── Fecha de pago
├── Método: [Transferencia, Depósito, Efectivo, Tarjeta]
├── Comprobante (imagen/PDF)
└── Registrado por (usuario del sistema)

ESTADO DE CUENTA POR INQUILINO
├── Pagos al corriente ✅
├── Pagos con retraso 🟡
├── Pagos vencidos 🔴
└── Saldo pendiente

COBRANZA AUTOMATIZADA
├── Email/WhatsApp automático día 1 del mes (recordatorio)
├── Alerta día 5 si no hay pago registrado
└── Escalamiento a admin día 10

REPORTE FINANCIERO
├── Ingresos por renta (por período, por propiedad, por agente)
├── Comisiones generadas Viviendo
├── Pagos pendientes (cartera vencida)
└── Proyección de ingresos próximo mes
```

---

### 3.7 MÓDULO: Mantenimiento y Servicios

**¿Qué hace?** Gestiona solicitudes de reparación y mantenimiento de propiedades en administración.

```
TICKET DE MANTENIMIENTO
├── Solicitante: [Inquilino / Agente / Propietario]
├── Propiedad (FK)
├── Categoría: [Plomería, Electricidad, Pintura, Jardinería, Cerrajería, ...]
├── Descripción del problema
├── Fotos adjuntas
├── Prioridad: Urgente / Normal / Baja
├── Estado: Abierto → Asignado → En proceso → Resuelto
├── Proveedor asignado (contacto externo)
├── Costo estimado / real
└── ¿Quién paga?: Inquilino / Propietario / Viviendo

HISTORIAL POR PROPIEDAD
└── Todos los mantenimientos realizados en el inmueble
```

---

### 3.8 MÓDULO: Reportes y Dashboard

**Dashboard principal (KPIs en tiempo real):**
```
┌─────────────────────────────────────────────────────┐
│  VIVIENDO CRM — PANEL PRINCIPAL                      │
├──────────────┬──────────────┬────────────────────────┤
│ Propiedades  │ Ocupación    │ Ingresos del mes       │
│ Disponibles  │ 87%          │ $XXX,XXX MXN           │
│   12         │              │                        │
├──────────────┼──────────────┼────────────────────────┤
│ Leads nuevos │ Visitas hoy  │ Contratos por vencer   │
│ esta semana  │              │ próx. 30 días          │
│   28         │   5          │   3                    │
├──────────────┴──────────────┴────────────────────────┤
│ PIPELINE DE VENTAS (Kanban)                          │
│ [Nuevo] [Contactado] [Visita] [Propuesta] [Cierre]  │
└─────────────────────────────────────────────────────┘
```

**Reportes disponibles:**
- Inventario de propiedades (por tipo, zona, precio, estado)
- Pipeline comercial (conversión por etapa, tiempo promedio de cierre)
- Rendimiento por agente (leads, visitas, cierres)
- Financiero (ingresos, comisiones, cobranza)
- Ocupación (tasa general, por tipo de inmueble, por zona)
- Vencimientos de contratos (próximos 30/60/90 días)

---

## 4. Motor de Publicación Multiportal

### ¿Cómo funciona?

```
VIVIENDO CRM
    │
    ├── Agente carga propiedad (1 vez, toda la info)
    │
    └── Selecciona portales → [Publicar]
            │
            ├── 🟢 Portal Web Viviendo (propio)
            ├── 🟡 Mercado Libre Inmuebles (API oficial)
            ├── 🔵 Vivanuncios
            ├── 🟣 Lamudi
            ├── 🟠 Inmuebles24
            └── ⚪ Facebook Marketplace (manual/semi-auto)
```

### Estados de publicación por portal

| Propiedad | Web Propia | Mercado Libre | Vivanuncios | Lamudi |
|---|:---:|:---:|:---:|:---:|
| VIV-001 Depto Polanco | ✅ Activo | ✅ Activo | ⏸ Pausado | ❌ No publicado |
| VIV-002 Local Roma | ✅ Activo | ✅ Activo | ✅ Activo | ✅ Activo |
| VIV-003 Oficina Reforma | ⏸ Pendiente | ❌ — | ❌ — | ❌ — |

### Sincronización de cambios

Cuando el agente modifica precio, fotos o descripción en el CRM:
```
CRM actualizado → Webhook/API → Portales activos actualizados automáticamente
```

Cuando la propiedad se renta:
```
Estado → "Rentada" → Despublicación automática en todos los portales activos
```

### Integración con Mercado Libre (prioridad 1)

```javascript
// Flujo de integración con ML Real Estate API
POST https://api.mercadolibre.com/items
{
  "site_id": "MLM", // México
  "category_id": "MLM1473", // Inmuebles en renta
  "title": "Departamento en renta Polanco 2 recámaras",
  "price": 18000,
  "currency_id": "MXN",
  "available_quantity": 1,
  "pictures": [...fotos_urls],
  "attributes": [
    { "id": "TOTAL_AREA", "value_name": "80 m²" },
    { "id": "ROOMS", "value_name": "2" },
    { "id": "FULL_BATHROOMS", "value_name": "1" }
  ],
  "location": { "address_line": "...", "zip_code": "..." }
}
```

---

## 5. Panel Administrativo — Pantallas y Vistas

### Mapa de pantallas

```
LOGIN
│
└── DASHBOARD (Home)
        │
        ├── PROPIEDADES
        │       ├── Lista / Grid / Mapa
        │       ├── Nueva propiedad
        │       ├── Detalle propiedad
        │       │       ├── Tab: Info general
        │       │       ├── Tab: Multimedia
        │       │       ├── Tab: Publicación (portales)
        │       │       ├── Tab: Historial de leads
        │       │       └── Tab: Contrato activo
        │       └── Filtros avanzados
        │
        ├── CRM (Leads)
        │       ├── Vista Kanban (Pipeline)
        │       ├── Vista Lista (tabla)
        │       ├── Nuevo lead
        │       └── Detalle lead (ficha 360°)
        │
        ├── PROPIETARIOS
        │       ├── Lista de propietarios
        │       ├── Nuevo propietario
        │       └── Detalle propietario
        │               ├── Sus propiedades
        │               └── Estado de cuenta
        │
        ├── INQUILINOS
        │       ├── Lista de inquilinos activos
        │       ├── Expediente digital
        │       └── Detalle inquilino
        │               ├── Contrato activo
        │               └── Historial de pagos
        │
        ├── CONTRATOS
        │       ├── Lista de contratos
        │       ├── Nuevo contrato
        │       ├── Alertas de vencimiento
        │       └── Renovaciones pendientes
        │
        ├── PAGOS Y COBRANZA
        │       ├── Registro de pagos
        │       ├── Estado de cuenta (todos los inquilinos)
        │       └── Pagos vencidos (cartera)
        │
        ├── MANTENIMIENTO
        │       ├── Tickets abiertos
        │       └── Historial
        │
        ├── PUBLICACIONES (Portales)
        │       ├── Dashboard de publicaciones activas
        │       ├── Estado por portal
        │       └── Log de sincronización
        │
        ├── REPORTES
        │       ├── Dashboard KPIs
        │       ├── Reporte financiero
        │       ├── Reporte ocupación
        │       └── Reporte agentes
        │
        └── CONFIGURACIÓN
                ├── Usuarios y permisos
                ├── Tokens API portales
                ├── Templates de email/WhatsApp
                ├── Configuración de alertas
                └── Datos de la empresa
```

---

## 6. Flujo de Trabajo Principal

### Flujo A: Captación de nueva propiedad

```
1. Propietario contacta a Viviendo
        ↓
2. Agente crea registro en Módulo Propietarios
        ↓
3. Agente crea la propiedad en el CRM
   (llena todos los campos, sube fotos, docs)
        ↓
4. Admin revisa y aprueba la propiedad
        ↓
5. Sistema publica en portales seleccionados (automático)
        ↓
6. Propiedad aparece en portal web + Mercado Libre + otros
```

### Flujo B: Atención a prospecto hasta cierre

```
1. Lead llega (formulario web / Mercado Libre / WhatsApp)
        ↓
2. Sistema crea lead automáticamente en CRM (etapa: Nuevo)
        ↓
3. Agente lo contacta → registra llamada → actualiza a "Contactado"
        ↓
4. Se agenda visita → etapa "Visita agendada"
        ↓
5. Visita realizada → agente registra resultado → "Propuesta enviada"
        ↓
6. Negociación → "En negociación"
        ↓
7. Acuerdo → se genera contrato → lead pasa a "Ganado"
        ↓
8. Lead se convierte en Inquilino (datos se migran automáticamente)
        ↓
9. Propiedad cambia a estado "Rentada"
        ↓
10. Sistema despublica en todos los portales automáticamente
```

### Flujo C: Administración mensual de renta

```
1. Día 1 del mes → sistema envía recordatorio al inquilino (email + WhatsApp)
        ↓
2. Inquilino realiza pago
        ↓
3. Agente registra pago en CRM (con comprobante)
        ↓
4. Sistema genera recibo de pago (PDF automático)
        ↓
5. Recibo disponible en portal propietario + portal inquilino
        ↓
6. Propietario recibe transferencia (menos comisión Viviendo)
```

---

## 7. Base de Datos — Entidades Clave

```sql
-- Entidades principales y sus relaciones

properties (propiedades)
    id, code, type, status, owner_id, agent_id
    address, lat, lng, price, area
    title, description, amenities (JSON)
    created_at, updated_at

owners (propietarios)
    id, name, rfc, phone, email, bank_account
    portal_access: boolean, portal_password

prospects (prospectos/leads)
    id, name, phone, email, source
    budget, zone, type_needed, pet_friendly
    stage, priority, agent_id
    created_at, last_contact_at

tenants (inquilinos)
    id, name, curp, rfc, phone, email
    documents (JSON: {id_url, income_url, ...})
    created_from_prospect_id (FK → prospects)

contracts (contratos)
    id, property_id, tenant_id, owner_id
    start_date, end_date
    monthly_amount, deposit
    annual_increase_pct
    status, document_url

payments (pagos)
    id, contract_id, period_month, period_year
    expected_amount, paid_amount
    paid_at, method, voucher_url
    registered_by

portal_publications (publicaciones en portales)
    id, property_id, portal_name
    external_id (ID en el portal externo)
    status: [active, paused, error, unpublished]
    last_sync_at, sync_log

maintenance_tickets (mantenimiento)
    id, property_id, reported_by
    category, description, priority, status
    assigned_to, cost, paid_by
    created_at, resolved_at

activities (actividades CRM)
    id, prospect_id, agent_id
    type: [call, email, whatsapp, visit, note]
    result, notes, next_action_date
    created_at
```

---

## 8. Integraciones Externas

| Integración | Propósito | Prioridad |
|---|---|:---:|
| **Mercado Libre API** | Publicación y actualización de inmuebles | 🔴 Alta |
| **WhatsApp Business API** | Notificaciones y seguimiento a leads/inquilinos | 🔴 Alta |
| **Google Maps API** | Geolocalización y mapa de propiedades | 🔴 Alta |
| **Email (SMTP / SendGrid)** | Notificaciones automáticas | 🔴 Alta |
| **Google Calendar API** | Sincronización de visitas agendadas | 🟡 Media |
| **Vivanuncios / Lamudi API** | Publicación multiportal | 🟡 Media |
| **Firma electrónica (Mifiel/Docusign)** | Firma digital de contratos | 🟡 Media |
| **Pasarela de pagos (Stripe/OpenPay)** | Pagos de renta en línea | 🟡 Media |
| **Facebook Marketplace** | Publicación semi-automática | 🟢 Baja |
| **Cloudinary** | Almacenamiento y optimización de imágenes | 🟡 Media |

---

## 9. Diferenciadores vs Wasi

| Funcionalidad | Wasi | Viviendo CRM (propio) |
|---|:---:|:---:|
| Publicación multiportal | ✅ | ✅ (construido a medida) |
| CRM con pipeline | ✅ | ✅ (personalizado para renta) |
| Portal propietario | ✅ | ✅ con estado de cuenta MXN |
| Portal inquilino | Básico | ✅ con pagos y tickets |
| Módulo de cobranza | ❌ | ✅ |
| Mantenimiento y tickets | ❌ | ✅ |
| Contratos con alertas | Parcial | ✅ con firma electrónica |
| WhatsApp automatizado | ❌ | ✅ |
| Personalización total | ❌ (SaaS genérico) | ✅ (100% a medida) |
| Costo mensual recurrente | $200-500 USD/mes | Costo propio (sin renta) |
| Datos propios de la empresa | ❌ (en servidores de Wasi) | ✅ (servidor propio) |

---

## 10. Stack Tecnológico Sugerido

```
BACKEND
├── PHP 8.3 / Laravel 11
├── MySQL 8.0
├── Redis (caché + colas)
└── Laravel Horizon (colas para sincronización de portales)

FRONTEND / ADMIN
├── Livewire 3 (dinamismo sin API)
├── FilamentPHP 3 (panel admin)
├── Tailwind CSS + Alpine.js
└── Chart.js (gráficas del dashboard)

PORTALES EXTERNOS
├── Laravel Sanctum (auth API)
├── Portal propietario: Blade + Tailwind (simple)
└── Portal inquilino: Blade + Tailwind

INFRAESTRUCTURA
├── Servidor: DigitalOcean / AWS / Hetzner (VPS)
├── Almacenamiento: S3 / Cloudinary (fotos)
├── Email: Mailgun / SendGrid
└── Dominio + SSL: Cloudflare

HERRAMIENTAS DE DESARROLLO
├── GitHub + CI/CD
└── Laravel Forge (deployment)
```

---

## 11. Fases de Desarrollo

### FASE 1 — MVP Core (8-10 semanas)
```
✅ Autenticación y roles
✅ Módulo Propiedades (CRUD completo + fotos)
✅ Publicación en portal web propio
✅ Módulo CRM Leads (Pipeline Kanban)
✅ Módulo Propietarios
✅ Dashboard básico con KPIs
```

### FASE 2 — Operaciones (6-8 semanas)
```
🔄 Módulo Inquilinos + Contratos
🔄 Módulo Pagos y Cobranza
🔄 Alertas automáticas (email + WhatsApp)
🔄 Portal Propietario (lectura)
🔄 Portal Inquilino (pagos + tickets)
```

### FASE 3 — Publicación Multiportal (4-6 semanas)
```
🔄 Integración Mercado Libre API
🔄 Integración Vivanuncios
🔄 Dashboard de publicaciones
🔄 Sincronización automática de cambios
```

### FASE 4 — Inteligencia y Automatización (4-6 semanas)
```
🔄 Módulo Mantenimiento
🔄 Reportes avanzados (PDF exportable)
🔄 Firma electrónica en contratos
🔄 Pagos en línea (inquilinos)
🔄 App móvil básica (PWA)
```

---

## 📋 Checklist de Inicio de Proyecto

- [ ] Definir dominio y hosting del CRM
- [ ] Obtener credenciales API de Mercado Libre (Inmuebles)
- [ ] Definir templates de email (bienvenida, recordatorio de pago, vencimiento)
- [ ] Recopilar toda la información de propiedades actuales para importar
- [ ] Definir proceso interno de validación antes de publicar propiedad
- [ ] Decidir pasarela de pagos (Stripe vs OpenPay vs Conekta)
- [ ] Definir proveedor de firma electrónica (Mifiel recomendado para MX)
- [ ] Configurar WhatsApp Business API (Meta Business Manager)
- [ ] Diseñar manual de uso para agentes (capacitación)

---

*Documento generado para: Viviendo Grupo Inmobiliario*
*Versión: 1.0 | Fecha: Julio 2026*
*Uso interno — Confidencial*
