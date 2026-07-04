# 🎨 DISEÑO DE INTERFAZ: ESCÁNER CON SOLUCIONES

**Especificación de UI/UX para las nuevas funcionalidades**

---

## 1. FLUJO DE AUTENTICACIÓN

### 1.1 Página de Registro

```
┌─────────────────────────────────────────────────────┐
│                   SAFE SCAN PRO                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  Crear Nueva Cuenta                          │  │
│  ├──────────────────────────────────────────────┤  │
│  │                                              │  │
│  │  Email                                       │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │ user@example.com                     │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  Usuario                                     │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │ john_doe                             │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  Contraseña (min 8 caracteres)              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │ ••••••••••••••                       │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │  📋 Debe contener: Mayús, minús, números   │  │
│  │                                              │  │
│  │  Confirmar Contraseña                       │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │ ••••••••••••••                       │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │         REGISTRARSE                  │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  ¿Ya tienes cuenta? Inicia Sesión →        │  │
│  │                                              │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 1.2 Dashboard Principal (Después de Login)

```
┌─────────────────────────────────────────────────────────────────┐
│  Safe Scan Pro          🔍 Buscar    ⚙️  Perfil  🚪 Logout     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Bienvenido, John! 👋                    Última sesión: Hoy    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                          ESTADÍSTICAS NUEVAS ✨               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ 📊      │  │ 👥      │  │ 📈      │  │ 🎯      │       │
│  │ Total   │  │ Hoy     │  │ Semana  │  │ Mes     │       │
│  │ 1,523   │  │ 45      │  │ +12%    │  │ 320     │       │
│  │ Usuarios│  │ Nuevos  │  │ Cambio  │  │ Nuevos  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
│  REGISTROS ÚLTIMOS 30 DÍAS (Gráfico interactivo)             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │           ╭─╮                              ╱╲          │  │
│  │         ╭─╯  ╰─╮                        ╱    ╲        │  │
│  │       ╭─╯       ╰─╮  ╭─╮             ╱        ╲      │  │
│  │     ╭─╯           ╰─╯  ╰────────────╱          ╰─    │  │
│  │   ╱│                                                  │  │
│  │  Jun1  Jun5  Jun10  Jun15  Jun20  Jun25  Jun30       │  │
│  │                                                        │  │
│  │  Click para detalles | Descargar CSV | Compartir     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  MIS ESCANEOS RECIENTES                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Escaneados: example.com              Hoy 10:30 AM │        │
│  │ Status: ✅ Completado  │  3 Vulnerabilidades    │        │
│  │ [Ver Soluciones] [Descargar] [Exportar]          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Escaneados: app.mysite.com           Ayer 3:45 PM │        │
│  │ Status: ✅ Completado  │  1 Vulnerabilidad     │        │
│  │ [Ver Soluciones] [Descargar] [Exportar]          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  ESCANEAR NUEVA URL                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  URL:  ┌──────────────────────────────────────────────┐        │
│        │ https://mi-sitio-a-escanear.com            │        │
│        └──────────────────────────────────────────────┘        │
│                                                                 │
│  Módulos:  ☑ XSS   ☑ SQL Injection  ☑ Headers                │
│            ☑ CSRF  ☑ Open Redirect  ☑ Info Disclosure       │
│                                                                 │
│  Profundidad: ▯ 1   ▯ 2   ●●● 3    Timeout: 10 seg           │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐        │
│  │  🔍 INICIAR ESCANEO                              │        │
│  └──────────────────────────────────────────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. RESULTADOS DE ESCANEO CON SOLUCIONES (NUEVA FUNCIONALIDAD)

### 2.1 Vista de Pestañas (Nuevo)

```
┌─────────────────────────────────────────────────────────────────┐
│  Escaneo: example.com  (Completado: 2026-06-05 10:30)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [ 📋 Resumen ]  [ 🔧 Soluciones NUEVA ]  [ 📊 Detalles ]   │
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  VULNERABILIDADES ENCONTRADAS: 3                              │
│                                                                 │
│  🔴 CRÍTICA (0)    🔴 ALTA (3)    🟡 MEDIA (0)    🟢 BAJA (0) │
│                                                                 │
│  Resumen de hallazgos:                                         │
│  • Missing X-Frame-Options Header                             │
│  • Missing Content-Security-Policy Header                     │
│  • Información de servidor expuesta                           │
│                                                                 │
│  [DESCARGAR REPORTE PDF]  [EXPORTAR JSON]  [COMPARTIR]       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.2 Pestaña de SOLUCIONES (Completamente Nueva ✨)

```
┌─────────────────────────────────────────────────────────────────┐
│  Escaneo: example.com  (Completado: 2026-06-05 10:30)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [ 📋 Resumen ]  [ 🔧 Soluciones ]  [ 📊 Detalles ]          │
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  🔍 FILTROS:  [Severidad ▼] [Stack ▼] [Estado ▼] [Buscar...]│
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ SOLUCIÓN #1: Missing X-Frame-Options Header                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔴 Severidad: ALTA  │  CWE: CWE-1021  │  Tiempo: 5 minutos   │
│                                                                 │
│  📋 DESCRIPCIÓN:                                               │
│  X-Frame-Options header is missing, allowing clickjacking     │
│  attacks. Attackers can embed your site in an iframe on       │
│  malicious websites to trick users.                           │
│                                                                 │
│  ⚠️  IMPACTO:                                                  │
│  Security vulnerability that affects user trust and data.     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ 💔 CÓDIGO VULNERABLE:                               │     │
│  ├──────────────────────────────────────────────────────┤     │
│  │                                                      │     │
│  │ // Default Node.js/Express - MISSING HEADER        │     │
│  │ app.get('/', (req, res) => {                        │     │
│  │   res.setHeader('Content-Type', 'text/html');      │     │
│  │   res.send('<h1>Hello World</h1>');                │     │
│  │ });                                                 │     │
│  │                                                      │     │
│  │ [COPIAR CÓDIGO] [VER EN CONTEXTO]                  │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ ✅ CÓDIGO SEGURO:                                   │     │
│  ├──────────────────────────────────────────────────────┤     │
│  │                                                      │     │
│  │ // Add X-Frame-Options header                      │     │
│  │ app.use((req, res, next) => {                       │     │
│  │   res.setHeader('X-Frame-Options', 'DENY');        │     │
│  │   next();                                           │     │
│  │ });                                                 │     │
│  │                                                      │     │
│  │ app.get('/', (req, res) => {                        │     │
│  │   res.send('<h1>Hello World</h1>');                │     │
│  │ });                                                 │     │
│  │                                                      │     │
│  │ [COPIAR CÓDIGO] [COPIAR TODO] [DESCARGAR FILE]     │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  📚 PASOS PARA ARREGLARLO:                                    │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ 1️⃣  ELIGE TU OPCIÓN                                │     │
│  │     □ DENY - Rechazar framing completamente        │     │
│  │     □ SAMEORIGIN - Permitir solo desde mismo sitio │     │
│  │     □ ALLOW-FROM - Permitir desde URL específica   │     │
│  │                                                      │     │
│  │ 2️⃣  IMPLEMENTA EL CÓDIGO                           │     │
│  │     Reemplaza el código vulnerable con el seguro   │     │
│  │     en tu aplicación                               │     │
│  │                                                      │     │
│  │ 3️⃣  VERIFICA LA CORRECCIÓN                         │     │
│  │     Ejecuta en terminal:                           │     │
│  │     curl -I https://tu-sitio.com | grep X-Frame   │     │
│  │     Deberías ver: X-Frame-Options: DENY            │     │
│  │                                                      │     │
│  │ 4️⃣  REDESPLIEGA                                    │     │
│  │     Despliega los cambios a producción             │     │
│  │                                                      │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  💡 MEJORES PRÁCTICAS:                                        │
│  • Usa DENY a menos que necesites framing específicamente    │
│  • Combina con Content-Security-Policy para defensa en       │
│    profundidad                                                │
│  • Prueba en todos tus ambientes (dev, staging, prod)        │
│                                                                 │
│  🔗 REFERENCIAS:                                              │
│  • 📖 OWASP Clickjacking Prevention Cheat Sheet             │
│  • 🌐 MDN: X-Frame-Options Header                           │
│  • 🎯 PortSwigger: Clickjacking Techniques                  │
│                                                                 │
│  🏷️  TAGS: [security-headers] [clickjacking] [HIGH] [FAST]  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ ✅ MARCAR COMO ARREGLADO    [VOLVER A ESCANEAR]    │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ SOLUCIÓN #2: Missing Content-Security-Policy Header           │
├─────────────────────────────────────────────────────────────────┤
│ (Similar formato a arriba)                                      │
│                                                                 │
│  🔴 Severidad: ALTA  │  CWE: CWE-693  │  Tiempo: 30 minutos   │
│                                                                 │
│  [Ver solución completa...]                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. MODAL DE SELECCIÓN DE STACK (NUEVO)

```
┌──────────────────────────────────────────────────────────────┐
│  ¿Qué tecnología usas en tu backend?                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ◯  Node.js / Express                                       │
│  ◯  Python / Flask                                          │
│  ◯  Python / Django                                         │
│  ◯  PHP                                                     │
│  ◯  Java / Spring Boot                                      │
│  ◯  .NET / C#                                               │
│  ◯  Go                                                      │
│  ◯  Nginx / Apache (Web Server)                             │
│  ◯  Otro:  ┌──────────────────────┐                        │
│            │_____________________│                         │
│                                                              │
│  💡 Mostraremos ejemplos de código en tu tecnología         │
│                                                              │
│  ┌──────────────┐           ┌──────────────┐              │
│  │  CANCELAR    │           │   CONTINUAR  │              │
│  └──────────────┘           └──────────────┘              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. CARD DE VULNERABILIDAD EXPANDIDA (Versión Móvil)

```
╔═════════════════════════════════════════╗
║   🔴 Missing X-Frame-Options            ║
║   Severity: ALTA                        ║
║   Time to fix: 5 min                    ║
╠═════════════════════════════════════════╣
║                                         ║
║  PROBLEMA:                              ║
║  Clickjacking attacks possible          ║
║                                         ║
║  ┌──────────────────────────────────┐   ║
║  │ ❌ Vulnerable:                   │   ║
║  │ res.setHeader('Content-Type'...) │   ║
║  │                                  │   ║
║  │ ✅ Fix:                          │   ║
║  │ res.setHeader('X-Frame-Options.. │   ║
║  │                                  │   ║
║  │ [TAP TO EXPAND] [COPY] [SHARE]   │   ║
║  └──────────────────────────────────┘   ║
║                                         ║
║  📖 Learn More | 🔗 References          ║
║                                         ║
║  ✅ Mark Fixed | 🔄 Update              ║
║                                         ║
╚═════════════════════════════════════════╝
```

---

## 5. EXPORTACIÓN DE REPORTE (NUEVO)

```
┌─────────────────────────────────────────────────────────────────┐
│  [📥 EXPORTAR REPORTE]                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Formato:                                                       │
│  ◯ PDF (Reporte profesional con soluciones)  RECOMENDADO ⭐   │
│  ◯ JSON (Para integración con herramientas)                   │
│  ◯ CSV (Para hojas de cálculo)                                │
│  ◯ HTML (Página interactiva compartible)                      │
│                                                                 │
│  Incluir:                                                       │
│  ☑ Vulnerabilidades encontradas                              │
│  ☑ Soluciones y código                                       │
│  ☑ Pasos de remediación                                      │
│  ☑ Referencias y mejores prácticas                           │
│  ☑ Timestamp y URL escaneada                                 │
│  ☑ Tu logo/marca                                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │           📥 DESCARGAR REPORTE                       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  O compartir:                                                   │
│  ┌──────────────────────────────────────────────────────┐     │
│  │  🔗 Enlace Compartible (vence en 7 días):           │     │
│  │  https://safescan.pro/report/abc123def              │     │
│  │                                                      │     │
│  │  [COPIAR] [ENVIAR EMAIL] [COMPARTIR EN SLACK]       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. VISTA DE PROGRESO DURANTE ESCANEO

```
┌─────────────────────────────────────────────────────────────────┐
│  Escaneando: example.com                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Progreso Overall: ▓▓▓▓▓▓░░░░░░░░░░░ 40%  3/7 módulos        │
│                                                                 │
│  ✅ Headers Check      [Completado]                            │
│  ✅ CSRF Detection      [Completado]                            │
│  ⏳ XSS Vulnerability   [Escaneando...]  50%                    │
│  ⏸️  SQL Injection       [En espera]                            │
│  ⏸️  Open Redirect      [En espera]                            │
│  ⏸️  Info Disclosure    [En espera]                            │
│                                                                 │
│  Tiempo estimado restante: 45 segundos                         │
│                                                                 │
│  Última acción: Probando XSS en parámetro 'id'                │
│                                                                 │
│  ┌──────────────────────────┐                                 │
│  │  ⏹️  CANCELAR ESCANEO     │                                 │
│  └──────────────────────────┘                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. NOTIFICACIONES Y ALERTAS (NUEVO)

### Sistema de Alertas

```
┌─────────────────────────────────────────────────┐
│ 🔴 CRÍTICO: Vulnerabilidad SQL Injection       │
│ Tu sitio example.com tiene vulns CRÍTICAS      │
│ [VER DETALLES] [DESCARTAR]                     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ ✅ BUENAS NOTICIAS: example.com está seguro    │
│ Ninguna vulnerabilidad detectada                │
│ Última verificación: Hace 2 días               │
│ [ESCANEAR DE NUEVO] [DESCARTAR]                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 📬 EMAIL SEMANAL: Resumen de seguridad         │
│ 3 nuevos escaneos esta semana                   │
│ [VER RESUMEN] [CONFIGURAR ALERTAS]             │
└─────────────────────────────────────────────────┘
```

---

## 8. TABLA COMPARATIVA: RESPUESTA API

### Endpoint: `GET /api/scans/123`

**Antes (❌ Sin soluciones):**

```
Status: 200
Size: ~2 KB
Time to fix: Unknown
```

**Después (✅ Con soluciones):**

```
Status: 200
Size: ~50 KB (con ejemplos de código)
Time to fix: ~30-45 minutos (claro y documentado)
Users who fixed: +500% (estimado)
```

---

## 9. RESPONSIVE DESIGN CONSIDERATIONS

### Desktop (1920x1080)

```
Full width layout
Side-by-side code comparison
Expandable sections
All details visible
```

### Tablet (768x1024)

```
Stacked layout
Tabs for code switching
Accordion for details
Scrollable solutions
```

### Mobile (375x667)

```
Card-based layout
One solution per screen
Swipe between vulnerable/secure code
Copy-paste friendly
Minimal but complete
```

---

## 10. TABLA DE COMPONENTES A CREAR

| Componente       | Archivo                | Líneas | Reutilizable |
| ---------------- | ---------------------- | ------ | ------------ |
| SolutionCard     | `SolutionCard.tsx`     | 150    | ✅ Sí        |
| SolutionSteps    | `SolutionSteps.tsx`    | 100    | ✅ Sí        |
| CodeComparison   | `CodeComparison.tsx`   | 120    | ✅ Sí        |
| SolutionModal    | `SolutionModal.tsx`    | 200    | ✅ Sí        |
| FilterBar        | `FilterBar.tsx`        | 80     | ✅ Sí        |
| StackSelector    | `StackSelector.tsx`    | 100    | ✅ Sí        |
| StatisticsWidget | `StatisticsWidget.tsx` | 120    | ✅ Sí        |
| AuthContext      | `AuthContext.tsx`      | 100    | ✅ Sí        |

---

## ✅ CONCLUSIÓN: DISEÑO DE UX

| Aspecto   | Score      | Notas                  |
| --------- | ---------- | ---------------------- |
| Intuitivo | ⭐⭐⭐⭐⭐ | Claro y obvio          |
| Completo  | ⭐⭐⭐⭐⭐ | Toda la info necesaria |
| Rápido    | ⭐⭐⭐⭐   | Acciones en 2 clicks   |
| Bonito    | ⭐⭐⭐⭐⭐ | Moderno y limpio       |
| Móvil     | ⭐⭐⭐⭐   | Responsivo             |

---

**El diseño es totalmente viable y mejoraría enormemente la experiencia del usuario.** ✨
