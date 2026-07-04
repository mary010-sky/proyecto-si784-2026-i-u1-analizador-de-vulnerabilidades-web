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

Informe de Especificación de Requerimientos de Software

Versión 1.0

| CONTROL DE VERSIONES |                  |                |              |            |                  |
|:--------------------:|:-----------------|:---------------|:-------------|:-----------|:-----------------|
| Versión              | Hecha por        | Revisada por   | Aprobada por | Fecha      | Motivo           |
| 1.0                  | M. Calloticona   | M. Ramos       |              | 05/04/2026 | Versión Original |
| 1.1                  | M. Ramos         | M. Calloticona |              | 12/04/2026 | Revisión de casos de uso y requerimientos no funcionales |

<div style="page-break-after: always;"></div>

---

## ÍNDICE GENERAL

1. [Introducción](#1-introducción)  
   1.1. Propósito  
   1.2. Alcance  
   1.3. Definiciones, Siglas y Abreviaturas  
   1.4. Referencias  

2. [Descripción General](#2-descripción-general)  
   2.1. Perspectiva del Producto  
   2.2. Funciones del Producto  
   2.3. Características de los Usuarios  
   2.4. Restricciones  
   2.5. Suposiciones y Dependencias  

3. [Requerimientos Funcionales](#3-requerimientos-funcionales)  
   3.1. Módulo de Autenticación y Usuarios  
   3.2. Módulo de Escaneo  
   3.3. Módulo de Inteligencia Artificial  
   3.4. Módulo de Reportes  
   3.5. Módulo de Administración  
   3.6. Módulo de Dashboard  

4. [Requerimientos No Funcionales](#4-requerimientos-no-funcionales)  

5. [Casos de Uso](#5-casos-de-uso)  

6. [Matriz de Trazabilidad](#6-matriz-de-trazabilidad)  

[Conclusiones](#conclusiones)  

<div style="page-break-after: always;"></div>

---

## Informe de Especificación de Requerimientos de Software (SRS)

---

## 1. Introducción

### 1.1. Propósito

El presente documento tiene como propósito especificar de forma completa y precisa los requerimientos funcionales y no funcionales del sistema **VulnScan Pro — Analizador de Vulnerabilidades Web**, una plataforma DAST (Dynamic Application Security Testing) con inteligencia artificial integrada.

Este documento está dirigido al equipo de desarrollo, al docente supervisor del curso, y a futuros mantenedores del sistema. Sirve como contrato técnico que define el comportamiento esperado del sistema y sus restricciones, constituyendo la base para el diseño, implementación y verificación del software.

### 1.2. Alcance

El sistema **VulnScan Pro** abarca los siguientes módulos funcionales:
1. Autenticación y gestión de usuarios (con roles y protección anti-fuerza bruta)
2. Motor de escaneo de vulnerabilidades (13 módulos OWASP Top 10)
3. Análisis de vulnerabilidades con IA (DeepSeek)
4. Generación y exportación de reportes (PDF, HTML, JSON)
5. Panel de administración (gestión de usuarios y auditoría)
6. Dashboard SOC con estadísticas en tiempo real

El sistema no incluye: análisis de código fuente estático (SAST), integración con sistemas de ticketing externos, ni análisis de aplicaciones móviles nativas.

### 1.3. Definiciones, Siglas y Abreviaturas

| **Término** | **Definición** |
|:------------|:---------------|
| SRS | Software Requirements Specification |
| RF | Requerimiento Funcional |
| RNF | Requerimiento No Funcional |
| UC | Use Case (Caso de Uso) |
| DAST | Dynamic Application Security Testing |
| OWASP | Open Web Application Security Project |
| JWT | JSON Web Token |
| CVSS | Common Vulnerability Scoring System |
| CWE | Common Weakness Enumeration |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| CRUD | Create, Read, Update, Delete |

### 1.4. Referencias

- OWASP Top 10:2021 — https://owasp.org/Top10/
- IEEE Std 830-1998 — Recommended Practice for Software Requirements Specifications
- ISO/IEC 25010:2023 — Systems and software quality models
- FastAPI Documentation — https://fastapi.tiangolo.com
- Next.js 16 Documentation — https://nextjs.org/docs

<div style="page-break-after: always;"></div>

---

## 2. Descripción General

### 2.1. Perspectiva del Producto

**VulnScan Pro** es un sistema nuevo, independiente, que no reemplaza ningún sistema existente. Interactúa con:
- **DeepSeek AI API** (externa): para análisis inteligente de vulnerabilidades.
- **Servidor SMTP** (opcional): para notificaciones de bloqueo de cuenta.
- **Aplicaciones web objetivo** (externas): URLs auditadas mediante peticiones HTTP/HTTPS.

### 2.2. Funciones del Producto

Las funciones principales del sistema son:

1. **Autenticación segura** con JWT, roles diferenciados y protección anti-fuerza bruta.
2. **Escaneo automático** de vulnerabilidades web con 13 módulos especializados.
3. **Crawling** de URLs y detección de tecnologías utilizadas por el objetivo.
4. **Análisis IA** de cada vulnerabilidad detectada con remediación contextualizada.
5. **Visualización** de resultados en dashboard SOC con gráficos interactivos.
6. **Exportación** de reportes en PDF, HTML y JSON.
7. **Administración** de usuarios, roles y logs de auditoría.

### 2.3. Características de los Usuarios

| **Tipo de Usuario** | **Nivel técnico** | **Funciones disponibles** |
|:--------------------|:-----------------:|:--------------------------|
| Administrador | Alto | Todas las funciones del sistema. Gestión de usuarios y auditoría. |
| Analista | Medio-alto | Escaneos, visualización, reportes, análisis IA. |
| Usuario | Medio | Escaneos básicos, visualización de sus propios resultados. |

### 2.4. Restricciones

- El sistema opera únicamente sobre URLs accesibles desde el servidor (no en redes locales del cliente).
- El módulo de IA requiere conexión a internet; si no está disponible, opera en modo fallback local.
- Los escaneos tienen un timeout máximo de 60 segundos por módulo para prevenir bloqueos.
- El sistema no realiza escaneos autenticados (no maneja credenciales de la aplicación objetivo).
- La base de datos debe ser MySQL 8.0 nativo (no compatible con SQLite ni PostgreSQL sin modificaciones).

### 2.5. Suposiciones y Dependencias

- Python 3.11+ instalado en el servidor de producción.
- Node.js 20 LTS instalado para el frontend.
- MySQL 8.0 activo con usuario y base de datos creados.
- Nginx instalado y configurado como proxy inverso.
- La clave `DEEPSEEK_API_KEY` está configurada en el archivo `.env` del backend.

<div style="page-break-after: always;"></div>

---

## 3. Requerimientos Funcionales

### 3.1. Módulo de Autenticación y Usuarios

| **ID** | **Requerimiento** | **Descripción** | **Prioridad** |
|:-------|:-----------------|:----------------|:-------------:|
| RF-01 | Registro de usuarios | El sistema debe permitir el registro con username, email y contraseña. La contraseña debe tener mínimo 8 caracteres, 1 mayúscula y 1 dígito. El primer usuario registrado recibe automáticamente el rol de Administrador. | Alta |
| RF-02 | Inicio de sesión | El sistema debe permitir autenticación con username O email + contraseña. Devuelve un JWT con expiración de 24 horas. | Alta |
| RF-03 | Protección anti-fuerza bruta | Tras 5 intentos fallidos consecutivos, la cuenta se bloquea automáticamente por 15 minutos. El contador se reinicia en inicio de sesión exitoso. | Alta |
| RF-04 | Cierre de sesión | El sistema debe invalidar la sesión activa del usuario (marcar el JTI como inválido en la base de datos). | Alta |
| RF-05 | Perfil de usuario | El usuario puede ver sus datos (username, email, rol, fecha de último acceso, IP de último acceso). | Media |
| RF-06 | Cambio de contraseña | El usuario autenticado puede cambiar su contraseña proporcionando la contraseña actual y la nueva (con las mismas reglas de validación de RF-01). | Media |
| RF-07 | Recuperación de contraseña | El sistema debe generar un token de recuperación enviado por email (o mostrado en modo desarrollo) con expiración de 1 hora. | Baja |
| RF-08 | Roles de usuario | El sistema soporta 3 roles: `admin` (acceso total), `analyst` (escaneos + reportes), `user` (escaneos básicos). Los endpoints aplican control de acceso por rol. | Alta |
| RF-09 | Auditoría de acciones | El sistema debe registrar en la tabla `audit_logs`: acción, usuario, IP de origen, resultado (éxito/fallo) y timestamp, para todas las operaciones de autenticación. | Alta |
| RF-10 | Sesiones activas | El sistema almacena en la tabla `user_sessions` las sesiones activas con: JTI, IP, User-Agent y fecha de expiración. | Media |

### 3.2. Módulo de Escaneo

| **ID** | **Requerimiento** | **Descripción** | **Prioridad** |
|:-------|:-----------------|:----------------|:-------------:|
| RF-11 | Iniciar escaneo | El usuario puede iniciar un escaneo proporcionando: URL objetivo, lista de módulos activos, profundidad de crawl (1-3), timeout por petición (5-60 s), stack tecnológico del objetivo y si se usa análisis IA. El sistema devuelve inmediatamente un `scan_id` y ejecuta el escaneo en segundo plano. | Alta |
| RF-12 | Módulo Headers | Detectar ausencia de: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`. Detectar cookies sin flags `Secure`, `HttpOnly`, `SameSite`. Detectar CORS permisivo (`Access-Control-Allow-Origin: *`). Detectar headers que revelan versiones de servidor. | Alta |
| RF-13 | Módulo SSL/TLS | Verificar: validez del certificado, fecha de vencimiento (alerta si vence en < 30 días), versión del protocolo (TLS 1.0/1.1 son obsoletos), certificado autofirmado. | Alta |
| RF-14 | Módulo SQLi | Probar con payloads de SQL Injection error-based (detectar mensajes de error SQL en respuesta) y boolean-based blind (detectar diferencias de contenido con condición verdadera vs falsa). Aplicar a parámetros GET y formularios POST encontrados. | Alta |
| RF-15 | Módulo XSS | Probar 4 payloads de XSS reflejado en parámetros GET y campos de formulario: `<script>alert(1)</script>`, `"><img src=x onerror=alert(1)>`, `javascript:alert(1)`, `<svg onload=alert(1)>`. Detectar reflejo del payload en la respuesta HTML. | Alta |
| RF-16 | Módulo CSRF | Detectar formularios POST que no contienen campo oculto con token CSRF (nombres comunes: `csrf_token`, `_token`, `csrfmiddlewaretoken`, `authenticity_token`). Detectar cookies sin atributo `SameSite`. | Alta |
| RF-17 | Módulo SSRF | Probar inyección de URL interna (`http://169.254.169.254/`, `http://localhost/`) en parámetros de URL comunes: `url`, `redirect`, `callback`, `fetch`, `request`. Detectar respuestas con contenido del servicio de metadatos o localhost. | Alta |
| RF-18 | Módulo LFI | Probar path traversal en parámetros `file`, `page`, `include`, `path`, `document` con payloads: `../../../etc/passwd`, `....//....//etc/passwd`, `%2e%2e%2f%2e%2e%2fetc/passwd`. Detectar contenido de `/etc/passwd` en la respuesta. | Alta |
| RF-19 | Módulo Command Injection | Probar parámetros con: `; id`, `| whoami`, `&& id`, `` `id` ``, `$(id)`. Detectar output de comandos del sistema operativo (`uid=`, `root`, `www-data`) en la respuesta. | Alta |
| RF-20 | Módulo Open Redirect | Probar parámetros `redirect`, `url`, `next`, `return_to`, `goto`, `continue` con URL externa (`https://evil.com`). Detectar redirecciones 301/302 hacia el dominio inyectado. | Media |
| RF-21 | Módulo Sensitive Files | Verificar accesibilidad de: `.env`, `.git/HEAD`, `phpinfo.php`, `wp-config.php`, `backup.sql`, `database.yml`, `config.php`, `web.config`, `robots.txt`, `sitemap.xml`, `.htaccess`. Reportar archivos con código HTTP 200 que no sean esperados públicamente. | Alta |
| RF-22 | Módulo HTTP Methods | Enviar petición OPTIONS a la URL objetivo. Detectar si los métodos `PUT`, `DELETE`, `TRACE`, `CONNECT` están habilitados y reportarlos como potencialmente peligrosos. | Media |
| RF-23 | Módulo Error Disclosure | Provocar respuestas de error (petición malformada, URL inválida) y detectar en la respuesta: stack traces, rutas del sistema de archivos, mensajes de error SQL, versiones de dependencias. | Media |
| RF-24 | Módulo Crawling | Extraer todos los enlaces (`<a href>`) y formularios (`<form action>`) del HTML de la página objetivo mediante BeautifulSoup. Seguir enlaces internos hasta la profundidad configurada (máx. 3). Retornar lista de URLs descubiertas. | Media |
| RF-25 | Detección tecnológica | Detectar tecnologías del objetivo mediante cabeceras HTTP, meta tags HTML, nombres de archivos y patrones de respuesta: CMS (WordPress, Joomla, Drupal, Magento), frameworks (Laravel, Django, Rails, Express, ASP.NET), librerías JS (jQuery, React, Vue, Angular), WAF (Cloudflare, Sucuri, ModSecurity), CDN (Cloudflare, Akamai, Fastly). | Media |
| RF-26 | Estado del escaneo | El sistema debe exponer un endpoint `GET /api/scans/{id}` que retorne el estado del escaneo: `pending`, `running`, `completed`, `failed`, conteo de vulnerabilidades por severidad y lista de vulnerabilidades encontradas. El frontend realiza polling cada 3 segundos hasta que el estado sea `completed` o `failed`. | Alta |
| RF-27 | Listado de escaneos | El sistema debe exponer un endpoint `GET /api/scans/` que retorne la lista de escaneos del usuario autenticado (paginada: skip/limit), con: URL, estado, total de vulnerabilidades, counts por severidad, duración y fechas. | Alta |
| RF-28 | Eliminación de escaneo | El usuario puede eliminar un escaneo (y sus vulnerabilidades asociadas) que haya realizado. El administrador puede eliminar cualquier escaneo. | Media |
| RF-29 | False Positive | El analista o administrador puede marcar una vulnerabilidad como falso positivo (toggle), lo que actualiza el flag `false_positive` en la base de datos. | Baja |
| RF-30 | Módulos disponibles | El sistema debe exponer un endpoint `GET /api/modules` que liste los 13 módulos disponibles con nombre, ID y descripción. | Baja |

### 3.3. Módulo de Inteligencia Artificial

| **ID** | **Requerimiento** | **Descripción** | **Prioridad** |
|:-------|:-----------------|:----------------|:-------------:|
| RF-31 | Análisis por vulnerabilidad | Si `use_ai=true` en el escaneo, el sistema debe llamar a la API de DeepSeek para cada vulnerabilidad encontrada y obtener: `confirmed` (boolean), `false_positive_probability` (0-100), `cvss_score` (0.0-10.0), `cwe_id` (ej: "CWE-89"), `risk_explanation`, `attack_scenario`, `remediation` (immediate, long_term, code_fix adaptado al stack, config_fix), `references`, `estimated_fix_time`. | Alta |
| RF-32 | Fallback local | Si la API de DeepSeek no está disponible o devuelve error, el sistema debe usar análisis local predefinido para SQLi (CVSS 9.8, CWE-89), XSS (CVSS 7.2, CWE-79) y CSRF (CVSS 6.5, CWE-352). Para otros tipos, retornar análisis genérico con CVSS 5.0. | Alta |
| RF-33 | Reporte ejecutivo IA | Al completar el escaneo, si `use_ai=true`, el sistema debe generar un reporte ejecutivo con: `risk_score` (0-100), `risk_level` (CRÍTICO/ALTO/MEDIO/BAJO), `executive_summary` (2-3 párrafos para gerencia), `top_threats`, `immediate_actions`, `security_posture`, `compliance_notes` (OWASP/PCI-DSS/ISO27001). | Alta |
| RF-34 | Solución por tipo | El sistema debe exponer un endpoint `POST /api/solutions/generate` que, dado un tipo de vulnerabilidad y stack tecnológico, retorne una solución técnica completa con código vulnerable, código seguro, pasos de solución y mejores prácticas. | Media |
| RF-35 | Priorización IA | Las vulnerabilidades encontradas deben ordenarse por severidad (Crítico → Alto → Medio → Bajo → Info) en los resultados del escaneo. | Media |

### 3.4. Módulo de Reportes

| **ID** | **Requerimiento** | **Descripción** | **Prioridad** |
|:-------|:-----------------|:----------------|:-------------:|
| RF-36 | Reporte JSON | El endpoint `GET /api/reports/{scan_id}/json` debe retornar todos los datos del escaneo en formato JSON estructurado: metadata del escaneo, tecnologías detectadas, lista completa de vulnerabilidades con análisis IA, conteos por severidad y reporte ejecutivo IA. | Alta |
| RF-37 | Reporte HTML | El endpoint `GET /api/reports/{scan_id}/html` debe retornar un documento HTML completo con diseño SOC (tema oscuro) que incluya: header con metadata, resumen ejecutivo IA, tabla de vulnerabilidades con badges de severidad, análisis detallado por vulnerabilidad con payloads y evidencias. | Media |
| RF-38 | Reporte PDF | El endpoint `GET /api/reports/{scan_id}/pdf` debe retornar el reporte en formato PDF generado a partir del HTML mediante WeasyPrint. Si WeasyPrint no está disponible, retornar el HTML como fallback. | Media |
| RF-39 | Autenticación en reportes | Los endpoints de reporte deben aceptar el token JWT como parámetro de query (`?token=...`) además del header `Authorization`, para facilitar la descarga directa desde el navegador. | Media |

### 3.5. Módulo de Administración

| **ID** | **Requerimiento** | **Descripción** | **Prioridad** |
|:-------|:-----------------|:----------------|:-------------:|
| RF-40 | Dashboard de administración | El endpoint `GET /api/admin/dashboard` (solo `admin`) debe retornar: total de usuarios, total de escaneos, total de vulnerabilidades, total de críticas, escaneos recientes (10), actividad reciente de audit_logs (10), datos diarios de escaneos (últimos 7 días), vulnerabilidades por severidad. | Alta |
| RF-41 | Listado de usuarios | El endpoint `GET /api/admin/users` (solo `admin`) debe retornar la lista paginada de usuarios con: id, username, email, rol, is_active, last_login, last_login_ip, created_at, failed_attempts, estado de bloqueo. | Alta |
| RF-42 | Cambio de rol | El endpoint `PATCH /api/admin/users/{id}/role` (solo `admin`) debe permitir cambiar el rol de un usuario a `admin`, `analyst` o `user`. | Alta |
| RF-43 | Activar/Desactivar usuario | El endpoint `PATCH /api/admin/users/{id}/toggle-active` (solo `admin`) debe alternar el estado `is_active` del usuario. Los usuarios inactivos no pueden iniciar sesión. | Alta |
| RF-44 | Desbloquear usuario | El endpoint `PATCH /api/admin/users/{id}/unlock` (solo `admin`) debe limpiar el contador de intentos fallidos y el campo `locked_until` de un usuario bloqueado por fuerza bruta. | Alta |
| RF-45 | Eliminar usuario | El endpoint `DELETE /api/admin/users/{id}` (solo `admin`) debe eliminar el usuario y sus datos asociados. No se puede eliminar al propio administrador autenticado. | Alta |
| RF-46 | Logs de auditoría | El endpoint `GET /api/admin/logs` (solo `admin`) debe retornar los logs de auditoría paginados con filtros opcionales: usuario, acción, resultado (éxito/fallo), rango de fechas. | Media |

### 3.6. Módulo de Dashboard

| **ID** | **Requerimiento** | **Descripción** | **Prioridad** |
|:-------|:-----------------|:----------------|:-------------:|
| RF-47 | Estadísticas globales | El dashboard debe mostrar 4 tarjetas de estadísticas: total de escaneos, total de vulnerabilidades, vulnerabilidades críticas, usuarios activos. | Alta |
| RF-48 | Gráfico de severidades | El dashboard debe mostrar un gráfico de dona (doughnut) con la distribución de vulnerabilidades por severidad (Crítico/Alto/Medio/Bajo). | Alta |
| RF-49 | Gráfico de escaneos diarios | El dashboard debe mostrar un gráfico de línea con el conteo de escaneos de los últimos 7 días. | Media |
| RF-50 | Escaneos recientes | El dashboard debe mostrar una tabla con los últimos 10 escaneos: URL, estado, total vulnerabilidades, barra de severidad proporcional, fecha. | Alta |
| RF-51 | Estado del sistema | El dashboard debe mostrar el estado de los 3 componentes del sistema: API Backend, Base de datos MySQL, IA DeepSeek (conectado/desconectado). | Media |

<div style="page-break-after: always;"></div>

---

## 4. Requerimientos No Funcionales

### 4.1. Rendimiento

| **ID** | **Requerimiento** | **Métrica** |
|:-------|:-----------------|:------------|
| RNF-01 | Tiempo de respuesta de la API | Los endpoints de autenticación y consulta deben responder en menos de 500 ms en condiciones normales (conexión local al servidor). |
| RNF-02 | Tiempo de escaneo | Un escaneo con todos los módulos activos (sin IA) debe completarse en menos de 120 segundos para URLs estándar. |
| RNF-03 | Carga concurrente | El sistema debe soportar al menos 10 usuarios concurrentes realizando escaneos simultáneos sin degradación de rendimiento superior al 20%. |
| RNF-04 | Tiempo de carga del dashboard | El dashboard debe cargar y renderizar completamente en menos de 3 segundos en una conexión de 10 Mbps. |

### 4.2. Seguridad

| **ID** | **Requerimiento** | **Descripción** |
|:-------|:-----------------|:----------------|
| RNF-05 | Cifrado de contraseñas | Todas las contraseñas deben almacenarse con bcrypt con cost factor ≥ 10. Nunca en texto plano. |
| RNF-06 | JWT seguro | Los tokens JWT deben firmarse con HMAC-SHA256 (HS256), incluir JTI único, expiración de 24 horas y la clave secreta debe tener mínimo 256 bits de entropía. |
| RNF-07 | HTTPS obligatorio en producción | Todas las comunicaciones en producción deben ser sobre HTTPS. El servidor Nginx debe redirigir HTTP a HTTPS. |
| RNF-08 | Headers de seguridad | El backend debe incluir en todas las respuestas: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`. |
| RNF-09 | Rate limiting | La API debe limitar: endpoint de login a 5 peticiones/minuto por IP, escaneos a 2/minuto por IP, resto de la API a 10 peticiones/segundo por IP. |
| RNF-10 | CORS | El servidor debe aceptar peticiones CORS únicamente desde los orígenes configurados en `ALLOWED_ORIGINS`. No se admite `*` en producción. |
| RNF-11 | Variables sensibles | Las credenciales (DATABASE_URL, SECRET_KEY, DEEPSEEK_API_KEY) deben gestionarse en variables de entorno; nunca commiteadas al repositorio. |

### 4.3. Disponibilidad y Confiabilidad

| **ID** | **Requerimiento** | **Descripción** |
|:-------|:-----------------|:----------------|
| RNF-12 | Disponibilidad | El sistema debe estar disponible el 99% del tiempo (máximo 7.3 horas de downtime mensual). |
| RNF-13 | Recuperación automática | El servicio backend (Gunicorn/FastAPI) debe reiniciarse automáticamente si falla, mediante la directiva `Restart=always` del servicio systemd. |
| RNF-14 | Integridad de datos | Los escaneos interrumpidos por fallo del servidor deben marcarse como `failed` automáticamente en el siguiente inicio del sistema. |
| RNF-15 | Logging | El sistema debe registrar en logs: inicio/fin de escaneos, errores de módulos, fallos de autenticación, peticiones a la API de IA y respuestas de error HTTP 5xx. |

### 4.4. Usabilidad

| **ID** | **Requerimiento** | **Descripción** |
|:-------|:-----------------|:----------------|
| RNF-16 | Interfaz intuitiva | Un usuario con conocimientos básicos de redes debe poder iniciar su primer escaneo en menos de 2 minutos sin necesitar documentación. |
| RNF-17 | Responsive design | La interfaz debe ser usable en resoluciones desde 1280×800 (desktop) y debe adaptarse para tablets (768×1024). No se requiere compatibilidad con móviles. |
| RNF-18 | Idioma | La interfaz debe estar en español; los reportes generados también en español. La documentación técnica de la API (Swagger) puede estar en inglés. |
| RNF-19 | Feedback de progreso | El usuario debe ver indicadores de progreso durante el escaneo (estado: pending/running) con actualización cada 3 segundos. |

### 4.5. Mantenibilidad

| **ID** | **Requerimiento** | **Descripción** |
|:-------|:-----------------|:----------------|
| RNF-20 | Modularidad del scanner | Cada módulo de escaneo debe ser una función independiente en `scanner.py` con firma `check_nombre(url) -> List[Dict]`. Añadir un nuevo módulo no debe requerir modificar otros módulos. |
| RNF-21 | Documentación de API | La API debe documentarse automáticamente con Swagger UI (FastAPI) en `/api/docs` y ReDoc en `/api/redoc`. |
| RNF-22 | Código limpio | El código Python debe cumplir PEP 8. El TypeScript/React debe seguir las convenciones del linter configurado en el proyecto. |
| RNF-23 | Control de versiones | Todo el código fuente debe estar versionado en Git con commits descriptivos. El repositorio debe incluir `.gitignore` que excluya `.env`, `venv/`, `node_modules/`, `__pycache__/`. |

### 4.6. Portabilidad

| **ID** | **Requerimiento** | **Descripción** |
|:-------|:-----------------|:----------------|
| RNF-24 | Compatibilidad del backend | El backend debe ejecutarse en cualquier sistema Linux con Python 3.11+ y MySQL 8.0, sin dependencias de sistema operativo específico. |
| RNF-25 | Script de despliegue | El repositorio debe incluir un script `deploy.sh` que automatice la instalación completa del sistema en un VPS Ubuntu 22.04 limpio. |
| RNF-26 | Variables de entorno | La configuración del sistema (URLs, claves, puertos) debe ser completamente configurable mediante variables de entorno en `.env`, sin modificar código fuente. |

<div style="page-break-after: always;"></div>

---

## 5. Casos de Uso

### 5.1. Diagrama de Actores

```
┌─────────────────────────────────────────────────────────────┐
│                     Sistema VulnScan Pro                     │
│                                                             │
│  ┌──────────┐     ┌───────────┐     ┌──────────────────┐   │
│  │ Usuario  │     │ Analista  │     │  Administrador   │   │
│  └────┬─────┘     └─────┬─────┘     └────────┬─────────┘   │
│       │                 │                     │             │
│       ▼                 ▼                     ▼             │
│  - Registrarse     - Todo lo de         - Todo lo de       │
│  - Iniciar sesión    Usuario +            Analista +        │
│  - Ver dashboard   - Ver reportes       - Gestionar         │
│  - Iniciar escaneo - Exportar PDF/JSON    usuarios          │
│  - Ver resultados  - Análisis IA        - Ver audit logs    │
│  - Cerrar sesión                        - Cambiar roles     │
└─────────────────────────────────────────────────────────────┘
```

### 5.2. Casos de Uso Principales

---

**UC-01: Registrar Usuario**

| | |
|:--|:--|
| **Actor** | Usuario no autenticado |
| **Precondición** | El usuario no tiene cuenta en el sistema |
| **Flujo principal** | 1. El usuario accede a `/register`. 2. Completa username, email y contraseña. 3. El sistema valida: username único, email único, contraseña ≥ 8 chars + 1 mayúscula + 1 dígito. 4. Si es el primer usuario, recibe rol `admin`; si no, recibe rol `user`. 5. El sistema almacena la cuenta y devuelve el token JWT. 6. El usuario es redirigido al dashboard. |
| **Flujo alternativo** | A1: Username o email ya existe → error 400 con mensaje descriptivo. A2: Contraseña inválida → error 400 indicando los requisitos incumplidos. |
| **Postcondición** | Cuenta creada, usuario autenticado en el sistema. |

---

**UC-02: Iniciar Sesión**

| | |
|:--|:--|
| **Actor** | Usuario registrado |
| **Precondición** | El usuario tiene cuenta activa |
| **Flujo principal** | 1. El usuario ingresa username/email y contraseña. 2. El sistema verifica si la cuenta está bloqueada (`locked_until`). 3. El sistema verifica si la cuenta está activa (`is_active`). 4. El sistema valida la contraseña con bcrypt. 5. Reinicia el contador de intentos fallidos. 6. Registra la sesión en `user_sessions` con IP y User-Agent. 7. Devuelve JWT y datos del usuario (rol, username). |
| **Flujo alternativo** | A1: Cuenta bloqueada → error 423 con tiempo restante de bloqueo. A2: Contraseña incorrecta → incrementa `failed_login_attempts`; si llega a 5, bloquea por 15 min. A3: Cuenta inactiva → error 403. |
| **Postcondición** | Usuario autenticado con JWT válido por 24 horas. |

---

**UC-03: Iniciar Escaneo**

| | |
|:--|:--|
| **Actor** | Usuario, Analista o Administrador autenticado |
| **Precondición** | Usuario autenticado con token JWT válido |
| **Flujo principal** | 1. El usuario ingresa la URL objetivo. 2. Selecciona los módulos de análisis (default: todos). 3. Configura opciones avanzadas: profundidad (1-3), timeout (5-60 s), stack tecnológico, activar IA. 4. Presiona "Iniciar Escaneo". 5. El sistema valida la URL (formato HTTP/HTTPS). 6. Crea el registro de escaneo en la BD con estado `pending`. 7. Devuelve el `scan_id` al frontend. 8. Lanza el escaneo como tarea en segundo plano. 9. El frontend inicia polling cada 3 segundos sobre `GET /api/scans/{id}`. |
| **Flujo alternativo** | A1: URL inválida → error 400. A2: Error en la red durante el escaneo → el escaneo se marca como `failed` con mensaje de error. |
| **Postcondición** | Escaneo creado y en ejecución. El usuario puede ver el progreso en tiempo real. |

---

**UC-04: Ver Resultados del Escaneo**

| | |
|:--|:--|
| **Actor** | Usuario, Analista o Administrador autenticado |
| **Precondición** | Existe un escaneo completado del usuario |
| **Flujo principal** | 1. El usuario hace click en un escaneo de la lista. 2. El sistema muestra la página de detalle con: metadata (URL, duración, fecha), tecnologías detectadas, URLs crawleadas, resumen de vulnerabilidades por severidad. 3. Para cada vulnerabilidad: tipo, severidad, endpoint afectado, payload utilizado, evidencia, descripción del riesgo, solución recomendada. 4. Si tiene análisis IA: CVSS score, CWE ID, escenario de ataque, código de remediación. 5. Si tiene reporte ejecutivo IA: risk score, resumen ejecutivo, amenazas top, acciones inmediatas. |
| **Flujo alternativo** | A1: El escaneo no pertenece al usuario y no es admin → error 403. |
| **Postcondición** | El usuario tiene acceso completo a todos los hallazgos del escaneo. |

---

**UC-05: Exportar Reporte**

| | |
|:--|:--|
| **Actor** | Analista o Administrador autenticado |
| **Precondición** | Existe un escaneo completado |
| **Flujo principal** | 1. El usuario accede al detalle del escaneo. 2. Presiona el botón de descarga (PDF, HTML o JSON). 3. Para PDF/HTML: el sistema genera el documento y lo sirve como archivo descargable. 4. Para JSON: el sistema retorna el JSON completo con todos los datos del escaneo. |
| **Flujo alternativo** | A1: WeasyPrint no instalado → el sistema ofrece HTML como alternativa al PDF. |
| **Postcondición** | El usuario descarga el reporte en el formato seleccionado. |

---

**UC-06: Gestionar Usuarios (Admin)**

| | |
|:--|:--|
| **Actor** | Administrador autenticado |
| **Precondición** | Usuario autenticado con rol `admin` |
| **Flujo principal** | 1. El admin accede a `/admin`. 2. Visualiza la tabla de usuarios con estado de cada uno. 3. Puede: cambiar el rol (dropdown en línea), activar/desactivar cuenta (toggle), desbloquear cuenta bloqueada por fuerza bruta, eliminar cuenta. 4. Puede revisar el historial de audit_logs con filtros por acción, usuario y resultado. |
| **Flujo alternativo** | A1: El admin intenta eliminarse a sí mismo → error 400. |
| **Postcondición** | Los cambios en usuarios se persisten en la base de datos. |

---

## 6. Matriz de Trazabilidad

| **Requerimiento** | **Componente** | **Archivo** | **Endpoint / Función** |
|:------------------|:---------------|:------------|:-----------------------|
| RF-01 a RF-10 | Backend Auth | `routes/auth_routes.py` | `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, `PUT /api/auth/change-password` |
| RF-11 a RF-30 | Backend Scanner | `scanner.py`, `routes/scan_routes.py` | `POST /api/scans/`, `GET /api/scans/{id}`, `GET /api/scans/` |
| RF-31 a RF-35 | Backend IA | `ai_service.py`, `solutions_routes.py` | `POST /api/solutions/generate` |
| RF-36 a RF-39 | Backend Reports | `routes/report_routes.py` | `GET /api/reports/{id}/json`, `GET /api/reports/{id}/html`, `GET /api/reports/{id}/pdf` |
| RF-40 a RF-46 | Backend Admin | `routes/admin_routes.py` | `GET /api/admin/dashboard`, `GET /api/admin/users`, `PATCH /api/admin/users/{id}/role` |
| RF-47 a RF-51 | Frontend Dashboard | `app/dashboard/page.tsx` | Componentes: StatCard, Chart, RecentScans |
| RNF-01 a RNF-04 | Backend Config | `main.py`, `vulnscan-backend.service` | Gunicorn (4 workers), QueuePool MySQL |
| RNF-05 a RNF-11 | Auth + Config | `auth.py`, `.env`, `nginx.conf` | bcrypt, JWT HS256, Nginx rate limiting |
| RNF-12 a RNF-15 | Infra | `vulnscan-backend.service`, `deploy.sh` | systemd Restart=always, logging |
| RNF-20 a RNF-26 | Infra + Code | `scanner.py`, `deploy.sh`, `.env.example` | Arquitectura modular, script despliegue |

---

## Conclusiones

1. El presente documento especifica de forma completa y verificable los **50 requerimientos funcionales** y **26 requerimientos no funcionales** del sistema **VulnScan Pro**, cubriendo todos los módulos de la plataforma.

2. La estructura modular del sistema (13 módulos de escaneo independientes, IA con fallback, roles diferenciados) permite que cada requerimiento sea implementado y verificado de forma aislada, facilitando el proceso de pruebas unitarias e integración.

3. Los casos de uso documentados (UC-01 a UC-06) cubren los flujos críticos del sistema y los flujos alternativos de error, proporcionando una guía clara para las pruebas funcionales de aceptación.

4. La matriz de trazabilidad establece la correspondencia directa entre cada requerimiento y su implementación en el código fuente, facilitando la verificación y el mantenimiento del sistema a lo largo del tiempo.

---

*Documento elaborado por el equipo de desarrollo — Curso Calidad y Pruebas de Software — UPT — 2026*
