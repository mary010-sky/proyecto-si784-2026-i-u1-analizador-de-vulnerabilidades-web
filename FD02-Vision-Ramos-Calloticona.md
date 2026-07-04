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

Informe de Visión

Versión 1.1

| CONTROL DE VERSIONES |                  |                |              |            |                             |
|:--------------------:|:-----------------|:---------------|:-------------|:-----------|:----------------------------|
| Versión              | Hecha por        | Revisada por   | Aprobada por | Fecha      | Motivo                      |
| 1.0                  | M. Calloticona   | M. Ramos       |              | 28/03/2026 | Versión Original            |
| 1.1                  | M. Ramos         | M. Calloticona |              | 04/04/2026 | Incorporación DeepSeek AI e infraestructura VPS |

<div style="page-break-after: always;"></div>

---

## ÍNDICE GENERAL

1. [Introducción](#1-introducción)  
   1.1. Propósito  
   1.2. Alcance  
   1.3. Definiciones, Siglas y Abreviaturas  
   1.4. Referencias  
   1.5. Visión General  

2. [Posicionamiento](#2-posicionamiento)  
   2.1. Oportunidad de Negocio  
   2.2. Definición del Problema  

3. [Descripción de los Interesados y Usuarios](#3-descripción-de-los-interesados-y-usuarios)  
   3.1. Resumen de los Interesados  
   3.2. Resumen de los Usuarios  
   3.3. Entorno de Usuario  
   3.4. Perfiles de los Interesados  
   3.5. Perfiles de los Usuarios  
   3.6. Necesidades de los Interesados y Usuarios  

4. [Vista General del Producto](#4-vista-general-del-producto)  
   4.1. Perspectiva del Producto  
   4.2. Resumen de Capacidades  
   4.3. Suposiciones y Dependencias  
   4.4. Costos y Precios  
   4.5. Licenciamiento e Instalación  

5. [Características del Producto](#5-características-del-producto)  

6. [Restricciones](#6-restricciones)  

7. [Rangos de Calidad](#7-rangos-de-calidad)  

8. [Precedencia y Prioridad](#8-precedencia-y-prioridad)  

9. [Otros Requisitos del Producto](#9-otros-requisitos-del-producto)  

[Conclusiones](#conclusiones)  
[Recomendaciones](#recomendaciones)  
[Bibliografía](#bibliografía)  
[Webgrafía](#webgrafía)  

<div style="page-break-after: always;"></div>

---

## Informe de Visión

---

## 1. Introducción

### 1.1. Propósito

El presente documento define los objetivos estratégicos, capacidades técnicas y alcance del sistema **VulnScan Pro**, una plataforma de análisis dinámico de seguridad (DAST) potenciada por inteligencia artificial, desarrollada en el marco del curso de Calidad y Pruebas de Software de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

Este documento sirve como acuerdo de visión entre el equipo de desarrollo y los interesados del proyecto, asegurando que el software cumpla con los estándares de seguridad web establecidos por el **OWASP Top 10**, los criterios de calidad definidos por la norma **ISO/IEC 25010** y las buenas prácticas de desarrollo seguro (S-SDLC).

### 1.2. Alcance

**VulnScan Pro** es una aplicación web que realiza auditorías de seguridad dinámica sobre URLs objetivo accesibles vía HTTP/HTTPS. El sistema analiza:

- **13 módulos de detección:** Cabeceras HTTP de seguridad (CSP, HSTS, X-Frame-Options, X-Content-Type), SQL Injection (error-based y blind), Cross-Site Scripting (XSS reflejado), CSRF, SSRF, LFI/Path Traversal, Command Injection, Open Redirect, archivos sensibles expuestos (.env, .git, phpinfo.php), métodos HTTP peligrosos (PUT, DELETE, TRACE), divulgación de errores y crawling de URLs.
- **Análisis SSL/TLS:** Validez del certificado, versión del protocolo, fecha de vencimiento.
- **Detección tecnológica:** CMS (WordPress, Joomla, Drupal), frameworks (Laravel, Django, Rails), librerías JS (jQuery, React, Vue), WAF y CDN.
- **Inteligencia Artificial (DeepSeek):** Análisis por vulnerabilidad con puntuación CVSS, CWE, escenario de ataque y código de remediación específico por stack tecnológico.
- **Reportes:** PDF (WeasyPrint), HTML y JSON exportables.

El sistema no ejecuta ataques destructivos ni afecta la disponibilidad del objetivo. Está limitado a pruebas no intrusivas sobre aplicaciones en entornos de desarrollo, preproducción o con autorización explícita del propietario.

### 1.3. Definiciones, Siglas y Abreviaturas

| **Sigla/Término** | **Definición** |
|:------------------|:---------------|
| DAST | Dynamic Application Security Testing — pruebas de seguridad sobre la aplicación en ejecución. |
| OWASP | Open Web Application Security Project — organización de referencia en seguridad web. |
| SQLi | SQL Injection — inyección de código SQL en parámetros de entrada. |
| XSS | Cross-Site Scripting — inyección de scripts maliciosos en páginas web. |
| CSRF | Cross-Site Request Forgery — falsificación de solicitudes entre sitios. |
| SSRF | Server-Side Request Forgery — peticiones del servidor a recursos internos no autorizados. |
| LFI | Local File Inclusion — inclusión de archivos locales del servidor. |
| CSP | Content Security Policy — cabecera que controla los recursos cargables por el navegador. |
| HSTS | HTTP Strict Transport Security — cabecera que fuerza el uso de HTTPS. |
| SSL/TLS | Secure Sockets Layer / Transport Layer Security — protocolos de cifrado. |
| JWT | JSON Web Token — estándar para transmisión segura de información entre partes. |
| CVSS | Common Vulnerability Scoring System — sistema de puntuación de vulnerabilidades (0-10). |
| CWE | Common Weakness Enumeration — catálogo de debilidades de software. |
| VPS | Virtual Private Server — servidor virtual privado en la nube. |
| SOC | Security Operations Center — centro de operaciones de seguridad. |
| ISO/IEC 25010 | Norma internacional que define el modelo de calidad para productos de software. |
| S-SDLC | Secure Software Development Lifecycle — ciclo de desarrollo de software seguro. |

### 1.4. Referencias

- OWASP Foundation. (2025). *OWASP Top 10 Project*. https://owasp.org/Top10/
- ISO/IEC 25010:2023. *Systems and software engineering — System and software quality models*.
- Ley N° 30096 — Ley de Delitos Informáticos del Perú.
- Ley N° 29733 — Ley de Protección de Datos Personales del Perú.
- FastAPI Documentation. (2025). https://fastapi.tiangolo.com
- Next.js Documentation. (2025). https://nextjs.org/docs
- DeepSeek API Documentation. (2025). https://api.deepseek.com/docs
- NIST. (2024). *National Vulnerability Database*. https://nvd.nist.gov

### 1.5. Visión General

**VulnScan Pro** es una herramienta automatizada de código abierto que permite a ingenieros de QA, desarrolladores y auditores de seguridad identificar riesgos web de forma proactiva antes del despliegue a producción. La arquitectura está compuesta por:

- **Frontend:** Next.js 16 (App Router) + TypeScript + TailwindCSS — dashboard SOC con gráficos en tiempo real.
- **Backend:** Python + FastAPI + SQLAlchemy — API REST con autenticación JWT, roles y auditoría.
- **Base de datos:** MySQL 8.0 nativo con pool de conexiones (QueuePool).
- **IA:** DeepSeek AI (OpenAI-compatible API) para análisis inteligente por vulnerabilidad.
- **Infraestructura:** VPS Linux (149.34.48.176) con Nginx, systemd y PM2.

Los resultados se presentan en un dashboard de seguridad con clasificación por severidad (Crítico, Alto, Medio, Bajo), análisis IA detallado por hallazgo, y exportación de reportes en PDF, HTML y JSON para su uso en auditorías académicas y técnicas.

<div style="page-break-after: always;"></div>

---

## 2. Posicionamiento

### 2.1. Oportunidad de Negocio

La creciente digitalización de servicios en Tacna y el Perú ha incrementado la superficie de ataque de las aplicaciones web locales. Sin embargo, las herramientas de seguridad profesionales tienen costos de licenciamiento inaccesibles para el contexto académico y las PYMES de la región:

| **Herramienta** | **Costo anual (USD)** | **Accesible para PYMES/Estudiantes** |
|:----------------|:---------------------:|:------------------------------------:|
| Burp Suite Professional | USD 449 | No |
| Nessus Professional | USD 3,590 | No |
| Acunetix | USD 4,500 | No |
| OpenVAS (cloud) | USD 1,200 | No |
| **VulnScan Pro** | **USD 0** | **Sí** |

**VulnScan Pro** cubre esa brecha ofreciendo capacidades equivalentes a herramientas de nivel profesional de forma gratuita, con inteligencia artificial integrada y enfocada en las vulnerabilidades más prevalentes según el OWASP Top 10.

### 2.2. Definición del Problema

Las aplicaciones web desarrolladas en entornos académicos y de pequeñas empresas frecuentemente se despliegan con configuraciones de seguridad deficientes: cabeceras HTTP ausentes, certificados SSL vencidos, formularios susceptibles a inyección de código, cookies sin flags de protección y archivos de configuración sensibles expuestos públicamente.

El problema central es la **ausencia de una instancia de verificación de seguridad entre el desarrollo y el despliegue**. Los desarrolladores no cuentan con herramientas accesibles y comprensibles para auditar su código antes de publicarlo. VulnScan Pro actúa como esa instancia, automatizando las pruebas más críticas del S-SDLC y presentando resultados con recomendaciones de remediación accionables generadas por IA.

**Declaración del problema:**

> Para *desarrolladores web, estudiantes de ingeniería de sistemas y PYMES de la región Tacna* que *necesitan verificar la seguridad de sus aplicaciones antes de desplegarlas*, **VulnScan Pro** es una *plataforma DAST con IA* que *detecta automáticamente vulnerabilidades OWASP Top 10 y genera soluciones técnicas específicas*, a diferencia de *las herramientas profesionales actuales* que *tienen costos inaccesibles y curvas de aprendizaje elevadas*.

<div style="page-break-after: always;"></div>

---

## 3. Descripción de los Interesados y Usuarios

### 3.1. Resumen de los Interesados

| **Interesado** | **Rol** | **Interés principal** |
|:---------------|:--------|:----------------------|
| Ing. Patrick Jose Cuadros Quiroga | Docente supervisor | Evaluar la calidad técnica del sistema y su alineación con los estándares del curso. |
| Calloticona Chambilla, Marymar D. | Desarrolladora backend | Construir un sistema funcional, seguro y bien arquitecturado. |
| Ramos Loza, Mariela Estefany | Desarrolladora frontend / QA | Garantizar una interfaz usable y pruebas de calidad del sistema. |
| Estudiantes EPIS (UPT) | Usuarios finales académicos | Contar con una herramienta práctica para sus propios proyectos web. |
| Auditores de TI | Revisores externos | Obtener reportes técnicos que permitan validar la seguridad de aplicaciones. |
| PYMES de Tacna | Beneficiarios externos | Acceder a diagnósticos de seguridad sin costo de licenciamiento. |

### 3.2. Resumen de los Usuarios

Los usuarios directos del sistema son ingenieros de QA, desarrolladores fullstack y estudiantes de sistemas con conocimientos básicos en protocolos web. Interactúan con el frontend para iniciar escaneos, revisar resultados con análisis IA y exportar reportes. El sistema soporta tres roles: **Administrador** (gestión completa), **Analista** (escaneos y reportes) y **Usuario** (escaneos básicos).

### 3.3. Entorno de Usuario

El sistema es accesible desde cualquier navegador web moderno (Chrome 120+, Firefox 120+, Edge 120+) en entornos de escritorio. No requiere instalación local. El backend se ejecuta en el VPS (149.34.48.176) con acceso permanente a internet para alcanzar las URLs objetivo durante el escaneo.

### 3.4. Perfiles de los Interesados

**Docente del curso**
- Nombre: Ing. Patrick Jose Cuadros Quiroga
- Interés: Evaluar la calidad técnica, funcional y de seguridad del sistema en relación con el OWASP Top 10 y la norma ISO/IEC 25010.
- Criterio de éxito: El sistema detecta correctamente al menos 8 categorías del OWASP Top 10 con resultados verificables y documentados.

**Auditores de TI externos**
- Interés: Reportes PDF claros con hallazgos, puntuación CVSS, identificador CWE y recomendaciones de remediación accionables.
- Criterio de éxito: Los reportes son exportables y contienen información suficiente para integrarse en procesos de auditoría formal.

### 3.5. Perfiles de los Usuarios

**Administrador del sistema**
- Conocimientos: Administración de sistemas, gestión de usuarios, seguridad informática avanzada.
- Responsabilidades: Gestionar usuarios (crear, editar, asignar roles, bloquear), revisar logs de auditoría, acceder a estadísticas globales del dashboard.
- Frecuencia de uso: Media — gestión periódica del sistema.

**Analista de seguridad / Ingeniero de QA**
- Conocimientos: Protocolos HTTP/HTTPS, fundamentos de seguridad web, uso de herramientas de testing.
- Frecuencia de uso: Alta — previo a cada ciclo de despliegue.
- Objetivo: Identificar, priorizar y documentar vulnerabilidades con el apoyo del análisis IA antes del pase a producción.

**Desarrollador fullstack / Estudiante**
- Conocimientos: Desarrollo web, nociones básicas de seguridad.
- Frecuencia de uso: Media — durante las etapas de integración y pruebas.
- Objetivo: Validar que su implementación no introduce vulnerabilidades conocidas del OWASP Top 10.

### 3.6. Necesidades de los Interesados y Usuarios

| **Necesidad** | **Problema actual** | **Solución propuesta** |
|:--------------|:--------------------|:-----------------------|
| Detectar vulnerabilidades antes del despliegue | No hay herramientas accesibles para auditar antes de publicar. | VulnScan Pro realiza análisis DAST automático sobre la URL del proyecto. |
| Entender el riesgo real de cada vulnerabilidad | Los reportes de herramientas existentes son técnicos y difíciles de interpretar. | DeepSeek AI genera explicaciones en español con escenarios de ataque y código de solución. |
| Reportes exportables para auditoría | No hay registro histórico ni documentación formal de seguridad. | El sistema genera reportes PDF, HTML y JSON con historial completo por escaneo. |
| Gestión de usuarios y roles | Los sistemas simples no diferencian niveles de acceso. | Panel administrativo con roles Admin/Analista/Usuario y auditoría de acciones. |
| Integración con stacks tecnológicos específicos | Las herramientas genéricas no adaptan las soluciones al stack del proyecto. | La IA adapta el código de remediación al stack seleccionado (Python, PHP, Node.js, Java, .NET). |

<div style="page-break-after: always;"></div>

---

## 4. Vista General del Producto

### 4.1. Perspectiva del Producto

**VulnScan Pro** es una herramienta independiente con arquitectura cliente-servidor de 3 capas:

```
[Usuario / Navegador]
        │  HTTPS
        ▼
  [Nginx — Proxy Inverso]
        │
   ┌────┴────────────┐
   │                 │
[Next.js 16      [FastAPI — Python]
 Frontend]           │
   :3000          [MySQL 8.0]
                     │
              [DeepSeek AI API]
```

El frontend (Next.js + TypeScript + TailwindCSS) consume la API REST del backend (FastAPI + Python). El backend orquesta los módulos de escaneo, gestiona la persistencia en MySQL y se comunica con la API de DeepSeek para el análisis IA. El sistema es autónomo salvo por la integración externa con DeepSeek (con fallback local si la API no está disponible).

### 4.2. Resumen de Capacidades

| **Capacidad** | **Descripción** |
|:--------------|:----------------|
| Scanner OWASP multimódulo | 13 módulos: Headers, SSL, XSS, SQLi, CSRF, Open Redirect, LFI, Command Injection, SSRF, Sensitive Files, HTTP Methods, Error Disclosure, Crawling. |
| Análisis IA por vulnerabilidad | DeepSeek AI genera CVSS, CWE, escenario de ataque y código de remediación por stack tecnológico. |
| Dashboard SOC en tiempo real | Gráficos de dona (vulns por severidad), línea (escaneos diarios), estadísticas globales, estado del sistema. |
| Autenticación y roles | JWT con roles Admin/Analista/Usuario, brute-force protection (bloqueo a los 5 intentos, 15 min), auditoría de acciones. |
| Detección tecnológica | CMS (WordPress, Joomla, Drupal), frameworks (Laravel, Django, Rails), librerías JS, WAF, CDN. |
| Reportes exportables | PDF (WeasyPrint), HTML con diseño SOC, JSON estructurado con todos los hallazgos y análisis IA. |
| Historial de escaneos | Registro completo con URLs crawleadas, tecnologías detectadas, duración y conteo por severidad. |
| Panel administrativo | Gestión de usuarios: asignar roles, activar/desactivar, desbloquear, eliminar. Logs de auditoría filtrados. |

### 4.3. Suposiciones y Dependencias

- El VPS (149.34.48.176) tiene acceso a internet para alcanzar las URLs objetivo durante el escaneo.
- El usuario tiene permisos legales sobre la aplicación que desea analizar.
- Las URLs objetivo responden mediante protocolo HTTP o HTTPS.
- La API de DeepSeek está operativa; si no lo está, el sistema usa análisis local de fallback.
- El entorno de producción cuenta con Python 3.11+, Node.js 20+, MySQL 8.0 y Nginx instalados.

### 4.4. Costos y Precios

El proyecto es de desarrollo académico con costo de licenciamiento cero. Todo el stack tecnológico es de código abierto. Los costos están limitados al tiempo de desarrollo del equipo y al VPS ya contratado. La API de DeepSeek ofrece créditos iniciales gratuitos suficientes para el uso académico del proyecto.

### 4.5. Licenciamiento e Instalación

El sistema se distribuye bajo **Licencia MIT**, permitiendo su uso, modificación y distribución libre con mantenimiento del aviso de copyright. La instalación se realiza ejecutando el script `deploy.sh` incluido en el repositorio, que automatiza todo el proceso de configuración del servidor (dependencias, MySQL, backend systemd, frontend PM2, Nginx, UFW) en un único comando.

<div style="page-break-after: always;"></div>

---

## 5. Características del Producto

| **ID** | **Característica** | **Descripción** | **Prioridad** |
|:-------|:------------------|:----------------|:-------------:|
| F-01 | Escaneo de cabeceras HTTP | Detecta ausencia o mala configuración de: CSP, HSTS, X-Frame-Options, X-Content-Type, X-XSS-Protection, Referrer-Policy. | Crítica |
| F-02 | Detección SQL Injection | Error-based (mensajes de error SQL) + boolean-based blind (diferencias de respuesta con payloads de variación lógica). | Crítica |
| F-03 | Detección XSS reflejado | Inyección de 4 payloads en parámetros GET/POST, detección de reflejo en respuesta HTML. | Crítica |
| F-04 | Validación SSL/TLS | Expiración del certificado, protocolo TLS (v1.0/v1.1 obsoleto), certificado inválido. | Alta |
| F-05 | Detección CSRF | Formularios POST sin token CSRF, cookie sin flag SameSite. | Alta |
| F-06 | Detección SSRF | Inyección de URL interna (169.254.169.254) en parámetros de URL. | Alta |
| F-07 | Detección LFI | Path traversal con `../etc/passwd` en parámetros de ruta y archivo. | Alta |
| F-08 | Detección Command Injection | Inyección de comandos OS (`; id`, `| whoami`) y detección de salida en respuesta. | Alta |
| F-09 | Archivos sensibles expuestos | Verificación de acceso a: `.env`, `.git/HEAD`, `phpinfo.php`, `wp-config.php`, `backup.sql`, etc. | Alta |
| F-10 | Open Redirect | Inyección de URLs externas en parámetros de redirección (redirect, url, next, return_to). | Media |
| F-11 | Métodos HTTP peligrosos | Detección de PUT, DELETE, TRACE habilitados mediante solicitud OPTIONS. | Media |
| F-12 | Error Disclosure | Detección de stack traces, mensajes de error SQL, rutas del sistema en respuestas de error. | Media |
| F-13 | Web Crawling | Extracción de URLs y endpoints desde el HTML de la página objetivo (BeautifulSoup). | Media |
| F-14 | Detección tecnológica | Fingerprinting de CMS, frameworks, JS libs, WAF y CDN mediante headers y patrones HTML. | Media |
| F-15 | Análisis IA DeepSeek | CVSS score, CWE ID, escenario de ataque, código de remediación, referencias, tiempo estimado de corrección. | Alta |
| F-16 | Dashboard SOC | Estadísticas globales, gráfico dona (vulns/severidad), gráfico línea (escaneos/día), scans recientes. | Alta |
| F-17 | Reporte ejecutivo IA | Risk score (0-100), nivel de riesgo, resumen para gerencia, amenazas top, acciones inmediatas, postura de seguridad. | Media |
| F-18 | Exportación PDF/HTML/JSON | Reportes con diseño SOC para archivado y auditoría formal. | Media |
| F-19 | Autenticación con roles | JWT con roles Admin/Analista/Usuario, brute-force protection, registro de sesiones por IP. | Crítica |
| F-20 | Panel administrativo | Gestión de usuarios, cambio de roles, logs de auditoría filtrados por acción/usuario/fecha. | Alta |

<div style="page-break-after: always;"></div>

---

## 6. Restricciones

### 6.1. Restricciones Funcionales

- El sistema no ejecuta ataques de denegación de servicio (DoS/DDoS) ni pruebas que afecten la disponibilidad del objetivo.
- El análisis está limitado a aplicaciones web accesibles mediante HTTP/HTTPS. No cubre aplicaciones de escritorio, aplicaciones móviles nativas ni protocolos propietarios.
- Las pruebas de SQLi y XSS son de tipo black-box sobre parámetros visibles; no realizan análisis de código fuente.
- El sistema no garantiza cobertura del 100% de vulnerabilidades existentes; los resultados deben complementarse con auditorías más profundas.
- El crawling está limitado a 3 niveles de profundidad para prevenir consumo excesivo de recursos.

### 6.2. Restricciones Legales y Éticas

- El uso del sistema sobre aplicaciones sin autorización expresa del propietario constituye infracción a la Ley N° 30096 de Delitos Informáticos del Perú.
- La interfaz incluye un aviso legal obligatorio que el usuario debe aceptar antes de iniciar cualquier escaneo.
- El sistema no almacena datos personales de terceros; los resultados de escaneos son propiedad del usuario autenticado.

### 6.3. Restricciones Técnicas

- El timeout máximo por módulo de escaneo está limitado a 60 segundos para evitar bloqueos del servidor objetivo.
- No se realizan escaneos paralelos sobre el mismo objetivo para prevenir sobrecarga.
- La API de DeepSeek requiere conexión a internet; el sistema dispone de análisis local de fallback para los tipos de vulnerabilidad más comunes (SQLi, XSS, CSRF).

<div style="page-break-after: always;"></div>

---

## 7. Rangos de Calidad

El sistema se evaluará bajo la norma **ISO/IEC 25010:2023** en las siguientes características:

| **Atributo de calidad** | **Subcaracterística** | **Criterio de aceptación** | **Referencia ISO 25010** |
|:------------------------|:----------------------|:---------------------------|:------------------------|
| Eficiencia de desempeño | Comportamiento temporal | Un escaneo completo (todos los módulos) no debe superar los 120 segundos para URLs estándar. | ISO 25010 — Performance efficiency |
| Fiabilidad | Madurez | El sistema debe completar el 95% de los escaneos sin errores fatales; los fallos deben registrarse en logs. | ISO 25010 — Reliability |
| Seguridad | Confidencialidad | Las comunicaciones frontend-backend deben cifrarse mediante HTTPS en producción. Los JWT deben tener expiración y JTI único. | ISO 25010 — Security |
| Seguridad | Integridad | Los datos de escaneos solo deben ser accesibles por el usuario propietario; el panel admin exige rol de administrador. | ISO 25010 — Security |
| Usabilidad | Capacidad de aprendizaje | Un usuario con conocimientos básicos de redes debe iniciar un escaneo sin capacitación previa. | ISO 25010 — Usability |
| Usabilidad | Operabilidad | El dashboard debe ser operable en resoluciones desde 1280x800 y responsive para tablets. | ISO 25010 — Usability |
| Mantenibilidad | Modificabilidad | La adición de nuevos módulos de escaneo debe requerir modificaciones solo en `scanner.py` y `main.py`. | ISO 25010 — Maintainability |
| Mantenibilidad | Testeabilidad | El sistema debe contar con endpoints de health check y logs estructurados para diagnóstico. | ISO 25010 — Maintainability |
| Portabilidad | Adaptabilidad | El backend debe ser desplegable en cualquier VPS Linux con Python 3.11+ y MySQL 8.0. | ISO 25010 — Portability |

<div style="page-break-after: always;"></div>

---

## 8. Precedencia y Prioridad

| **#** | **Funcionalidad** | **Prioridad** | **Entrega estimada** |
|:------|:-----------------|:-------------:|:---------------------|
| 1 | Autenticación JWT y gestión de roles | Crítica | Sprint 1 |
| 2 | Motor de escaneo: Headers, SSL, XSS, SQLi | Crítica | Sprint 1-2 |
| 3 | Motor de escaneo: CSRF, SSRF, LFI, Command Injection | Alta | Sprint 2 |
| 4 | Motor de escaneo: Open Redirect, Sensitive Files, HTTP Methods, Error Disclosure | Alta | Sprint 2 |
| 5 | Web Crawling y detección tecnológica | Media | Sprint 2 |
| 6 | Integración DeepSeek AI con fallback local | Alta | Sprint 3 |
| 7 | Dashboard SOC con gráficos en tiempo real | Alta | Sprint 3 |
| 8 | Panel de scanner interactivo con polling | Alta | Sprint 3 |
| 9 | Panel administrativo de usuarios y auditoría | Alta | Sprint 3-4 |
| 10 | Exportación de reportes PDF/HTML/JSON | Media | Sprint 4 |
| 11 | Despliegue en VPS con Nginx/systemd/PM2/UFW | Alta | Sprint 4 |

La prioridad máxima es la correcta detección de vulnerabilidades críticas, ya que constituye el valor central del sistema. La integridad y confiabilidad de los resultados no puede ser comprometida en favor de funcionalidades secundarias.

<div style="page-break-after: always;"></div>

---

## 9. Otros Requisitos del Producto

### a) Estándares Legales

- El sistema debe cumplir la **Ley N° 30096** (Ley de Delitos Informáticos del Perú), con aviso legal obligatorio previo al escaneo.
- El tratamiento de datos debe alinearse con la **Ley N° 29733** (Protección de Datos Personales del Perú).
- La herramienta debe incluir documentación explícita sobre uso ético y hacking autorizado.

### b) Estándares de Comunicación

- Toda comunicación frontend-backend debe realizarse mediante HTTPS en entornos de producción (Nginx con certificado SSL).
- La API REST sigue las convenciones RESTful y se documenta automáticamente con Swagger UI (FastAPI `/api/docs`).
- Las respuestas de error deben ser descriptivas pero no revelar información interna del sistema (stack traces ocultados en producción).

### c) Estándares de Cumplimiento de la Plataforma

- El backend debe ser compatible con Python 3.11 o superior.
- El frontend debe compilar correctamente con Node.js 20 LTS y Next.js 16.
- El sistema debe funcionar correctamente en Chrome 120+, Firefox 120+ y Edge 120+.
- La base de datos MySQL debe ejecutarse en versión 8.0 o superior con el charset `utf8mb4`.

### d) Estándares de Calidad y Seguridad

- El código Python debe seguir las convenciones **PEP 8**; el TypeScript debe seguir las convenciones de ESLint configuradas en el proyecto.
- Las dependencias deben auditarse antes de cada entrega con `pip audit` (backend) y `npm audit` (frontend).
- El repositorio debe incluir un `README.md` con instrucciones de instalación, configuración y ejecución.
- Todas las contraseñas deben almacenarse con **bcrypt** (cost factor ≥ 10); los tokens JWT deben firmarse con `HS256` y tener expiración de 24 horas.
- Las variables sensibles (DATABASE_URL, SECRET_KEY, DEEPSEEK_API_KEY) deben gestionarse mediante variables de entorno en `.env` nunca commiteadas al repositorio.

---

## Conclusiones

El proyecto **VulnScan Pro — Analizador de Vulnerabilidades Web** se establece como una solución técnica innovadora y viable que eleva el estándar de calidad en el desarrollo de software dentro de la Universidad Privada de Tacna. A través de una arquitectura moderna (FastAPI + MySQL + Next.js) y 13 módulos de escaneo alineados con el OWASP Top 10, potenciados por inteligencia artificial (DeepSeek), el sistema provee a estudiantes, ingenieros de QA y PYMES de la región una herramienta profesional gratuita para identificar vulnerabilidades web antes del despliegue.

El documento de visión define con claridad el alcance funcional (20 características), los interesados, los perfiles de usuario, las restricciones legales y técnicas, y los estándares de calidad bajo los cuales será evaluado el sistema (ISO/IEC 25010), garantizando un desarrollo alineado con las expectativas académicas y las buenas prácticas de ingeniería de software seguro.

---

## Recomendaciones

- **Integración CI/CD:** Incorporar VulnScan Pro como paso de seguridad en pipelines de GitHub Actions, transformándola en una herramienta DevSecOps nativa.
- **Ampliación de módulos:** Incorporar detección de componentes con vulnerabilidades conocidas (A06:2021 — Vulnerable Components) cruzando hallazgos con la base de datos NVD.
- **Actualización de payloads:** Establecer un proceso periódico de actualización de los payloads de XSS y SQLi para mantener efectividad frente a nuevas técnicas de evasión.
- **Autenticación multifactor (MFA):** Añadir un segundo factor (TOTP) para cuentas administrativas en entornos con datos sensibles.
- **Escalado horizontal:** Diseñar la capa de escaneo para soporte de múltiples workers en cola (Celery + Redis) cuando el volumen de escaneos concurrentes supere la capacidad del servidor actual.

---

## Bibliografía

OWASP Foundation. (2025). *OWASP Top 10 Project*. Recuperado de https://owasp.org/Top10/

ISO/IEC 25010:2023. (2023). *Systems and software engineering — System and software quality models*. International Organization for Standardization.

McKinley, T. (2022). *Web Application Security: Exploitation and Countermeasures for Modern Web Applications*. O'Reilly Media.

NIST. (2024). *National Vulnerability Database (NVD)*. Recuperado de https://nvd.nist.gov

Stuttard, D., & Pinto, M. (2023). *The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws* (2nd ed.). Wiley.

---

## Webgrafía

FastAPI Documentation. (2025). *FastAPI Framework*. Recuperado de https://fastapi.tiangolo.com

Next.js Documentation. (2025). *Next.js — The React Framework*. Recuperado de https://nextjs.org/docs

DeepSeek AI. (2025). *DeepSeek API Documentation*. Recuperado de https://api.deepseek.com/docs

Tailwind CSS Documentation. (2025). Recuperado de https://tailwindcss.com/docs

Python Software Foundation. (2025). *Python 3.11 Documentation*. Recuperado de https://docs.python.org/3.11/

Ley N° 30096 — Ley de Delitos Informáticos. (2013). Congreso de la República del Perú. Recuperado de https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/139699-30096

---

*Documento elaborado por el equipo de desarrollo — Curso Calidad y Pruebas de Software — UPT — 2026*
