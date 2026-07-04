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

Informe de Factibilidad

Versión 1.0

| CONTROL DE VERSIONES |                  |                |              |            |                  |
|:--------------------:|:-----------------|:---------------|:-------------|:-----------|:-----------------|
| Versión              | Hecha por        | Revisada por   | Aprobada por | Fecha      | Motivo           |
| 1.0                  | M. Calloticona   | M. Ramos       |              | 28/03/2026 | Versión Original |
| 1.1                  | M. Ramos         | M. Calloticona |              | 04/04/2026 | Actualización stack tecnológico |

<div style="page-break-after: always;"></div>

---

## ÍNDICE GENERAL

1. [Descripción del Proyecto](#1-descripción-del-proyecto)  
   1.1. Nombre del Proyecto  
   1.2. Duración del Proyecto  
   1.3. Descripción  
   1.4. Objetivos  

2. [Riesgos](#2-riesgos)  

3. [Análisis de la Situación Actual](#3-análisis-de-la-situación-actual)  
   3.1. Planteamiento del Problema  
   3.2. Consideraciones de Hardware y Software  

4. [Estudio de Factibilidad](#4-estudio-de-factibilidad)  
   4.1. Factibilidad Técnica  
   4.2. Factibilidad Económica  
   4.3. Factibilidad Operativa  
   4.4. Factibilidad Legal  
   4.5. Factibilidad Social  
   4.6. Factibilidad Ambiental  

5. [Análisis Financiero](#5-análisis-financiero)  
   5.1. Justificación de la Inversión  

6. [Conclusiones](#6-conclusiones)  

<div style="page-break-after: always;"></div>

---

## Informe de Factibilidad

---

## 1. Descripción del Proyecto

### 1.1. Nombre del Proyecto

**Analizador de Vulnerabilidades Web — VulnScan Pro**

Sistema de auditoría de seguridad web con inteligencia artificial, orientado a la detección automática de vulnerabilidades según el estándar OWASP Top 10.

### 1.2. Duración del Proyecto

- **Tiempo total de desarrollo:** 4 semanas (1 mes)

| **Fase**                        | **Duración** | **Actividades Clave**                                                                                          |
|:--------------------------------|:-------------|:---------------------------------------------------------------------------------------------------------------|
| **Fase 1: Arquitectura y Setup** | Semana 1     | Definición de arquitectura, configuración del VPS (149.34.48.176), base de datos MySQL, estructura FastAPI y Next.js. |
| **Fase 2: Backend y Scanner**   | Semana 2     | Implementación del motor de escaneo: XSS, SQLi, CSRF, SSRF, LFI, Headers, SSL. API REST con autenticación JWT.  |
| **Fase 3: Frontend y Dashboard**| Semana 3     | Dashboard SOC en Next.js, escáner interactivo, panel de administración, visualización de resultados con gráficos. |
| **Fase 4: IA e Integración**    | Semana 4     | Integración DeepSeek AI para análisis automático, generación de reportes PDF/HTML/JSON, pruebas finales y despliegue. |

### 1.3. Descripción

**VulnScan Pro** es una plataforma web profesional de análisis dinámico de seguridad (DAST) desarrollada en el marco del curso *Calidad y Pruebas de Software* de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna. El sistema permite a ingenieros de QA, desarrolladores y auditores de seguridad identificar vulnerabilidades web de forma automatizada antes del despliegue a producción.

La plataforma integra inteligencia artificial (DeepSeek AI) para analizar cada vulnerabilidad detectada, generar escenarios de ataque realistas, proporcionar código de remediación específico para el stack tecnológico objetivo y producir reportes ejecutivos con puntuación de riesgo. La arquitectura está compuesta por un backend en Python con FastAPI, una base de datos MySQL nativa, y un frontend en Next.js 16 con TypeScript y TailwindCSS, desplegados en un servidor VPS Linux mediante Nginx, systemd y PM2.

El contexto de aplicación abarca tanto el ámbito académico universitario como el entorno real de PYMES y desarrolladores independientes de la región Tacna, que actualmente no tienen acceso a herramientas de auditoría de seguridad profesionales por su elevado costo.

### 1.4. Objetivos

#### 1.4.1. Objetivo General

Desarrollar una plataforma web integral de análisis de vulnerabilidades de seguridad que permita a equipos de desarrollo e ingeniería de calidad identificar, priorizar y remediar brechas de seguridad en aplicaciones web, mediante un motor de escaneo OWASP Top 10 potenciado por inteligencia artificial, con despliegue nativo en infraestructura VPS Linux.

#### 1.4.2. Objetivos Específicos

1. **Implementar un motor de escaneo multimódulo** capaz de detectar las vulnerabilidades más críticas del OWASP Top 10: SQL Injection, Cross-Site Scripting (XSS), CSRF, SSRF, LFI, Command Injection, Open Redirect, cabeceras HTTP inseguras, configuración SSL/TLS deficiente, archivos sensibles expuestos y métodos HTTP peligrosos.

2. **Desarrollar un sistema de autenticación robusto** con roles diferenciados (Administrador, Analista, Usuario), protección anti-fuerza bruta, sesiones con JWT, registro de auditoría y gestión de usuarios desde un panel administrativo.

3. **Integrar DeepSeek AI** para análisis automático por vulnerabilidad: puntuación CVSS, identificador CWE, escenario de ataque, código de remediación adaptado al stack tecnológico objetivo y reporte ejecutivo de riesgo.

4. **Construir un frontend SOC** (Security Operations Center) en Next.js 16 con dashboard de estadísticas en tiempo real, gráficos interactivos, escáner con configuración avanzada y panel de administración de usuarios.

5. **Desplegar el sistema en producción** sobre un VPS Linux (IP: 149.34.48.176) con Nginx como proxy inverso, systemd para el backend, PM2 para el frontend, UFW para el firewall y MySQL nativo como base de datos.

<div style="page-break-after: always;"></div>

---

## 2. Riesgos

| **#** | **Riesgo** | **Probabilidad** | **Impacto** | **Mitigación** |
|:------|:-----------|:----------------|:------------|:---------------|
| R-01 | Bloqueo de IPs por servidores objetivo durante el escaneo | Media | Alto | Implementar timeouts configurables, límite de peticiones y User-Agent rotatorio. |
| R-02 | Falsos positivos que generen resultados incorrectos | Alta | Medio | Validación cruzada con múltiples payloads y análisis de confianza por IA. |
| R-03 | Uso indebido de la herramienta sin autorización del objetivo | Baja | Crítico | Aviso legal obligatorio en la interfaz; documentación ética en el repositorio. |
| R-04 | Fallo en la integración con la API de DeepSeek (rate limit, timeout) | Media | Medio | Implementación de análisis local de fallback para las vulnerabilidades más comunes. |
| R-05 | Indisponibilidad del VPS durante escaneos activos | Baja | Alto | Configuración de reinicio automático con systemd (Restart=always) y monitoreo de health check. |
| R-06 | Consumo excesivo de recursos del servidor durante escaneos paralelos | Media | Medio | Límite de escaneos concurrentes y workers controlados con Gunicorn (4 workers). |
| R-07 | Vulnerabilidades en el propio sistema (credenciales expuestas, SQLi en la plataforma) | Baja | Crítico | Revisión de seguridad interna, variables de entorno en `.env`, prepared statements en SQLAlchemy. |

<div style="page-break-after: always;"></div>

---

## 3. Análisis de la Situación Actual

### 3.1. Planteamiento del Problema

La seguridad de las aplicaciones web en entornos académicos y de pequeñas empresas en la región Tacna presenta deficiencias estructurales derivadas de la falta de herramientas de auditoría accesibles. Las soluciones profesionales existentes (Burp Suite Professional: USD 449/año, Nessus: USD 3,590/año, Acunetix: USD 4,500/año) tienen costos de licenciamiento que las hacen inaccesibles para estudiantes, desarrolladores independientes y PYMES.

Como consecuencia, las aplicaciones web locales frecuentemente se despliegan con configuraciones de seguridad deficientes: cabeceras HTTP ausentes, certificados SSL vencidos, formularios vulnerables a inyección SQL, cookies sin flags de protección, y endpoints sensibles expuestos. Esta situación expone datos de ciudadanos, estudiantes y organizaciones a ataques automatizados crecientes.

El problema central es la ausencia de una capa de verificación de seguridad entre el desarrollo y el despliegue productivo. **VulnScan Pro** actúa como esa capa, automatizando las pruebas de seguridad más críticas del ciclo de vida de desarrollo seguro (S-SDLC) de manera gratuita y con resultados comprensibles incluso para equipos sin experiencia avanzada en ciberseguridad.

### 3.2. Consideraciones de Hardware y Software

#### Hardware disponible

| **Componente** | **Especificación** | **Estado** |
|:---------------|:-------------------|:-----------|
| Laptop de desarrollo | CPU Intel i5/i7 11ª gen, 16 GB RAM, SSD 512 GB | Disponible |
| VPS de producción | IP: 149.34.48.176, 2 vCPU, 4 GB RAM, 50 GB SSD, Ubuntu 22.04 | Activo |
| Monitor externo | 24" Full HD | Disponible |

#### Stack tecnológico completo

| **Tecnología** | **Versión** | **Propósito** | **Costo** |
|:---------------|:------------|:--------------|:----------|
| Python | 3.11+ | Lenguaje principal del backend | S/. 0.00 (Open Source) |
| FastAPI | 0.110+ | Framework API REST asíncrono | S/. 0.00 (MIT) |
| SQLAlchemy | 2.0 | ORM para base de datos MySQL | S/. 0.00 (MIT) |
| MySQL | 8.0 | Base de datos relacional nativa | S/. 0.00 (GPL) |
| Gunicorn + Uvicorn | Latest | Servidor WSGI/ASGI para producción | S/. 0.00 (MIT) |
| Next.js | 16 (App Router) | Framework frontend React | S/. 0.00 (MIT) |
| TypeScript | 5.x | Tipado estático para JavaScript | S/. 0.00 (Apache 2.0) |
| TailwindCSS | 3.x | Framework CSS utilitario | S/. 0.00 (MIT) |
| Chart.js | 4.x | Gráficos interactivos | S/. 0.00 (MIT) |
| DeepSeek AI API | deepseek-chat | Análisis IA de vulnerabilidades | S/. 0.00* (plan gratuito) |
| Nginx | 1.24 | Proxy inverso y servidor web | S/. 0.00 (BSD) |
| PM2 | Latest | Process manager Node.js | S/. 0.00 (AGPL) |
| UFW | Latest | Firewall Linux | S/. 0.00 (GPL) |
| BeautifulSoup4 | 4.12 | Web crawling y parsing HTML | S/. 0.00 (MIT) |
| python-jose | 3.x | Generación y validación JWT | S/. 0.00 (MIT) |
| WeasyPrint | Latest | Generación de reportes PDF | S/. 0.00 (BSD) |
| VS Code | Latest | IDE de desarrollo | S/. 0.00 (Gratuito) |
| Git / GitHub | 2.x | Control de versiones | S/. 0.00 (Plan Free) |

*DeepSeek AI ofrece créditos iniciales gratuitos para uso académico.

<div style="page-break-after: always;"></div>

---

## 4. Estudio de Factibilidad

Los resultados del estudio de factibilidad indican que el proyecto **VulnScan Pro** es viable desde las dimensiones técnica, económica, operativa, legal, social y ambiental. La evaluación fue realizada por el equipo de desarrollo y revisada por la docente supervisora del curso.

### 4.1. Factibilidad Técnica

El proyecto es **técnicamente factible**. El equipo cuenta con los conocimientos necesarios en desarrollo web fullstack (Python, JavaScript/TypeScript, bases de datos relacionales) y el stack elegido está completamente basado en tecnologías de código abierto maduras y ampliamente documentadas.

| **Criterio** | **Puntuación (1-5)** | **Justificación** |
|:-------------|:--------------------:|:------------------|
| Disponibilidad de tecnología | 5 | Python, FastAPI, Next.js y MySQL son frameworks estables con amplia comunidad. |
| Conocimiento del equipo | 4 | Dominio intermedio-avanzado en Python, JS/TS y bases de datos. |
| Escalabilidad de la arquitectura | 5 | Arquitectura desacoplada cliente-servidor permite añadir módulos de escaneo sin refactorizar el core. |
| Disponibilidad de infraestructura | 5 | VPS Linux contratado (149.34.48.176) con acceso root y conectividad permanente. |
| Compatibilidad tecnológica | 5 | Todo el stack es compatible entre sí y con el sistema operativo Ubuntu 22.04 del VPS. |

**Medidas de seguridad técnica implementadas:**
- Sanitización de entradas con Pydantic (FastAPI) y tipado estricto TypeScript.
- Timeouts configurables por módulo (5, 10, 30, 60 segundos) para evitar DoS accidental.
- Rate limiting en la API (slowapi) y en Nginx (3 zonas: API general, login, escaneos).
- Autenticación JWT con expiración, JTI único por sesión y tabla de sesiones activas.
- Variables de entorno en `.env` con `python-dotenv`; no hay credenciales en código fuente.
- Headers de seguridad HTTP aplicados por middleware: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`.

### 4.2. Factibilidad Económica

El proyecto es **económicamente factible** bajo un modelo de desarrollo académico de bajo costo. Todo el stack tecnológico es de código abierto y no requiere pago de licencias. Los únicos costos reales son los operativos del equipo de desarrollo durante las 4 semanas de ejecución.

#### 4.2.1. Costos Generales

| **Ítem** | **Cantidad** | **Costo Unitario (S/.)** | **Costo Total (S/.)** |
|:---------|:------------:|:------------------------:|:---------------------:|
| Papel e impresión de documentación | 1 resma | S/. 15.00 | S/. 15.00 |
| Útiles de escritorio | Global | S/. 10.00 | S/. 10.00 |
| **Total Costos Generales** | | | **S/. 25.00** |

#### 4.2.2. Costos Operativos durante el Desarrollo

| **Ítem** | **Cantidad (mes)** | **Costo Unitario (S/.)** | **Costo Total (S/.)** |
|:---------|:------------------:|:------------------------:|:---------------------:|
| Energía eléctrica (consumo PC + monitor) | 1 | S/. 35.00 | S/. 35.00 |
| Servicio de internet (fibra óptica) | 1 | S/. 40.00 | S/. 40.00 |
| **Total Costos Operativos** | | | **S/. 75.00** |

#### 4.2.3. Costos del Ambiente (Software y Licencias)

| **Recurso / Software** | **Proveedor** | **Tipo de Licencia** | **Costo (S/.)** |
|:----------------------|:--------------|:---------------------|:---------------:|
| Python 3.11 + FastAPI | PSF / Sebastián Ramírez | Open Source (MIT) | S/. 0.00 |
| Next.js 16 + TypeScript | Vercel / Microsoft | Open Source (MIT) | S/. 0.00 |
| MySQL 8.0 | Oracle | GPL v2 | S/. 0.00 |
| TailwindCSS 3.x | Tailwind Labs | MIT | S/. 0.00 |
| DeepSeek AI API | DeepSeek | Free tier académico | S/. 0.00 |
| VS Code + extensiones | Microsoft | Gratuita | S/. 0.00 |
| Repositorio GitHub | GitHub | Plan Free | S/. 0.00 |
| Nginx + PM2 | Open Source | BSD / AGPL | S/. 0.00 |
| **Total Costos de Ambiente** | | | **S/. 0.00** |

#### 4.2.4. Costos de Personal

El equipo de desarrollo está conformado por 2 estudiantes con dedicación parcial (20 horas/semana cada una durante 4 semanas). Como proyecto académico, el costo de personal no representa una erogación monetaria real, pero se valora a título informativo:

| **Rol** | **Persona** | **Horas totales** | **Valor hora (S/.)** | **Costo referencial (S/.)** |
|:--------|:------------|:-----------------:|:--------------------:|:---------------------------:|
| Backend Developer / Scrum Master | Calloticona Chambilla, Marymar D. | 80 horas | S/. 15.00 | S/. 1,200.00 |
| Frontend Developer / QA Engineer | Ramos Loza, Mariela Estefany | 80 horas | S/. 15.00 | S/. 1,200.00 |
| **Total Personal (referencial)** | | **160 horas** | | **S/. 2,400.00** |

#### 4.2.5. Costos Totales del Desarrollo

| **Categoría** | **Monto (S/.)** |
|:--------------|:---------------:|
| Costos Generales | S/. 25.00 |
| Costos Operativos (1 mes) | S/. 75.00 |
| Costos de Software y Licencias | S/. 0.00 |
| Personal (referencial, no erogado) | S/. 2,400.00 |
| Imprevistos (5%) | S/. 5.00 |
| **INVERSIÓN TOTAL EFECTIVA** | **S/. 105.00** |
| **INVERSIÓN TOTAL REFERENCIAL** | **S/. 2,505.00** |

### 4.3. Factibilidad Operativa

El sistema es **operativamente factible**. Los beneficios directos incluyen:

- **Para el equipo docente:** Herramienta de evaluación práctica para que los estudiantes demuestren comprensión de seguridad web en el marco del curso Calidad y Pruebas de Software.
- **Para los estudiantes EPIS:** Herramienta gratuita para auditar sus propios proyectos antes de presentarlos.
- **Para PYMES de Tacna:** Acceso a diagnósticos de seguridad sin costo de licenciamiento.
- **Mantenibilidad:** La arquitectura modular del scanner permite que nuevos módulos de seguridad sean añadidos sin modificar el core del sistema.

**Lista de interesados:**

| **Interesado** | **Rol** | **Nivel de involucramiento** |
|:---------------|:--------|:-----------------------------|
| Ing. Patrick Jose Cuadros Quiroga | Docente / supervisor | Alto |
| Calloticona Chambilla, Marymar D. | Desarrolladora backend | Alto |
| Ramos Loza, Mariela Estefany | Desarrolladora frontend / QA | Alto |
| Estudiantes EPIS (UPT) | Usuarios finales | Medio |
| PYMES y desarrolladores de Tacna | Beneficiarios externos | Bajo |

### 4.4. Factibilidad Legal

El desarrollo y distribución de **VulnScan Pro** se rige bajo un estricto marco de legalidad:

- **Ley N° 30096 — Ley de Delitos Informáticos (Perú):** La plataforma incluye un aviso legal obligatorio que el usuario debe aceptar antes de iniciar cualquier escaneo, declarando poseer autorización explícita sobre la aplicación objetivo. El sistema no ejecuta ningún ataque destructivo ni afecta la disponibilidad del servicio auditado.

- **Ley N° 29733 — Protección de Datos Personales (Perú):** El sistema no recolecta ni almacena datos personales de terceros. Los resultados de los escaneos residen en la base de datos del sistema y solo son accesibles para el usuario autenticado que realizó el escaneo.

- **Licenciamiento:** El código fuente se distribuye bajo **Licencia MIT**, garantizando transparencia total y ausencia de funciones ocultas.

- **Disclaimer:** La plataforma incluye términos de uso que especifican que los autores no se responsabilizan por el uso indebido del software sobre sistemas sin autorización expresa.

### 4.5. Factibilidad Social

**VulnScan Pro** genera impacto social positivo en múltiples dimensiones:

- **Democratización de la ciberseguridad:** Permite que estudiantes y PYMES de Tacna accedan a diagnósticos de seguridad equivalentes a herramientas comerciales de costo elevado.
- **Formación en hacking ético:** Promueve el uso responsable y ético de herramientas de seguridad dentro del ecosistema académico de la UPT.
- **Protección del ciudadano:** Al elevar la seguridad de aplicaciones locales, se protege indirectamente la información personal de los ciudadanos que utilizan servicios digitales de pequeñas empresas de la región.
- **Cultura de desarrollo seguro (DevSecOps):** Introduce la práctica de pruebas de seguridad como parte integral del proceso de desarrollo de software, educando a la próxima generación de ingenieros en la región.

### 4.6. Factibilidad Ambiental

El proyecto se alinea con los principios de **Green IT**:

- **Eficiencia computacional:** FastAPI es uno de los frameworks Python más eficientes en términos de consumo de CPU y memoria por petición, reduciendo el impacto energético en el servidor.
- **Cero residuos físicos:** Distribución 100% digital mediante GitHub. No se requiere impresión ni medios físicos.
- **Infraestructura compartida:** El VPS aloja múltiples proyectos, optimizando el uso de recursos físicos de hardware.
- **Lazy loading y optimización frontend:** Next.js aplica code splitting y optimización automática de recursos, reduciendo el consumo de ancho de banda y la carga en el dispositivo del usuario final.

<div style="page-break-after: always;"></div>

---

## 5. Análisis Financiero

### 5.1. Justificación de la Inversión

La inversión de S/. 105.00 efectivos se justifica ampliamente por los beneficios tanto tangibles como intangibles que genera el sistema.

#### 5.1.1. Beneficios del Proyecto

**Beneficios tangibles:**
- Reducción del tiempo de detección de vulnerabilidades: de días (auditoría manual) a minutos (escaneo automatizado).
- Eliminación del costo de licencias de herramientas de seguridad equivalentes (USD 449–4,500/año).
- Generación automática de reportes técnicos listos para auditoría, reduciendo horas de trabajo de redacción manual.
- Reducción del riesgo económico asociado a brechas de seguridad (costo promedio de una brecha de datos en PYME: USD 25,000–50,000).

**Beneficios intangibles:**
- Elevación del estándar de calidad de software en el entorno académico de la UPT.
- Construcción de competencias prácticas en ciberseguridad para el equipo de desarrollo.
- Reputación como equipo de desarrollo con buenas prácticas de seguridad.
- Contribución a la cultura de seguridad digital en la región Tacna.

#### 5.1.2. Criterios de Inversión

**5.1.2.1. Relación Beneficio/Costo (B/C)**

| **Concepto** | **Valor (S/.)** |
|:-------------|:---------------:|
| Costo total efectivo del proyecto | S/. 105.00 |
| Beneficio anual estimado (ahorro en licencias + reducción de riesgo) | S/. 12,000.00 |
| **B/C = 12,000 / 105 = 114.3** | **B/C > 1 → Se acepta el proyecto** |

**5.1.2.2. Valor Actual Neto (VAN)**

Con una vida útil estimada del software de 3 años, una tasa de descuento del 12% anual y beneficios anuales conservadores de S/. 2,000.00:

- VAN = -105 + (2,000/1.12) + (2,000/1.12²) + (2,000/1.12³)
- VAN = -105 + 1,786 + 1,594 + 1,424 = **S/. 4,699 → VAN > 0, se acepta el proyecto**

**5.1.2.3. Tasa Interna de Retorno (TIR)**

Dado el bajo costo del proyecto y los beneficios proyectados, la TIR estimada supera el **150%**, muy por encima del costo de oportunidad de capital (COK = 12%). **El proyecto se acepta.**

<div style="page-break-after: always;"></div>

---

## 6. Conclusiones

1. El proyecto **VulnScan Pro — Analizador de Vulnerabilidades Web** es **altamente factible** desde todas las dimensiones analizadas: técnica, económica, operativa, legal, social y ambiental.

2. El stack tecnológico seleccionado (FastAPI + MySQL + Next.js + DeepSeek AI) garantiza un sistema moderno, escalable, seguro y de costo cero en licenciamiento, maximizando el valor del proyecto con una inversión efectiva mínima.

3. La integración de inteligencia artificial (DeepSeek AI) diferencia al sistema de herramientas académicas convencionales, ofreciendo análisis contextualizado por vulnerabilidad con código de remediación específico, lo que incrementa significativamente la utilidad práctica del sistema.

4. El proyecto cumple con el marco legal peruano (Ley N° 30096 y Ley N° 29733) y adopta un enfoque ético de hacking defensivo, con mecanismos de control que previenen el uso indebido de la plataforma.

5. Los indicadores financieros (B/C = 114.3, VAN positivo, TIR > 150%) confirman la viabilidad y conveniencia de desarrollar e implementar el sistema.

---

*Documento elaborado por el equipo de desarrollo — Curso Calidad y Pruebas de Software — UPT — 2026*
