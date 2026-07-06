<center>

![Logo UPT](media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Propuesta del Proyecto *Analizador de Vulnerabilidades Web — VulnScan Pro***

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

**Proyecto**

***VulnScan Pro — Analizador de Vulnerabilidades Web, Tacna, 2026***

**Presentado por:**

***Calloticona Chambilla, Marymar D. y Ramos Loza, Mariela Estefany***

***Estudiantes de la Escuela Profesional de Ingeniería de Sistemas — UPT***

***04 de abril de 2026***

<div style="page-break-after: always;"></div>

---

| CONTROL DE VERSIONES | | | | | |
|:---:|:---|:---|:---|:---|:---|
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| 1.0 | M. Calloticona | M. Ramos | | 04/04/2026 | Versión Original |

<div style="page-break-after: always;"></div>

---

# Tabla de contenido

Resumen Ejecutivo

**I Propuesta narrativa**

1. Planteamiento del Problema
2. Justificación del proyecto
3. Objetivo general
4. Beneficios
5. Alcance
6. Requerimientos del sistema
7. Restricciones
8. Supuestos
9. Resultados esperados
10. Metodología de implementación
11. Actores claves
12. Papel y responsabilidades del personal
13. Plan de monitoreo y evaluación
14. Cronograma del proyecto
15. Hitos de entregables

**II Presupuesto**

1. Planteamiento de aplicación del presupuesto
2. Presupuesto
3. Análisis de Factibilidad
4. Evaluación Financiera

Anexo 01 — Requerimientos del Sistema *VulnScan Pro*

<div style="page-break-after: always;"></div>

---

## RESUMEN EJECUTIVO

| **Nombre del Proyecto propuesto**: | |
|:-------------------------------------------------------|:--------------------------------------|
| *VulnScan Pro — Analizador de Vulnerabilidades Web, Tacna, 2026* | |
| **Propósito del Proyecto y Resultados esperados:** | |
| El propósito del proyecto es desarrollar y desplegar una plataforma web de análisis dinámico de seguridad (DAST) gratuita, en español y potenciada por inteligencia artificial, que permita a estudiantes, desarrolladores y PYMES de Tacna identificar y remediar vulnerabilidades OWASP Top 10 en sus aplicaciones web. | |
| Los resultados esperados son: | |
| - Un motor de escaneo funcional con 13 módulos OWASP Top 10:2021. | |
| - Un sistema de autenticación multi-rol (Admin/Analista/Usuario) con auditoría completa. | |
| - Integración de DeepSeek AI para análisis contextualizado de cada vulnerabilidad detectada. | |
| - Reportes exportables en PDF, HTML y JSON, y un dashboard SOC en tiempo real. | |
| - Despliegue en producción sobre VPS Linux con instalación automatizada de un solo comando. | |
| **Población Objetivo:** | |
| Estudiantes de la EPIS-UPT, desarrolladores independientes, ingenieros de QA y PYMES de la región Tacna que requieren diagnósticos de seguridad web sin costo de licenciamiento. | |
| **Monto de Inversión (En Soles):** | **Duración del Proyecto (En Meses):** |
| ***S/. 148.05*** (efectivo) / *S/. 2,668.05* (referencial) | ***1 mes (4 semanas)*** |

<div style="page-break-after: always;"></div>

---

## I. Propuesta narrativa

### 1. Planteamiento del Problema

| | |
|:--|:--|
| **El problema de:** | La falta de herramientas de auditoría de seguridad web accesibles, gratuitas y en español |
| **Que afecta a:** | Estudiantes de ingeniería, desarrolladores independientes, equipos de QA y PYMES de Tacna |
| **El impacto del cual es:** | Aplicaciones web con vulnerabilidades conocidas (SQL Injection, XSS, CSRF, archivos sensibles expuestos) desplegadas en producción, expuestas a ataques automatizados crecientes. Según el OWASP Top 10:2021, más del 94% de las aplicaciones web presenta al menos una vulnerabilidad de la lista |
| **Una solución exitosa sería:** | Una plataforma web DAST gratuita, multi-módulo OWASP, con análisis de inteligencia artificial y reportes exportables para auditoría formal |

Las alternativas comerciales existentes —Burp Suite Professional (USD 449/año), Nessus Professional (USD 3,590/año), Acunetix (USD 4,500/año) y Qualys WAS (USD 2,995/año)— son inaccesibles económicamente para el segmento objetivo y operan íntegramente en inglés, sin análisis contextualizado del impacto de cada hallazgo.

### 2. Justificación del proyecto

- **Brecha de acceso económico:** el costo de las herramientas DAST comerciales es entre 10 y 100 veces superior a la inversión efectiva requerida para VulnScan Pro (S/. 148.05).
- **Prevalencia real y medible del problema:** el 94% de las aplicaciones web presenta al menos una vulnerabilidad del OWASP Top 10:2021.
- **Valor educativo y formativo:** el desarrollo y uso del sistema en el entorno académico de la EPIS-UPT forma a los estudiantes en prácticas de *Security by Design* y hacking ético defensivo.
- **Retorno financiero verificado:** el análisis financiero (Anexo 01 del Informe de Factibilidad) determinó B/C = 35.2, VAN = S/. 12,355.88 y una TIR muy superior al costo de oportunidad del capital (12%).
- **Cumplimiento normativo desde el diseño:** el sistema incorpora desde su concepción el cumplimiento de la Ley N° 30096 (Delitos Informáticos) y la Ley N° 29733 (Protección de Datos Personales) del Perú.

### 3. Objetivo general

Desarrollar una plataforma web integral de análisis de vulnerabilidades de seguridad que permita a equipos de desarrollo e ingeniería de calidad identificar, priorizar y remediar brechas de seguridad en aplicaciones web mediante un motor de escaneo OWASP Top 10 potenciado por inteligencia artificial, desplegado en infraestructura VPS Linux de producción.

### 4. Beneficios

**Beneficios tangibles (cuantificables):**

| **Beneficio** | **Valor estimado anual (S/.)** |
|:--------------|:------------------------------:|
| Ahorro en licencias de herramientas equivalentes (Burp Suite: USD 449 ≈ S/. 1,706/año) | S/. 1,706.00 |
| Reducción de tiempo en detección de vulnerabilidades (de 2 días a 5 minutos → 4 h/semana × S/. 15/h × 50 semanas) | S/. 3,000.00 |
| Prevención de incidentes de seguridad en proyectos académicos (costo estimado de un incidente: S/. 500) | S/. 500.00 |
| **Total beneficios tangibles anuales** | **S/. 5,206.00** |

**Beneficios intangibles:**

- Elevación del estándar de calidad de software en la EPIS-UPT.
- Formación práctica en ciberseguridad del equipo de desarrollo.
- Mejora en la reputación del proyecto ante el mercado laboral.
- Contribución al ecosistema de seguridad digital de la región Tacna.
- Disponibilidad de una herramienta open source replicable por otros grupos de la universidad.

### 5. Alcance

**Dentro del alcance:** motor DAST con 13 módulos OWASP Top 10:2021, autenticación JWT multi-rol (Administrador/Analista/Usuario), integración con DeepSeek AI, reportes exportables en PDF/HTML/JSON, dashboard SOC en tiempo real, panel administrativo, auditoría completa de accesos y despliegue automatizado en VPS Linux.

**Fuera del alcance:** análisis estático de código fuente (SAST), pruebas de infraestructura de red, análisis de aplicaciones móviles, pruebas de APIs GraphQL, integración CI/CD y soporte multi-tenant.

### 6. Requerimientos del sistema

El sistema fue especificado formalmente en el Documento SRS (67 requerimientos funcionales, 30 requerimientos no funcionales y 18 reglas de negocio — ver Anexo 01). Los requerimientos de infraestructura mínimos y recomendados son:

| **Componente** | **Mínimo** | **Recomendado** |
|:---------------|:----------:|:---------------:|
| Servidor | 1 vCPU, 2 GB RAM, Ubuntu 22.04 | 2 vCPU, 4 GB RAM, Ubuntu 22.04 |
| Almacenamiento | 20 GB SSD | 50 GB SSD |
| Navegador cliente | Chrome 120+ / Firefox 120+ | Chrome 125+ |

**Requerimientos de rendimiento:** inicio de escaneo (POST `/scans`) < 500 ms; polling de estado (GET `/scans/{id}`) < 200 ms; generación de reporte PDF < 10 s (hasta 50 vulnerabilidades); carga del dashboard < 3 s en conexión de 10 Mbps.

### 7. Restricciones

| **#** | **Restricción** | **Tipo** |
|:-----:|:----------------|:--------:|
| RES-01 | Uso autorizado únicamente; aviso legal obligatorio antes de escanear | Legal/Ética |
| RES-02 | Sin escaneos destructivos; los módulos son de solo lectura | Técnica |
| RES-03 | Un escaneo activo por usuario, para proteger los recursos del VPS | Técnica |
| RES-04 | Timeout máximo de 60 s por módulo (configurable 5-60 s) | Técnica |
| RES-05 | Objetivo HTTP/HTTPS únicamente; sin escaneo de IPs privadas | Técnica |
| RES-06 | Backend Python 3.11+ (incompatible con versiones ≤ 3.9) | Técnica |
| RES-07 | Despliegue solo en Linux (Ubuntu 22.04 LTS) | Técnica |
| RES-08 | Resultados orientativos; no reemplaza una auditoría profesional manual | Técnica |
| RSTR-01 | VPS Linux de 2 vCPU / 4 GB RAM, lo que limita la concurrencia máxima | Infraestructura |
| RSTR-05 | Proyecto académico con inversión efectiva ≤ S/. 200 | Económica |
| RSTR-08 | Desarrollo en 4 semanas por un equipo de 2 desarrolladoras | Tiempo |

### 8. Supuestos

- El usuario final posee autorización legal expresa sobre las aplicaciones que decide escanear.
- La API de DeepSeek AI se encuentra disponible para el análisis inteligente (se implementó un mecanismo de fallback local en caso de indisponibilidad).
- El VPS Ubuntu 22.04 LTS contratado permanece activo con conectividad continua durante el desarrollo y la operación del sistema.
- El equipo de desarrollo cuenta con el conocimiento técnico necesario en Python, TypeScript y SQL para ejecutar el proyecto sin capacitación adicional.

### 9. Resultados esperados

- Motor de escaneo con los 13 módulos OWASP Top 10 operativos, detectando al menos el 85% de las vulnerabilidades reales en sitios de prueba, con tasa de falsos positivos menor al 15%.
- Sistema de autenticación JWT multi-rol con bloqueo automático anti-fuerza bruta y auditoría del 100% de las acciones relevantes.
- Módulo de inteligencia artificial (DeepSeek) entregando puntuación CVSS, identificador CWE, escenario de ataque y código de remediación por stack tecnológico en el 100% de los análisis.
- Dashboard SOC con actualización de estadísticas cada 60 segundos y polling de estado de escaneo cada 3 segundos.
- Reportes exportables (PDF/HTML/JSON) generados en menos de 10 segundos para escaneos de hasta 50 vulnerabilidades.
- Sistema desplegado en producción con disponibilidad (uptime) mensual igual o superior al 99.5%.
- Retorno financiero con B/C = 35.2, VAN = S/. 12,355.88 y TIR muy superior al costo de oportunidad del capital.

### 10. Metodología de implementación

El proyecto sigue una metodología documental secuencial en la que cada entregable formal alimenta al siguiente:

1. **Informe de Factibilidad (FD01):** valida la viabilidad técnica, económica, operativa, legal, social y ambiental antes de iniciar el desarrollo.
2. **Documento de Visión (FD02):** define el posicionamiento del producto, los stakeholders, las 12 características del sistema (CRQ-01 a CRQ-12), las restricciones y los rangos de calidad ISO/IEC 25010.
3. **Documento SRS (FD03):** traduce la Visión en 67 requerimientos funcionales, 30 requerimientos no funcionales, 18 reglas de negocio y 13 casos de uso con sus diagramas de secuencia y de clases.
4. **Documento SAD (FD04):** aplica el modelo de vistas 4+1 (Kruchten) para representar la arquitectura del sistema y documenta los atributos de calidad mediante escenarios concretos.
5. **Implementación en 4 fases semanales:** arquitectura y setup → backend y motor de escaneo → frontend y dashboard SOC → inteligencia artificial, reportes y despliegue en producción.

### 11. Actores claves

| **Nombre** | **Descripción** | **Responsabilidad** |
|:-----------|:----------------|:---------------------|
| Ing. Patrick Jose Cuadros Quiroga | Docente del curso Calidad y Pruebas de Software, EPIS-UPT | Supervisar el desarrollo y evaluar la calidad técnica y documental del sistema |
| Calloticona Chambilla, Marymar D. | Co-desarrolladora — backend, motor de escaneo, DevOps | Diseñar e implementar la API FastAPI, el motor de escaneo, JWT, DeepSeek AI y el despliegue en VPS |
| Ramos Loza, Mariela Estefany | Co-desarrolladora — frontend, QA, reportes | Diseñar e implementar el dashboard Next.js, las pruebas de usuario y la generación de reportes |
| Dirección EPIS — UPT | Entidad académica supervisora | Validar el cumplimiento de estándares académicos de la EPIS |
| Estudiantes EPIS (UPT) | Usuarios finales académicos | Usar la plataforma para auditar sus propios proyectos de desarrollo web |
| PYMES y desarrolladores de Tacna | Beneficiarios externos | Usar la plataforma para diagnosticar la seguridad de sus aplicaciones |

Los roles funcionales dentro del propio sistema son: **Administrador** (control total: usuarios, audit logs, todos los escaneos), **Analista de Seguridad** (escaneos avanzados con IA, configuración de stack, exportación de reportes) y **Usuario Regular** (escaneos simples, visualización de resultados, reportes básicos).

### 12. Papel y responsabilidades del personal

| **Rol** | **Integrante** | **Horas totales** | **Responsabilidades principales** |
|:--------|:----------------|:------------------:|:-----------------------------------|
| Backend Developer / Scrum Master | Calloticona Chambilla, Marymar D. | 80 h | Arquitectura del backend, motor de escaneo (13 módulos), autenticación JWT, integración DeepSeek AI, script de despliegue, configuración del VPS (Nginx, systemd, UFW). |
| Frontend Developer / QA Engineer | Ramos Loza, Mariela Estefany | 80 h | Dashboard SOC, escáner interactivo, panel de administración, pruebas de calidad y usabilidad, generación de reportes PDF/HTML/JSON. |
| **Total** | | **160 h** | |

### 13. Plan de monitoreo y evaluación

El seguimiento del proyecto se realiza mediante indicadores de calidad basados en el modelo ISO/IEC 25010:2011, evaluados durante y después del desarrollo:

| **Característica** | **Métrica** | **Valor objetivo** |
|:--------------------|:------------|:-------------------:|
| Funcionalidad | % de módulos OWASP implementados | 100% (13/13) |
| Funcionalidad | % de vulnerabilidades detectadas en sitio de prueba | ≥ 85% |
| Rendimiento | Tiempo de inicio de escaneo desde el clic | < 2 s |
| Rendimiento | Escaneos simultáneos soportados | ≥ 10 |
| Usabilidad | Tiempo hasta el primer escaneo sin tutorial | < 5 min |
| Usabilidad | Clics necesarios para un escaneo básico | ≤ 3 |
| Confiabilidad | Uptime mensual | ≥ 99.5% |
| Confiabilidad | Recuperación automática tras una caída | < 5 s |
| Confiabilidad | Tasa de falsos positivos por módulo | < 15% |
| Seguridad | Cobertura del audit log sobre acciones relevantes | 100% |
| Mantenibilidad | Líneas de código por módulo de escaneo | < 100 |
| Portabilidad | Pasos de instalación en un VPS limpio | 1 comando |

**Mecanismos de monitoreo continuo una vez desplegado el sistema:** registro de auditoría (AuditLog) de toda acción relevante (login, escaneos, exportaciones, cambios de usuario); reinicio automático del servicio backend mediante `systemd` (`Restart=always`, `RestartSec=5`); panel de administración con estadísticas globales en tiempo real; y revisión periódica del cumplimiento de las métricas anteriores por parte del equipo de desarrollo y el docente supervisor.

### 14. Cronograma del proyecto

| **Fase** | **Duración** | **Actividades Clave** |
|:---------|:------------|:----------------------|
| Fase 1: Arquitectura y Setup | Semana 1 | Definición de arquitectura, configuración VPS (149.34.48.176), MySQL, FastAPI, Next.js, estructura de carpetas y control de versiones. |
| Fase 2: Backend y Motor de Escaneo | Semana 2 | Implementación de los 13 módulos OWASP Top 10: XSS, SQLi, CSRF, SSRF, LFI, Command Injection, Open Redirect, Headers, SSL, Archivos Sensibles, HTTP Methods, Error Disclosure, Crawling. API REST con JWT. |
| Fase 3: Frontend y Dashboard SOC | Semana 3 | Dashboard con gráficos Chart.js, escáner interactivo con polling en tiempo real, panel de administración, autenticación con roles. |
| Fase 4: IA, Reportes y Despliegue | Semana 4 | Integración DeepSeek AI, generación PDF/HTML/JSON, script deploy.sh, Nginx, systemd, PM2, UFW. Pruebas finales. |

### 15. Hitos de entregables

| **Hito** | **Semana** | **Entregable** |
|:---------|:----------:|:----------------|
| H1 — Viabilidad y arquitectura aprobadas | Semana 1 | Informe de Factibilidad (FD01), Documento de Visión (FD02), VPS configurado |
| H2 — Motor de escaneo funcional | Semana 2 | Documento SRS (FD03), API REST con 13 módulos OWASP y autenticación JWT operativos |
| H3 — Interfaz y dashboard operativos | Semana 3 | Documento SAD (FD04), dashboard SOC, escáner interactivo y panel de administración funcionales |
| H4 — Sistema en producción | Semana 4 | Integración DeepSeek AI, reportes PDF/HTML/JSON, despliegue automatizado (`deploy.sh`) en el VPS |
| H5 — Cierre del proyecto | Semana 4 | Informe Final (FD05) y Propuesta del Proyecto (FD06) entregados |

<div style="page-break-after: always;"></div>

---

## II. Presupuesto

### 1. Planteamiento de aplicación del presupuesto

El presupuesto del proyecto se destina a cubrir los costos generales de documentación, los costos operativos durante el mes de desarrollo (energía eléctrica, conectividad a internet y alquiler del VPS de producción) y un margen de imprevistos del 5%. Al tratarse de un stack tecnológico 100% open source, no se incurre en costos de licenciamiento de software. El costo de personal se reporta únicamente como valor referencial, dado que el proyecto es de carácter académico y no representa una erogación monetaria real.

### 2. Presupuesto

| **Categoría** | **Monto Efectivo (S/.)** | **Monto Referencial (S/.)** |
|:--------------|:------------------------:|:---------------------------:|
| Costos Generales (papel, útiles, internet móvil de pruebas) | S/. 45.00 | S/. 45.00 |
| Costos Operativos (energía, internet, VPS — 1 mes) | S/. 96.00 | S/. 96.00 |
| Costos de Software y Licencias | S/. 0.00 | S/. 0.00 |
| Personal (referencial — no erogado, 160 h) | S/. 0.00 | S/. 2,400.00 |
| Imprevistos (5%) | S/. 7.05 | S/. 127.05 |
| **INVERSIÓN TOTAL** | **S/. 148.05** | **S/. 2,668.05** |

### 3. Análisis de Factibilidad

| **Dimensión** | **Resultado** |
|:--------------|:--------------|
| Técnica | 4.83/5 — stack maduro, equipo con conocimiento del dominio, infraestructura ya disponible |
| Económica | Inversión efectiva de S/. 148.05; costo de licenciamiento cero |
| Operativa | Beneficios directos para docente, estudiantes, QA, PYMES y auditores de TI |
| Legal | Cumplimiento de la Ley N° 30096 y la Ley N° 29733 |
| Social | Democratización de la ciberseguridad en la región Tacna |
| Ambiental | Alineación con principios de Green IT (eficiencia computacional, cero residuos físicos) |

El detalle completo del análisis de factibilidad se encuentra en el Informe de Factibilidad (FD01).

### 4. Evaluación Financiera

**Relación Beneficio/Costo (B/C):**

```
B/C = Beneficios Totales Anuales / Inversión Total Efectiva
B/C = S/. 5,206.00 / S/. 148.05
B/C = 35.2
```
> B/C = 35.2 > 1 → **Se acepta el proyecto.** Por cada sol invertido, se generan S/. 35.20 en beneficios.

**Valor Actual Neto (VAN):** considerando vida útil de 3 años, tasa de descuento (COK) de 12% anual y beneficio neto anual de S/. 5,206.00:

```
VAN = -148.05 + (5,206 / 1.12¹) + (5,206 / 1.12²) + (5,206 / 1.12³)
VAN = S/. 12,355.88
```
> VAN = S/. 12,355.88 > 0 → **Se acepta el proyecto.**

**Tasa Interna de Retorno (TIR):** dado el bajo costo de inversión (S/. 148.05) frente a los beneficios anuales de S/. 5,206.00, la TIR supera el **3,400%**, muy superior al COK del 12%.

> TIR >> COK (12%) → **Se acepta el proyecto.** La inversión es altamente rentable.

<div style="page-break-after: always;"></div>

---

## Anexo 01 — Requerimientos del Sistema *VulnScan Pro*

El sistema fue especificado formalmente en el Documento SRS (FD03), que detalla 67 requerimientos funcionales, 30 requerimientos no funcionales y 18 reglas de negocio, agrupados en los siguientes módulos:

| **Módulo** | **Rango de RF** | **Cantidad** |
|:-----------|:----------------|:-------------:|
| Autenticación y Gestión de Usuarios | RF-01 a RF-16 | 16 |
| Motor de Escaneo de Vulnerabilidades | RF-17 a RF-42 | 26 |
| Inteligencia Artificial (DeepSeek AI) | RF-43 a RF-47 | 5 |
| Reportes | RF-48 a RF-52 | 5 |
| Dashboard y Visualización | RF-53 a RF-58 | 6 |
| Administración | RF-59 a RF-63 | 5 |
| Historial de Escaneos | RF-64 a RF-67 | 4 |
| **Total requerimientos funcionales** | | **67** |

Los 30 requerimientos no funcionales se agrupan según los atributos de calidad ISO/IEC 25010: seguridad (RNF-01, 07-09, 13, 15, 17, 20, 26-28, 30), rendimiento (RNF-02-03, 14, 19, 21-22), usabilidad (RNF-04, 16, 23), confiabilidad (RNF-05-06, 12), mantenibilidad (RNF-10, 18, 24-25, 29) y portabilidad (RNF-11).

El sistema contempla además 13 casos de uso completamente especificados (UC-01 a UC-13), cubriendo desde el registro e inicio de sesión hasta la ejecución de los módulos OWASP y la generación de análisis de inteligencia artificial. El detalle completo de cada requerimiento, regla de negocio, caso de uso, diagrama de secuencia y diagrama de clases se encuentra en el Documento SRS (FD03-Requerimientos-Ramos-Calloticona).

---

*Documento elaborado por: Calloticona Chambilla, Marymar D. y Ramos Loza, Mariela Estefany*
*Curso: Calidad y Pruebas de Software — Docente: Ing. Patrick Jose Cuadros Quiroga — UPT — 2026*
