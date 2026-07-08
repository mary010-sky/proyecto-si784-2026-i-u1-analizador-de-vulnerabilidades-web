<center>

![Logo UPT](media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Informe Final**

**Proyecto *Analizador de Vulnerabilidades Web — VulnScan Pro***

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

| CONTROL DE VERSIONES | | | | | |
|:---:|:---|:---|:---|:---|:---|
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| 1.0 | M. Calloticona | M. Ramos | | 04/04/2026 | Versión Original |

<div style="page-break-after: always;"></div>

---

## INDICE GENERAL

1. [Antecedentes](#1-antecedentes)
2. [Planteamiento del Problema](#2-planteamiento-del-problema)
   - a. [Problema](#a-problema)
   - b. [Justificación](#b-justificación)
   - c. [Alcance](#c-alcance)
3. [Objetivos](#3-objetivos)
4. [Marco Teórico](#4-marco-teórico)
5. [Desarrollo de la Solución](#5-desarrollo-de-la-solución)
   - a. [Análisis de Factibilidad](#a-análisis-de-factibilidad-técnica-económica-operativa-social-legal-ambiental)
   - b. [Tecnología de Desarrollo](#b-tecnología-de-desarrollo)
   - c. [Metodología de implementación](#c-metodología-de-implementación-documento-de-visión-srs-sad)
6. [Cronograma](#6-cronograma)
7. [Presupuesto](#7-presupuesto)
8. [Conclusiones](#8-conclusiones)

[Recomendaciones](#recomendaciones)

[Bibliografía](#bibliografía)

[Anexos](#anexos)

<div style="page-break-after: always;"></div>

---

## Informe Final

---

## 1. Antecedentes

En la actualidad, las aplicaciones web desarrolladas en entornos académicos y por PYMES de la región Tacna suelen desplegarse con configuraciones de seguridad deficientes: cabeceras HTTP ausentes, certificados SSL vencidos, formularios vulnerables a inyección SQL, cookies sin flags de protección y archivos de configuración sensibles expuestos públicamente (`.env`, `.git`, `phpinfo.php`). Según el OWASP Top 10:2021, más del 94% de las aplicaciones web presentan al menos una vulnerabilidad de la lista, siendo SQL Injection, XSS y cabeceras inseguras las más prevalentes.

La causa principal de esta situación es la falta de herramientas de auditoría de seguridad accesibles. Las soluciones profesionales existentes en el mercado —Burp Suite Professional (USD 449/año), Nessus Professional (USD 3,590/año), Acunetix (USD 4,500/año) y Qualys WAS (USD 2,995/año)— tienen costos que las hacen inaccesibles para estudiantes universitarios, desarrolladores independientes y pequeñas empresas locales. A ello se suma que estas herramientas operan íntegramente en inglés y no ofrecen análisis contextualizado del impacto de cada hallazgo.

Frente a este panorama, el equipo del curso de Calidad y Pruebas de Software de la Escuela Profesional de Ingeniería de Sistemas (EPIS) de la Universidad Privada de Tacna (UPT) propuso el desarrollo de **VulnScan Pro**, una plataforma DAST (Dynamic Application Security Testing) gratuita, en español y potenciada por inteligencia artificial, capaz de ofrecer capacidades equivalentes a las herramientas comerciales mencionadas, democratizando el acceso a la ciberseguridad en el ecosistema académico y empresarial de la región.

El proyecto se desarrolló durante el semestre académico 2026-I, entre marzo y abril de 2026, y su proceso completo —desde el estudio de factibilidad hasta el despliegue en producción— se documentó en cinco entregables formales: Informe de Factibilidad (FD01), Documento de Visión (FD02), Especificación de Requerimientos de Software / SRS (FD03), Documento de Arquitectura de Software / SAD (FD04) y el presente Informe Final (FD05).

<div style="page-break-after: always;"></div>

---

## 2. Planteamiento del Problema

### a. Problema

| | |
|:--|:--|
| **El problema de:** | La falta de herramientas de auditoría de seguridad web accesibles, gratuitas y en español |
| **Que afecta a:** | Estudiantes de ingeniería, desarrolladores independientes, equipos de QA y PYMES de Tacna |
| **El impacto del cual es:** | Aplicaciones web con vulnerabilidades conocidas (SQL Injection, XSS, CSRF, archivos sensibles expuestos) desplegadas en producción, expuestas a ataques automatizados |
| **Una solución exitosa sería:** | Una plataforma web DAST gratuita, multi-módulo OWASP Top 10, con análisis de inteligencia artificial y reportes exportables para auditoría formal |

### b. Justificación

La inversión en el desarrollo de VulnScan Pro se justifica por los siguientes factores:

- **Brecha de acceso económico:** las herramientas DAST comerciales cuestan entre USD 449 y USD 4,500 anuales, montos inalcanzables para estudiantes y PYMES de Tacna. VulnScan Pro ofrece capacidades equivalentes con una inversión efectiva de solo **S/. 148.05**.
- **Prevalencia real del problema:** el 94% de las aplicaciones web presenta al menos una vulnerabilidad del OWASP Top 10:2021, por lo que la necesidad de un mecanismo de detección accesible es vigente y medible.
- **Valor educativo:** al ser desarrollado y usado en el entorno académico de la EPIS-UPT, el sistema forma a la próxima generación de ingenieros en prácticas de *Security by Design* y hacking ético defensivo.
- **Retorno financiero comprobado:** el análisis financiero determinó una relación Beneficio/Costo de **35.2**, un VAN de **S/. 12,355.88** y una TIR muy superior al costo de oportunidad del capital (12%), confirmando que el proyecto es ampliamente rentable incluso en términos estrictamente monetarios.
- **Cumplimiento normativo:** el sistema fue diseñado desde el inicio para cumplir la Ley N° 30096 (Delitos Informáticos) y la Ley N° 29733 (Protección de Datos Personales) del Perú, evitando cualquier ambigüedad legal en su uso.

### c. Alcance

**Dentro del alcance:** motor DAST con 13 módulos OWASP Top 10:2021 (SQL Injection, XSS, CSRF, SSRF, LFI, Command Injection, Open Redirect, Security Headers, SSL/TLS, Sensitive Files, HTTP Methods, Error Disclosure, Web Crawling), autenticación JWT multi-rol (Administrador / Analista / Usuario), integración con DeepSeek AI para análisis contextualizado de cada vulnerabilidad, generación de reportes en PDF/HTML/JSON, dashboard SOC (Security Operations Center) en tiempo real, panel administrativo, auditoría completa de accesos y despliegue automatizado en VPS Linux (Nginx + systemd + PM2 + UFW).

**Fuera del alcance:** análisis estático de código fuente (SAST), pruebas de infraestructura de red, análisis de aplicaciones móviles, pruebas de APIs GraphQL, integración CI/CD y soporte multi-tenant. Estas capacidades quedan identificadas como trabajo futuro en las recomendaciones del proyecto.

<div style="page-break-after: always;"></div>

---

## 3. Objetivos

### Objetivo General

Desarrollar una plataforma web integral de análisis de vulnerabilidades de seguridad que permita a equipos de desarrollo e ingeniería de calidad identificar, priorizar y remediar brechas de seguridad en aplicaciones web mediante un motor de escaneo OWASP Top 10 potenciado por inteligencia artificial, desplegado en infraestructura VPS Linux de producción.

### Objetivos Específicos

1. Implementar un motor de escaneo multimódulo capaz de detectar las 13 categorías de vulnerabilidades más críticas del OWASP Top 10: SQL Injection (error-based y blind), XSS reflejado, CSRF, SSRF, LFI/Path Traversal, Command Injection, Open Redirect, cabeceras HTTP inseguras, SSL/TLS deficiente, archivos sensibles expuestos, métodos HTTP peligrosos y divulgación de errores.
2. Desarrollar un sistema de autenticación robusto con roles Admin/Analista/Usuario, protección anti-fuerza bruta (bloqueo automático tras 5 intentos fallidos por 15 minutos), sesiones JWT con JTI único, registro de auditoría completo y gestión de usuarios desde panel administrativo.
3. Integrar DeepSeek AI para análisis automático por vulnerabilidad: puntuación CVSS (0-10), identificador CWE, escenario de ataque, código de remediación adaptado al stack tecnológico del objetivo y reporte ejecutivo de riesgo global con risk score (0-100).
4. Construir un dashboard SOC en Next.js 16 con estadísticas en tiempo real, gráficos interactivos (Chart.js), escáner con configuración avanzada (profundidad, timeout, stack, IA), polling automático del estado del escaneo y panel de administración.
5. Desplegar el sistema en producción sobre VPS Linux (149.34.48.176) con Nginx como proxy reverso, systemd para el backend (Gunicorn 4 workers), PM2 para el frontend, UFW firewall y MySQL 8.0 nativo, mediante un script `deploy.sh` que automatiza toda la instalación en un solo comando.

<div style="page-break-after: always;"></div>

---

## 4. Marco Teórico

El desarrollo de VulnScan Pro se sustenta en los siguientes conceptos, estándares y marcos normativos:

**DAST (Dynamic Application Security Testing):** metodología de pruebas de seguridad que analiza una aplicación en tiempo de ejecución, sin acceso al código fuente, simulando el comportamiento de un atacante externo. Es el paradigma sobre el que se construye el motor de escaneo del sistema.

**OWASP Top 10:2021:** lista de las diez categorías de vulnerabilidades web más críticas, publicada por la Open Web Application Security Project (OWASP). VulnScan Pro implementa 13 módulos de detección alineados con estas categorías (A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection, A05 Security Misconfiguration, A10 SSRF, entre otras).

**CVSS v3.1 (Common Vulnerability Scoring System):** estándar internacional para calificar la severidad de una vulnerabilidad en una escala de 0.0 a 10.0. El módulo de inteligencia artificial de VulnScan Pro calcula un puntaje y vector CVSS para cada hallazgo.

**CWE (Common Weakness Enumeration):** catálogo estándar de tipos de debilidades de software (p. ej. CWE-89 para SQL Injection, CWE-79 para XSS). Se utiliza para clasificar y documentar cada vulnerabilidad detectada.

**JWT (JSON Web Token) — RFC 7519:** estándar abierto para la transmisión segura de información de autenticación mediante tokens firmados digitalmente. El sistema usa JWT con algoritmo HS256, expiración de 24 horas e identificador JTI único por sesión.

**RBAC (Role-Based Access Control):** modelo de control de acceso en el que los permisos se asignan según el rol del usuario (Administrador, Analista, Usuario), implementado en la capa de autorización de la API.

**ISO/IEC 25010:2011 (SQuaRE):** modelo internacional de calidad de software utilizado para evaluar el sistema en las dimensiones de funcionalidad, rendimiento, usabilidad, confiabilidad, seguridad, mantenibilidad y portabilidad.

**Modelo de vistas 4+1 (Kruchten, 1995):** marco de referencia arquitectónico utilizado en el Documento de Arquitectura de Software (SAD) para describir el sistema desde cinco perspectivas complementarias: caso de uso, lógica, implementación, procesos y despliegue.

**Marco legal peruano:** Ley N° 30096 — Ley de Delitos Informáticos, que exige contar con autorización expresa antes de realizar pruebas de seguridad sobre un sistema de terceros; y Ley N° 29733 — Ley de Protección de Datos Personales, que rige el tratamiento de la información gestionada por la plataforma.

<div style="page-break-after: always;"></div>

---

## 5. Desarrollo de la Solución

### a. Análisis de Factibilidad (técnica, económica, operativa, social, legal, ambiental)

El Informe de Factibilidad (Anexo 01) determinó que el proyecto es viable en las seis dimensiones evaluadas:

| **Dimensión** | **Resultado** |
|:--------------|:--------------|
| Técnica | **4.83/5.** El equipo domina el stack (Python, TypeScript, SQL); la arquitectura es desacoplada y escalable; la infraestructura VPS ya estaba activa y disponible. |
| Económica | **Inversión efectiva de S/. 148.05.** Stack 100% open source (MIT/BSD/Apache/GPL) y DeepSeek AI en su capa gratuita; los únicos costos reales son operativos (energía, internet, VPS). |
| Operativa | **Beneficios directos para todos los stakeholders:** docente, estudiantes, ingenieros de QA, PYMES de Tacna y auditores de TI. El sistema opera de forma autónoma con reinicio automático (systemd). |
| Legal | **Cumplimiento de la Ley N° 30096 y la Ley N° 29733.** Aviso legal obligatorio antes de cada escaneo; licenciamiento MIT; disclaimer de responsabilidad. |
| Social | **Democratización de la ciberseguridad** en la región Tacna, formación en cultura de hacking ético y reducción de la brecha digital en seguridad entre grandes corporaciones y organizaciones locales. |
| Ambiental | **Alineación con Green IT:** FastAPI y Next.js son eficientes en consumo de CPU/memoria; distribución 100% digital sin residuos físicos; infraestructura compartida en VPS. |

### b. Tecnología de Desarrollo

VulnScan Pro se construyó sobre una arquitectura de tres capas desacopladas:

```
PRESENTACIÓN: Next.js 16 + TypeScript + TailwindCSS
   Dashboard SOC, Escáner, Admin, Reportes — PM2, puerto 3000
NEGOCIO: FastAPI + Python 3.11 + Gunicorn (4 workers)
   13 módulos OWASP + Autenticación JWT + DeepSeek AI — systemd, puerto 8000
DATOS: MySQL 8.0 + SQLAlchemy 2.0 (QueuePool)
   7 modelos: User, UserSession, Scan, Vulnerability, AuditLog, Report, PasswordReset
INFRAESTRUCTURA: Nginx + UFW + Ubuntu 22.04 LTS
   IP: 149.34.48.176 — Rate limiting + TLS + Security Headers
```

**Stack tecnológico principal:** Python 3.11 y FastAPI 0.110+ para la API REST asíncrona; SQLAlchemy 2.0 y PyMySQL para el acceso a datos; python-jose y bcrypt/passlib para la seguridad de autenticación; WeasyPrint para la generación de reportes PDF; Next.js 16 (App Router), TypeScript y TailwindCSS para el frontend; Chart.js para las visualizaciones del dashboard; DeepSeek AI (modelo `deepseek-chat`) para el análisis inteligente de vulnerabilidades; y Nginx, PM2, systemd y UFW para la infraestructura de producción. El detalle completo de versiones, licencias y costos de cada tecnología se documenta en el Anexo 01 (Informe de Factibilidad).

### c. Metodología de implementación (Documento de VISION, SRS, SAD)

El proyecto siguió una metodología documental secuencial alineada con las buenas prácticas de ingeniería de software, en la que cada entregable formal alimenta al siguiente:

1. **Informe de Factibilidad (FD01):** estableció la viabilidad técnica, económica, operativa, legal, social y ambiental del proyecto antes de iniciar cualquier desarrollo (Semana 1, Fase 1).
2. **Documento de Visión (FD02):** definió el posicionamiento del producto, los stakeholders, las características del sistema (12 características CRQ), las restricciones y los rangos de calidad ISO/IEC 25010, sirviendo como marco de referencia compartido por todo el equipo.
3. **Especificación de Requerimientos de Software / SRS (FD03):** tradujo la Visión en 67 requerimientos funcionales, 30 requerimientos no funcionales y 18 reglas de negocio, junto con 13 casos de uso completamente narrados y sus respectivos diagramas de secuencia y de clases.
4. **Documento de Arquitectura de Software / SAD (FD04):** aplicó el modelo de vistas 4+1 (Kruchten) para representar la arquitectura desde las perspectivas de caso de uso, vista lógica, vista de implementación, vista de procesos y vista de despliegue, y documentó los atributos de calidad del software mediante escenarios concretos (funcionalidad, usabilidad, confiabilidad, rendimiento y mantenibilidad).
5. **Implementación y despliegue:** el desarrollo se ejecutó en 4 fases semanales (arquitectura y setup; backend y motor de escaneo; frontend y dashboard; IA, reportes y despliegue), culminando con el despliegue automatizado en el VPS de producción mediante `deploy.sh`.

Esta metodología documental garantiza la trazabilidad completa entre la necesidad de negocio (Visión), los requerimientos (SRS) y la solución técnica implementada (SAD), facilitando la evaluación académica y la mantenibilidad futura del sistema.

<div style="page-break-after: always;"></div>

---

## 6. Cronograma

El proyecto se desarrolló en un plazo total de **4 semanas (1 mes)**, entre marzo y abril de 2026:

| **Fase** | **Duración** | **Actividades Clave** |
|:---------|:------------|:----------------------|
| Fase 1: Arquitectura y Setup | Semana 1 | Definición de arquitectura, configuración VPS (149.34.48.176), MySQL, FastAPI, Next.js, estructura de carpetas y control de versiones. |
| Fase 2: Backend y Motor de Escaneo | Semana 2 | Implementación de los 13 módulos OWASP Top 10: XSS, SQLi, CSRF, SSRF, LFI, Command Injection, Open Redirect, Headers, SSL, Archivos Sensibles, HTTP Methods, Error Disclosure, Crawling. API REST con JWT. |
| Fase 3: Frontend y Dashboard SOC | Semana 3 | Dashboard con gráficos Chart.js, escáner interactivo con polling en tiempo real, panel de administración, autenticación con roles. |
| Fase 4: IA, Reportes y Despliegue | Semana 4 | Integración DeepSeek AI, generación PDF/HTML/JSON, script deploy.sh, Nginx, systemd, PM2, UFW. Pruebas finales. |

<div style="page-break-after: always;"></div>

---

## 7. Presupuesto

El proyecto, al ser de carácter académico, presenta una inversión efectiva mínima gracias al uso de tecnologías 100% open source:

| **Categoría** | **Monto Efectivo (S/.)** | **Monto Referencial (S/.)** |
|:--------------|:------------------------:|:---------------------------:|
| Costos Generales | S/. 45.00 | S/. 45.00 |
| Costos Operativos (1 mes) | S/. 96.00 | S/. 96.00 |
| Costos de Software y Licencias | S/. 0.00 | S/. 0.00 |
| Personal (referencial — no erogado) | S/. 0.00 | S/. 2,400.00 |
| Imprevistos (5%) | S/. 7.05 | S/. 127.05 |
| **INVERSIÓN TOTAL** | **S/. 148.05** | **S/. 2,668.05** |

El detalle desagregado de cada categoría de costo (papel e impresión, energía eléctrica, alquiler de VPS, horas de personal por integrante, etc.) se documenta en la sección 4.2 del Informe de Factibilidad (Anexo 01).

<div style="page-break-after: always;"></div>

---

## 8. Conclusiones

1. El proyecto **VulnScan Pro — Analizador de Vulnerabilidades Web** cumplió satisfactoriamente sus objetivos general y específicos, entregando una plataforma DAST funcional, desplegada en producción, con 13 módulos de escaneo OWASP Top 10, análisis de inteligencia artificial y reportes exportables.
2. El análisis de factibilidad confirmó la viabilidad del proyecto en las seis dimensiones evaluadas, destacando la factibilidad técnica (4.83/5) y económica (inversión efectiva de S/. 148.05 frente a herramientas comerciales de hasta USD 4,500/año).
3. Los indicadores financieros son excepcionales: **B/C = 35.2**, **VAN = S/. 12,355.88** (positivo) y **TIR muy superior al 3,400%**, muy por encima del costo de oportunidad del capital (12%), validando ampliamente la inversión realizada.
4. La metodología documental secuencial (Factibilidad → Visión → SRS → SAD) garantizó trazabilidad completa entre la necesidad de negocio, los 67 requerimientos funcionales especificados y la arquitectura de software implementada bajo el modelo de vistas 4+1.
5. La integración de DeepSeek AI diferencia a VulnScan Pro de herramientas académicas convencionales, proporcionando análisis contextualizado (CVSS, CWE, escenario de ataque y código de remediación por stack tecnológico) que incrementa significativamente su utilidad práctica.
6. El sistema cumple estrictamente con el marco legal peruano (Ley N° 30096 y Ley N° 29733), adoptando un enfoque ético de hacking defensivo con mecanismos que previenen activamente el uso indebido de la plataforma.

---

## Recomendaciones

1. Extender los módulos de escaneo a la OWASP API Security Top 10 en versiones futuras, cubriendo APIs REST y GraphQL.
2. Implementar un sistema de notificaciones automáticas (email o webhook) al completar un escaneo, reduciendo la necesidad de polling manual.
3. Ampliar los módulos de escaneo en versiones futuras para cubrir vulnerabilidades adicionales del panorama OWASP (p. ej. CORS Misconfiguration, deserialización insegura).
4. Considerar la integración con pipelines CI/CD (GitHub Actions) para habilitar el escaneo automático en cada despliegue.
5. Publicar la experiencia del proyecto como caso de estudio en la revista académica de la EPIS-UPT, y evaluar su réplica por otros grupos de la universidad.

---

## Bibliografía

- OWASP Foundation (2021). *OWASP Top Ten*. https://owasp.org/Top10/
- ISO/IEC (2011). *ISO/IEC 25010:2011 — SQuaRE*. International Standards Organization.
- FIRST.org (2019). *CVSS v3.1 Specification Document*.
- Ramírez, S. (2023). *FastAPI documentation*. https://fastapi.tiangolo.com/
- Vercel Inc. (2024). *Next.js 16 Documentation*. https://nextjs.org/docs
- DeepSeek AI (2024). *DeepSeek API Reference*. https://platform.deepseek.com/api-docs
- Congreso de la República del Perú (2013). *Ley N° 30096 — Ley de Delitos Informáticos*.
- Congreso de la República del Perú (2011). *Ley N° 29733 — Ley de Protección de Datos Personales*.
- Kruchten, P. (1995). *Architectural Blueprints — The "4+1" View Model of Software Architecture*. IEEE Software.
- Pressman, R. (2010). *Ingeniería del Software: Un Enfoque Práctico* (7ª ed.). McGraw-Hill.

<div style="page-break-after: always;"></div>

---

## Anexos

**Anexo 01** Informe de Factibilidad — *FD01-Factibilidad-Ramos-Calloticona*

**Anexo 02** Documento de Visión — *FD02-Vision-Ramos-Calloticona*

**Anexo 03** Documento SRS (Especificación de Requerimientos de Software) — *FD03-Requerimientos-Ramos-Calloticona*

**Anexo 04** Documento SAD (Documento de Arquitectura de Software) — *FD04-Arquitectura-Ramos-Calloticona*

**Anexo 05** Manuales y otros documentos — scripts de despliegue (`deploy.sh`), configuración de infraestructura (Nginx, systemd, UFW) y evidencias de ejecución en el VPS de producción (149.34.48.176)

---

*Documento elaborado por: Calloticona Chambilla, Marymar D. y Ramos Loza, Mariela Estefany*
*Curso: Calidad y Pruebas de Software — Docente: Ing. Patrick Jose Cuadros Quiroga — UPT — 2026*
