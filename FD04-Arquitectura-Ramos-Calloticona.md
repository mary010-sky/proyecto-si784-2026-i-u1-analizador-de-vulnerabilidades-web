<center>

![./media/logo-upt.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Analizador de Vulnerabilidades Web — VulnScan Pro**

Curso: *Calidad y Pruebas de Software*

Docente: *Ing. Patrick Jose Cuadros Quiroga*

Integrantes:

**Ramos Loza, Mariela Estefany (2023077478)**

**Calloticona Chambilla, Marymar D. (2023076791)**

**Tacna – Perú**

**2026**

</center>

<div style="page-break-after: always;"></div>

---

**Analizador de Vulnerabilidades Web — VulnScan Pro**

Informe de Arquitectura de Software

Versión 1.0

| CONTROL DE VERSIONES |                  |                |              |            |                  |
|:--------------------:|:-----------------|:---------------|:-------------|:-----------|:-----------------|
| Versión              | Hecha por        | Revisada por   | Aprobada por | Fecha      | Motivo           |
| 1.0                  | M. Calloticona   | M. Ramos       |              | 12/04/2026 | Versión Original |
| 1.1                  | M. Ramos         | M. Calloticona |              | 19/04/2026 | Revisión diagramas y descripción de capas |

<div style="page-break-after: always;"></div>

---

## ÍNDICE GENERAL

1. [Introducción](#1-introducción)  
   1.1. Propósito  
   1.2. Alcance  
   1.3. Definiciones y Abreviaturas  
   1.4. Referencias  

2. [Representación Arquitectónica](#2-representación-arquitectónica)  
   2.1. Estilo Arquitectónico  
   2.2. Restricciones Arquitectónicas  

3. [Metas y Restricciones de la Arquitectura](#3-metas-y-restricciones-de-la-arquitectura)  

4. [Vista de Casos de Uso](#4-vista-de-casos-de-uso)  

5. [Vista Lógica](#5-vista-lógica)  
   5.1. Diagrama de Componentes  
   5.2. Descripción de Capas  
   5.3. Diagrama de Clases (Modelo de Datos)  

6. [Vista de Procesos](#6-vista-de-procesos)  
   6.1. Flujo de Escaneo  
   6.2. Flujo de Autenticación  

7. [Vista de Despliegue](#7-vista-de-despliegue)  
   7.1. Arquitectura de Infraestructura  
   7.2. Configuración de Nginx  
   7.3. Configuración del Servicio systemd  

8. [Vista de Implementación](#8-vista-de-implementación)  
   8.1. Estructura de Archivos del Backend  
   8.2. Estructura de Archivos del Frontend  

9. [Decisiones Arquitectónicas](#9-decisiones-arquitectónicas)  

10. [Patrones de Diseño Aplicados](#10-patrones-de-diseño-aplicados)  

[Conclusiones](#conclusiones)  

<div style="page-break-after: always;"></div>

---

## Informe de Arquitectura de Software

---

## 1. Introducción

### 1.1. Propósito

El presente documento describe la arquitectura de software del sistema **VulnScan Pro**, una plataforma DAST (Dynamic Application Security Testing) con inteligencia artificial. Su propósito es comunicar las decisiones arquitectónicas significativas tomadas durante el diseño del sistema, proveer una guía para el equipo de desarrollo y futuros mantenedores, y justificar la elección de componentes, patrones y tecnologías utilizadas.

El documento sigue el modelo de vistas arquitectónicas **4+1** (Lógica, Proceso, Despliegue, Implementación y Casos de Uso) adaptado para el alcance académico del proyecto.

### 1.2. Alcance

La arquitectura cubre:
- **Backend:** API REST con FastAPI (Python) y MySQL
- **Frontend:** SPA con Next.js 16 (React + TypeScript)
- **Motor de escaneo:** 13 módulos de análisis de vulnerabilidades
- **Integración IA:** DeepSeek AI API
- **Infraestructura:** VPS Linux con Nginx, systemd, PM2 y UFW

### 1.3. Definiciones y Abreviaturas

| **Término** | **Definición** |
|:------------|:---------------|
| SPA | Single Page Application |
| ORM | Object-Relational Mapper |
| REST | Representational State Transfer |
| JWT | JSON Web Token |
| ASGI | Asynchronous Server Gateway Interface |
| WSGI | Web Server Gateway Interface |
| CDN | Content Delivery Network |
| SSL | Secure Sockets Layer |
| VPS | Virtual Private Server |
| PM2 | Process Manager 2 (Node.js) |

### 1.4. Referencias

- FastAPI Architecture Guide — https://fastapi.tiangolo.com/advanced/
- Next.js App Router — https://nextjs.org/docs/app
- SQLAlchemy 2.0 — https://docs.sqlalchemy.org/en/20/
- Gunicorn Deployment — https://gunicorn.org/
- Nginx Configuration — https://nginx.org/en/docs/

<div style="page-break-after: always;"></div>

---

## 2. Representación Arquitectónica

### 2.1. Estilo Arquitectónico

**VulnScan Pro** adopta una arquitectura de **3 capas cliente-servidor** con **separación de responsabilidades** clara:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE PRESENTACIÓN                     │
│         Next.js 16 + TypeScript + TailwindCSS (Puerto 3000)     │
│   Dashboard SOC │ Scanner Page │ Admin Panel │ Scan Detail      │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTPS / REST API (JSON)
                                │ via Nginx Proxy
┌───────────────────────────────▼─────────────────────────────────┐
│                         CAPA DE NEGOCIO                         │
│      FastAPI + Python + Gunicorn + Uvicorn (Puerto 8000)        │
│   Auth Routes │ Scan Routes │ Admin Routes │ Report Routes      │
│         Scanner Engine │ AI Service │ Models                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │ SQLAlchemy ORM
┌───────────────────────────────▼─────────────────────────────────┐
│                          CAPA DE DATOS                          │
│                   MySQL 8.0 (Puerto 3306)                       │
│  users │ scans │ vulnerabilities │ audit_logs │ user_sessions   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      SERVICIO EXTERNO IA                        │
│              DeepSeek AI API (api.deepseek.com)                 │
│              (con fallback local si no disponible)              │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Restricciones Arquitectónicas

1. **No Docker:** El sistema se despliega directamente en el sistema operativo (bare metal virtualizado en VPS).
2. **MySQL nativo:** La capa de datos usa MySQL 8.0 con PyMySQL como driver; no se permite SQLite ni PostgreSQL.
3. **Asincronismo limitado:** FastAPI es asíncrono pero el motor de escaneo (`scanner.py`) usa `requests` (síncrono) y se ejecuta en hilos mediante `BackgroundTasks`.
4. **IA como servicio externo:** DeepSeek es un servicio externo; la arquitectura debe funcionar completamente sin él (fallback local).
5. **Monolito modular:** El backend es un único proceso FastAPI con routers separados por dominio; no hay microservicios.

<div style="page-break-after: always;"></div>

---

## 3. Metas y Restricciones de la Arquitectura

| **Meta** | **Decisión Arquitectónica** |
|:---------|:---------------------------|
| Alta cohesión / bajo acoplamiento | Separación en módulos: `auth.py`, `scanner.py`, `ai_service.py`, `database.py`, `models.py` con responsabilidades únicas. |
| Escalabilidad del scanner | Cada módulo de escaneo es una función independiente. Añadir un módulo nuevo = añadir una función en `scanner.py` y registrarla en `run_full_scan()`. |
| Seguridad por defecto | JWT obligatorio en todos los endpoints salvo `/register`, `/login`, `/health`. Headers de seguridad aplicados globalmente por middleware. |
| Disponibilidad | Systemd con `Restart=always` + Nginx como proxy que maneja reconexiones. Pool de conexiones MySQL con `pool_pre_ping=True`. |
| Facilidad de despliegue | Script `deploy.sh` que automatiza toda la instalación. `.env.example` con todas las variables documentadas. |
| Transparencia para auditoría | Audit logs en base de datos para todas las operaciones de autenticación y administración. |

<div style="page-break-after: always;"></div>

---

## 4. Vista de Casos de Uso

Los casos de uso arquitectónicamente significativos que condicionan las decisiones de diseño son:

| **Caso de Uso** | **Impacto Arquitectónico** |
|:----------------|:--------------------------|
| UC-03: Iniciar Escaneo | Requiere ejecución asíncrona en segundo plano (BackgroundTasks + threading) para no bloquear la API durante minutos de escaneo. |
| UC-04: Ver Resultados en Tiempo Real | Requiere polling desde el frontend (cada 3 s) al endpoint `GET /api/scans/{id}` hasta que el estado cambie a `completed`. |
| UC-05: Exportar Reporte PDF | Requiere WeasyPrint como dependencia del sistema operativo o fallback a HTML puro. |
| UC-06: Gestionar Usuarios (Admin) | Requiere sistema de roles con `require_role()` como FastAPI Dependency aplicada por endpoint. |
| Análisis IA por vulnerabilidad | Requiere llamada HTTP síncrona a DeepSeek API con timeout controlado y fallback local para cada vulnerabilidad. |

<div style="page-break-after: always;"></div>

---

## 5. Vista Lógica

### 5.1. Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND (FastAPI)                        │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ auth_routes │  │ scan_routes │  │admin_routes │            │
│  │  /api/auth/ │  │ /api/scans/ │  │ /api/admin/ │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                │                │                    │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐            │
│  │   auth.py   │  │  scanner.py │  │ ai_service  │            │
│  │ JWT / bcrypt│  │ 13 módulos  │  │ deepseek.py │            │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘            │
│         │                │                                     │
│  ┌──────┴──────────────────┴─────────────┐                     │
│  │              models.py                │                     │
│  │  User │ Scan │ Vulnerability │ etc.   │                     │
│  └──────────────────┬────────────────────┘                     │
│                     │                                          │
│  ┌──────────────────┴────────────────────┐                     │
│  │             database.py               │                     │
│  │   SQLAlchemy Engine + SessionLocal    │                     │
│  │   QueuePool (10 conn, 20 overflow)    │                     │
│  └───────────────────────────────────────┘                     │
│                                                                 │
│  ┌─────────────────┐  ┌────────────────────┐                   │
│  │ report_routes   │  │ solutions_routes   │                   │
│  │ /api/reports/   │  │ /api/solutions/    │                   │
│  └─────────────────┘  └────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                        │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │/dashboard│  │/scanner  │  │/scanner  │  │    /admin     │  │
│  │  page.tsx│  │ page.tsx │  │  [id]/   │  │    page.tsx   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───────┬───────┘  │
│       │             │             │                │           │
│  ┌────┴─────────────┴─────────────┴────────────────┴───────┐   │
│  │                       lib/api.ts                        │   │
│  │         Centraliza todas las llamadas a la API          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │  hooks/useAuth  │  │   components/   │                      │
│  │  (JWT + estado) │  │ Navbar │ Badges │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Descripción de Capas

#### Capa de Presentación (Frontend)

| **Componente** | **Responsabilidad** |
|:---------------|:--------------------|
| `app/page.tsx` | Redirige a `/dashboard` si autenticado, o a `/login`. |
| `app/dashboard/page.tsx` | Dashboard SOC: estadísticas, gráficos (Chart.js), escaneos recientes, estado del sistema. |
| `app/scanner/page.tsx` | Escáner interactivo: selección de módulos, configuración avanzada, lista de escaneos con polling en tiempo real. |
| `app/scanner/[id]/page.tsx` | Detalle del escaneo: vulnerabilidades con análisis IA, tecnologías, URLs crawleadas, reportes. |
| `app/admin/page.tsx` | Panel admin: tabla de usuarios con acciones inline, logs de auditoría. |
| `app/login/page.tsx` | Formulario de inicio de sesión con feedback de errores. |
| `app/register/page.tsx` | Formulario de registro con validación de contraseña en cliente. |
| `lib/api.ts` | Cliente API centralizado: todas las llamadas HTTP al backend, manejo de errores, tipos TypeScript. |
| `hooks/useAuth.ts` | Estado global de autenticación: usuario actual, login, logout, redirección automática. |
| `components/Navbar.tsx` | Barra de navegación fija con links filtrados por rol del usuario. |
| `components/SeverityBadge.tsx` | Componentes reutilizables: SeverityBadge (chip) y SeverityBar (barra proporcional). |

#### Capa de Negocio (Backend)

| **Componente** | **Responsabilidad** |
|:---------------|:--------------------|
| `main.py` | Punto de entrada FastAPI: lifespan (init_db), CORS, middleware de headers de seguridad, registro de routers, health check, lista de módulos. |
| `auth.py` | Lógica de JWT: `create_access_token()`, `get_current_user()`, `require_role(*roles)`. |
| `database.py` | Configuración del engine SQLAlchemy con MySQL, QueuePool, `SessionLocal`, `get_db()` como dependencia, `init_db()`. |
| `models.py` | 7 modelos SQLAlchemy: User, UserSession, Scan, Vulnerability, AuditLog, Report, PasswordReset. |
| `scanner.py` | Motor de escaneo: 13 funciones independientes + `run_full_scan()` que las orquesta. Usa `requests` y `BeautifulSoup4`. |
| `ai_service.py` | Integración DeepSeek: `analyze_vulnerability()`, `generate_scan_report()`, `_fallback_analysis()`, clase `AIService`. |
| `routes/auth_routes.py` | Endpoints de autenticación: register, login, me, change-password, forgot-password, reset-password. |
| `routes/scan_routes.py` | Endpoints de escaneos: crear, listar, obtener, eliminar, marcar falso positivo. Lanza `_run_scan_background()` como BackgroundTask. |
| `routes/admin_routes.py` | Endpoints de administración (solo `admin`): dashboard, usuarios CRUD, logs de auditoría. |
| `routes/report_routes.py` | Endpoints de reportes: JSON, HTML, PDF con autenticación por token en query string. |
| `solutions_routes.py` | Endpoints de soluciones IA: generación de solución por tipo de vulnerabilidad y stack. |

#### Capa de Datos

| **Tabla** | **Campos Principales** | **Descripción** |
|:----------|:----------------------|:----------------|
| `users` | id, username, email, hashed_password, role, is_active, failed_login_attempts, locked_until, last_login, last_login_ip | Usuarios del sistema con control de acceso y protección anti-fuerza bruta. |
| `user_sessions` | id, user_id, token_jti, ip_address, user_agent, expires_at | Sesiones JWT activas para invalidación remota. |
| `scans` | id, user_id, target_url, status, modules(JSON), total_vulns, critical/high/medium/low_count, technologies(JSON), crawled_urls(JSON), scan_duration, result_summary(JSON), error_message | Registro de escaneos con metadatos completos. |
| `vulnerabilities` | id, scan_id, vuln_type, severity(ENUM), title, description, endpoint, payload, evidence, risk, solution, ai_analysis(JSON), cwe_id, cvss_score, false_positive | Vulnerabilidades detectadas con análisis IA embebido. |
| `audit_logs` | id, user_id, action, ip_address, success, details(JSON), created_at | Registro de auditoría de todas las acciones de autenticación y administración. |
| `reports` | id, scan_id, format, filename, file_path, created_at | Registro de reportes generados y su ubicación en disco. |
| `password_resets` | id, user_id, token, expires_at, used | Tokens de recuperación de contraseña con expiración. |

### 5.3. Diagrama de Clases (Modelo de Datos)

```
┌──────────────┐         ┌──────────────────┐
│    User      │  1     *│   UserSession    │
│──────────────│─────────│──────────────────│
│ id: Integer  │         │ id: Integer      │
│ username: Str│         │ user_id: FK      │
│ email: Str   │         │ token_jti: Str   │
│ hashed_pwd   │         │ ip_address: Str  │
│ role: Enum   │         │ user_agent: Str  │
│ is_active    │         │ expires_at: DT   │
│ failed_login │         └──────────────────┘
│ locked_until │
│ last_login   │  1     *┌──────────────┐
│ last_login_ip│─────────│    Scan      │
└──────────────┘         │──────────────│
                         │ id: Integer  │
        1                │ user_id: FK  │
        │                │ target_url   │
        ▼ *              │ status: Enum │
┌──────────────┐         │ modules: JSON│
│  AuditLog    │         │ total_vulns  │
│──────────────│         │ critical_cnt │
│ id: Integer  │         │ high_count   │
│ user_id: FK  │         │ medium_count │
│ action: Str  │         │ low_count    │
│ ip_address   │         │ technologies │
│ success: Bool│         │ crawled_urls │
│ details: JSON│         │ scan_duration│
│ created_at   │         │ result_summary│
└──────────────┘         └──────┬───────┘
                                │ 1
                                │
                                ▼ *
                         ┌──────────────────┐
                         │  Vulnerability   │
                         │──────────────────│
                         │ id: Integer      │
                         │ scan_id: FK      │
                         │ vuln_type: Str   │
                         │ severity: Enum   │
                         │ title: Str       │
                         │ description: Str │
                         │ endpoint: Str    │
                         │ payload: Str     │
                         │ evidence: Str    │
                         │ risk: Str        │
                         │ solution: Str    │
                         │ ai_analysis: JSON│
                         │ cwe_id: Str      │
                         │ cvss_score: Float│
                         │ false_positive   │
                         └──────────────────┘
```

<div style="page-break-after: always;"></div>

---

## 6. Vista de Procesos

### 6.1. Flujo de Escaneo (Proceso Asíncrono)

```
Cliente (Frontend)                 FastAPI (Backend)              Scanner Engine
       │                                  │                              │
       │─── POST /api/scans/ ────────────►│                              │
       │    {url, modules, ...}           │                              │
       │                                 │ Crea scan (status=pending)    │
       │                                 │ en MySQL                      │
       │◄── {id: 42, status: "pending"} ──│                              │
       │                                 │                              │
       │  (cada 3 segundos)              │ BackgroundTask.add_task()     │
       │─── GET /api/scans/42 ──────────►│──────────────────────────────►│
       │◄── {status: "running"} ─────────│       run_full_scan()        │
       │                                 │       ├── check_headers()     │
       │─── GET /api/scans/42 ──────────►│       ├── check_ssl()        │
       │◄── {status: "running"} ─────────│       ├── check_sqli()       │
       │                                 │       ├── check_xss()        │
       │─── GET /api/scans/42 ──────────►│       ├── check_csrf()       │
       │◄── {status: "running"} ─────────│       ├── check_ssrf()       │
       │                                 │       ├── ...13 módulos       │
       │                                 │       │                       │
       │                                 │       ▼                       │
       │                                 │   Para cada vuln encontrada:  │
       │                                 │   ai_service.analyze_vuln()   │
       │                                 │   → DeepSeek API (o fallback) │
       │                                 │   → Guardar en MySQL          │
       │                                 │                               │
       │                                 │   Actualizar scan:            │
       │                                 │   status=completed            │
       │─── GET /api/scans/42 ──────────►│   counts, technologies, urls  │
       │◄── {status: "completed",  ──────│                               │
       │     vulnerabilities: [...]}     │                               │
       │                                 │                               │
```

### 6.2. Flujo de Autenticación

```
Cliente (Frontend)                 FastAPI (Backend)               MySQL
       │                                  │                           │
       │─── POST /api/auth/login ────────►│                           │
       │    {username, password}          │                           │
       │                                 │─── SELECT user ──────────►│
       │                                 │◄── user data ─────────────│
       │                                 │                           │
       │                                 │ ¿locked_until > ahora?    │
       │                                 │   → Error 423             │
       │                                 │                           │
       │                                 │ bcrypt.verify(pwd)        │
       │                                 │   → Fallo: failed_attempts+1
       │                                 │     Si >= 5: set locked_until
       │                                 │   → Éxito: failed_attempts=0
       │                                 │                           │
       │                                 │ Crear JWT con JTI único   │
       │                                 │─── INSERT user_session ──►│
       │                                 │─── INSERT audit_log ─────►│
       │◄── {access_token, role, ...} ───│                           │
       │                                 │                           │
       │  (requests siguientes)          │                           │
       │─── GET /api/auth/me ───────────►│                           │
       │    Authorization: Bearer <JWT>  │ Decodificar JWT           │
       │                                 │ Verificar JTI en sessions │
       │◄── {id, username, email, role}──│                           │
```

<div style="page-break-after: always;"></div>

---

## 7. Vista de Despliegue

### 7.1. Arquitectura de Infraestructura

```
Internet
   │
   │ HTTPS (443) / HTTP (80→redirect 443)
   ▼
┌──────────────────────────────────────────────────┐
│              VPS Linux Ubuntu 22.04               │
│           IP Pública: 149.34.48.176               │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │              Nginx 1.24                     │ │
│  │   - Rate limiting (3 zonas)                 │ │
│  │   - SSL termination (Let's Encrypt)         │ │
│  │   - Security headers                        │ │
│  │   - Gzip compression                        │ │
│  │   - Deny .env/.git/.sql files               │ │
│  └────────┬──────────────────────┬─────────────┘ │
│           │                      │               │
│           │ proxy_pass           │ proxy_pass    │
│           │ localhost:8000       │ localhost:3000│
│           ▼                      ▼               │
│  ┌──────────────────┐  ┌──────────────────────┐ │
│  │  FastAPI Backend │  │  Next.js Frontend    │ │
│  │  Gunicorn 4W     │  │  PM2 (cluster mode)  │ │
│  │  puerto 8000     │  │  puerto 3000         │ │
│  │  systemd service │  │  .next/standalone    │ │
│  └────────┬─────────┘  └──────────────────────┘ │
│           │                                      │
│           │ pymysql (3306)                       │
│           ▼                                      │
│  ┌──────────────────┐                            │
│  │   MySQL 8.0      │                            │
│  │  vulnscan_db     │                            │
│  │  usuario: vscan  │                            │
│  └──────────────────┘                            │
│                                                  │
│  UFW Firewall:                                   │
│  - 22 (SSH): ALLOW                               │
│  - 80 (HTTP): ALLOW                              │
│  - 443 (HTTPS): ALLOW                            │
│  - 3306 (MySQL): DENY (solo localhost)           │
│  - 8000 (FastAPI): DENY (solo localhost)         │
└──────────────────────────────────────────────────┘
              │
              │ HTTPS (api.deepseek.com)
              ▼
      DeepSeek AI API
      (Servicio externo)
```

### 7.2. Configuración de Nginx

Las zonas de rate limiting configuradas en Nginx:

| **Zona** | **Endpoint** | **Límite** | **Propósito** |
|:---------|:-------------|:----------:|:--------------|
| `api_limit` | `/api/` (general) | 10 req/s por IP | Proteger la API de scraping masivo |
| `login_limit` | `/api/auth/login` | 5 req/min por IP | Prevenir ataques de fuerza bruta desde la red |
| `scan_limit` | `/api/scans/` (POST) | 2 req/min por IP | Prevenir abuso del motor de escaneo |

Headers de seguridad aplicados por Nginx a todas las respuestas:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'; ...`

### 7.3. Configuración del Servicio systemd

El archivo `vulnscan-backend.service` define:

| **Directiva** | **Valor** | **Propósito** |
|:--------------|:----------|:--------------|
| `ExecStart` | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 main:app` | 4 workers ASGI en localhost solo |
| `Restart` | `always` | Reinicio automático ante fallos |
| `RestartSec` | `5` | Espera 5 seg antes de reiniciar |
| `NoNewPrivileges` | `yes` | El proceso no puede elevar privilegios |
| `PrivateTmp` | `yes` | Directorio /tmp aislado |
| `ProtectSystem` | `strict` | Sistema de archivos de solo lectura |

<div style="page-break-after: always;"></div>

---

## 8. Vista de Implementación

### 8.1. Estructura de Archivos del Backend

```
backend/
├── .env                    # Variables de entorno (no en repo)
├── .env.example            # Plantilla de variables
├── requirements.txt        # Dependencias Python
├── main.py                 # Punto de entrada FastAPI
├── database.py             # Engine MySQL, SessionLocal, init_db
├── models.py               # Modelos SQLAlchemy (7 tablas)
├── auth.py                 # JWT, bcrypt, require_role()
├── scanner.py              # Motor de escaneo (13 módulos)
├── ai_service.py           # Integración DeepSeek + AIService class
├── solutions_routes.py     # Rutas de soluciones IA
└── routes/
    ├── __init__.py
    ├── auth_routes.py      # /api/auth/*
    ├── scan_routes.py      # /api/scans/*
    ├── admin_routes.py     # /api/admin/*
    └── report_routes.py    # /api/reports/*
```

### 8.2. Estructura de Archivos del Frontend

```
frontend/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── src/
    ├── app/
    │   ├── layout.tsx              # Layout raíz con metadata
    │   ├── page.tsx                # Redirect → dashboard/login
    │   ├── login/page.tsx          # Formulario login
    │   ├── register/page.tsx       # Formulario registro
    │   ├── dashboard/page.tsx      # Dashboard SOC principal
    │   ├── scanner/
    │   │   ├── page.tsx            # Escáner interactivo
    │   │   └── [id]/page.tsx       # Detalle escaneo + vuln cards
    │   ├── admin/page.tsx          # Panel administración
    │   ├── solutions/page.tsx      # Generador de soluciones IA
    │   └── profile/page.tsx        # Perfil usuario
    ├── components/
    │   ├── Navbar.tsx              # Barra navegación con roles
    │   └── SeverityBadge.tsx       # SeverityBadge + SeverityBar
    ├── hooks/
    │   └── useAuth.ts              # Estado autenticación global
    └── lib/
        └── api.ts                  # Cliente API centralizado + tipos TS
```

<div style="page-break-after: always;"></div>

---

## 9. Decisiones Arquitectónicas

| **ID** | **Decisión** | **Alternativas consideradas** | **Justificación** |
|:-------|:-------------|:------------------------------|:------------------|
| DA-01 | FastAPI sobre Django REST Framework | Flask, Django REST, Express.js | FastAPI ofrece validación automática con Pydantic, documentación OpenAPI nativa, rendimiento ASGI y sintaxis moderna. Ideal para APIs con tipado estricto. |
| DA-02 | MySQL nativo sobre SQLite | SQLite (file), PostgreSQL | Requerimiento explícito del proyecto. MySQL es más adecuado para entornos de producción con múltiples usuarios concurrentes. |
| DA-03 | Next.js 16 (App Router) sobre React SPA puro | Create React App, Vite+React, Vue.js | Next.js provee SSR, optimización automática de imágenes, routing basado en archivos y mejor SEO. El App Router es el estándar actual. |
| DA-04 | BackgroundTasks + threading para escaneos | Celery + Redis, asyncio puro | Para el alcance académico, BackgroundTasks de FastAPI con hilos nativos es suficiente sin añadir infraestructura de colas. Celery requeriría Redis como broker adicional. |
| DA-05 | Polling cada 3 segundos para estado del escaneo | WebSockets, Server-Sent Events | Polling es más simple de implementar, no requiere mantener conexiones persistentes, y la latencia de 3 segundos es aceptable para escaneos de 30-120 segundos. |
| DA-06 | DeepSeek AI con fallback local | Solo DeepSeek, Solo local, GPT-4 | DeepSeek ofrece API compatible con OpenAI a menor costo. El fallback local garantiza que el sistema funcione aunque la API esté caída, mejorando la confiabilidad. |
| DA-07 | Monolito modular vs microservicios | Microservicios (scanner service, auth service) | Para el alcance académico, un monolito modular es más simple de desplegar, depurar y mantener. La separación en archivos por responsabilidad (`scanner.py`, `auth.py`, etc.) permite migrar a microservicios en el futuro sin refactorización mayor. |
| DA-08 | Nginx como proxy inverso | Apache, Caddy, despliegue directo | Nginx es el estándar para VPS Linux: alto rendimiento, configuración de rate limiting nativa, fácil configuración de SSL con Certbot, y excelente documentación. |
| DA-09 | JWT sobre sesiones en servidor | Session cookies + Redis, Auth0 | JWT es stateless y compatible con arquitecturas cliente-servidor separadas. Se almacena la tabla `user_sessions` para permitir revocación de tokens sin depender de Redis. |
| DA-10 | SQLAlchemy 2.0 como ORM | Raw SQL, Tortoise-ORM, Peewee | SQLAlchemy es el ORM Python más maduro y con mejor soporte para MySQL. La versión 2.0 simplifica el API con `Session.execute()` y mejora el tipado. |

<div style="page-break-after: always;"></div>

---

## 10. Patrones de Diseño Aplicados

| **Patrón** | **Aplicación en VulnScan Pro** | **Archivo** |
|:-----------|:-------------------------------|:------------|
| **Repository Pattern** | `get_db()` como FastAPI Dependency inyecta la sesión de base de datos en cada endpoint. Cada router recibe `db: Session = Depends(get_db)`. | `database.py`, todos los routers |
| **Strategy Pattern** | Cada módulo de escaneo es una estrategia independiente intercambiable. `run_full_scan()` selecciona qué módulos ejecutar según la lista `modules`. | `scanner.py` |
| **Decorator Pattern** | `@router.get(...)`, `@app.middleware(...)` y `Depends(require_role(...))` añaden comportamiento a los endpoints sin modificar la lógica principal. | `main.py`, todos los routers |
| **Dependency Injection** | FastAPI usa DI para `get_db()`, `get_current_user()`, `require_role()` — composición de dependencias en cadena. | `auth.py`, `database.py` |
| **Observer Pattern** | El frontend implementa polling periódico (cada 3 s) como mecanismo de observación del estado del escaneo, alternativa síncrona al patrón observer puro. | `scanner/page.tsx` |
| **Factory Pattern** | `create_access_token()` centraliza la creación de JWTs con todos los campos requeridos. `_fallback_analysis()` actúa como factory de análisis locales. | `auth.py`, `ai_service.py` |
| **Facade Pattern** | `lib/api.ts` es una fachada que oculta los detalles de las peticiones HTTP (headers, manejo de errores, tokens) y expone métodos simples como `scanApi.start()`, `authApi.login()`. | `frontend/src/lib/api.ts` |
| **Singleton** | La instancia `ai_service = AIService()` en `ai_service.py` actúa como singleton con cache interno para resultados de análisis por tipo de vulnerabilidad. | `ai_service.py` |
| **Template Method** | `_run_scan_background()` define el algoritmo general del escaneo (crawl → módulos → IA → guardar), mientras que cada función `check_*()` implementa el paso específico. | `routes/scan_routes.py`, `scanner.py` |

---

## Conclusiones

1. La arquitectura de **3 capas cliente-servidor** adoptada en **VulnScan Pro** garantiza una separación clara de responsabilidades: presentación (Next.js), lógica de negocio (FastAPI) y datos (MySQL), facilitando el mantenimiento y la evolución independiente de cada capa.

2. La decisión de usar un **monolito modular** sobre microservicios es adecuada para el alcance académico del proyecto: reduce la complejidad operacional sin sacrificar la organización interna del código, que está correctamente desacoplado en módulos con responsabilidades únicas.

3. El **patrón de escaneo en segundo plano** (BackgroundTasks + threading) con **polling desde el cliente** resuelve de forma pragmática el problema de escaneos de larga duración sin bloquear la API ni requerir infraestructura adicional (Celery + Redis).

4. La **integración de DeepSeek AI con fallback local** garantiza que el sistema sea confiable independientemente de la disponibilidad del servicio externo, cumpliendo el requerimiento no funcional de disponibilidad del 99%.

5. La arquitectura de despliegue con **Nginx + systemd + PM2 + UFW** en VPS Linux representa la infraestructura estándar de producción para aplicaciones web en el mercado actual, proporcionando al equipo experiencia práctica en entornos reales.

6. Los 10 patrones de diseño documentados demuestran la aplicación consciente de principios de ingeniería de software (SOLID, DRY) en el diseño del sistema, alineándose con los objetivos formativos del curso de Calidad y Pruebas de Software.

---

*Documento elaborado por el equipo de desarrollo — Curso Calidad y Pruebas de Software — UPT — 2026*
