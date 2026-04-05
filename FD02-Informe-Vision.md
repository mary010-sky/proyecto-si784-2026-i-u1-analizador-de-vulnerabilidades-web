<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

# UNIVERSIDAD PRIVADA DE TACNA

## FACULTAD DE INGENIERÍA

### Escuela Profesional de Ingeniería de Sistemas

**Curso:** Calidad y Pruebas de Software  
**Proyecto:** Analizador de Vulnerabilidades Web (ScanGuard UPT)  
**Docente:** Ing. Patrick Jose Cuadros Quiroga

**Integrantes:**

* Ramos Loza, Mariela Estefany (2023077478)
* Calloticona Chambilla, Marymar D. (2023076791)

**Tacna – Perú**  
**2026**

---

<div style="page-break-after: always;"></div>

## CONTROL DE VERSIONES

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1.0 | **M. Calloticona** | **M. Ramos** | | 28/03/2026 | Versión Original |
| 1.1 | **M. Calloticona** | **M. Ramos** | | 04/04/2026 | Extensión de métricas ISO 25010 e Introducción detallada |

---

<div style="page-break-after: always;"></div>

## **INDICE GENERAL**

1. [**Introducción**](#1-introducción)  
   1.1 Propósito  
   1.2 Alcance  
   1.3 Definiciones, Siglas y Abreviaturas  
   1.4 Referencias  
   1.5 Visión General  
2. [**Posicionamiento**](#2-posicionamiento)  
   2.1 Oportunidad de negocio  
   2.2 Definición del problema  
3. [**Descripción de los interesados y usuarios**](#3-descripción-de-los-interesados-y-usuarios)  
   3.1 Resumen de los interesados  
   3.2 Resumen de los usuarios  
   3.3 Entorno de usuario  
   3.4 Perfiles de los interesados  
   3.5 Perfiles de los Usuarios  
   3.6 Necesidades de los interesados y usuarios  
4. [**Vista General del Producto**](#4-vista-general-del-producto)  
   4.1 Perspectiva del producto  
   4.2 Resumen de capacidades  
   4.3 Suposiciones y dependencias  
   4.4 Costos y precios  
   4.5 Licenciamiento e instalación  
5. [**Características del producto**](#5-características-del-producto)  
6. [**Restricciones**](#6-restricciones)  
7. [**Rangos de calidad**](#7-rangos-de-calidad)  
8. [**Precedencia y Prioridad**](#8-precedencia-y-prioridad)  
9. [**Otros requerimientos del producto**](#9-otros-requerimientos-del-producto)  
10. [**Conclusiones**](#conclusiones)  
11. [**Recomendaciones**](#recomendaciones)  
12. [**Bibliografía**](#bibliografía)

---

<div style="page-break-after: always;"></div>

## **1. Introducción**

**1.1 Propósito**  
El presente Documento de Visión tiene como objetivo fundamental definir las directrices estratégicas, técnicas y operativas para el desarrollo del proyecto **"ScanGuard UPT: Analizador de Vulnerabilidades Web"**. Este documento busca alinear los esfuerzos del equipo de desarrollo con las expectativas académicas del curso de **Calidad y Pruebas de Software**, estableciendo un marco de referencia que garantice que el producto final cumpla con estándares rigurosos de seguridad, fiabilidad y eficiencia.

**1.2 Alcance**  
El proyecto comprende el diseño y desarrollo de una plataforma de pruebas de seguridad dinámica (DAST). El sistema interactuará con aplicaciones web externas para identificar fallos de configuración y vulnerabilidades lógicas sin necesidad de acceder al código fuente, utilizando un motor desarrollado en $.NET\ 8$ y una interfaz reactiva en $Angular$.

**1.3 Definiciones, Siglas y Abreviaturas**  
* **OWASP:** *Open Web Application Security Project*.  
* **DAST:** *Dynamic Application Security Testing*.  
* **XSS:** *Cross-Site Scripting*.  
* **SQLi:** *SQL Injection*.  

**1.4 Referencias**  
* ISO/IEC 25010: Modelo de calidad del software.  
* Ley N° 30096: Ley de Delitos Informáticos del Perú.  
* Documentación oficial de Angular 18 y .NET 8.

**1.5 Visión General**  
El sistema se posiciona como una herramienta de auditoría de "Caja Negra" orientada a mejorar el aseguramiento de la calidad (QA) mediante la automatización de escaneos preventivos.

---

## **2. Posicionamiento**

**2.1 Oportunidad de negocio**  
Dada la creciente digitalización en la región de Tacna, las PYMES enfrentan riesgos críticos de ciberseguridad. ScanGuard UPT ofrece una alternativa de bajo costo y alta eficiencia para diagnosticar vulnerabilidades antes de ataques reales.

**2.2 Definición del problema**  
| **Componente** | **Descripción** |
| :--- | :--- |
| **Problema** | Carencia de auditorías de seguridad accesibles. |
| **Afectados** | Desarrolladores, empresas locales y usuarios finales. |
| **Impacto** | Exposición de datos personales y pérdida de reputación institucional. |
| **Solución** | Automatización de pruebas dinámicas de seguridad web. |

---

## **3. Descripción de los interesados y usuarios**

**3.1 Resumen de los interesados**  
Incluye al docente del curso, la Escuela Profesional de Ingeniería de Sistemas y el equipo de desarrollo (Marymar y Mariela).

**3.2 Resumen de los usuarios**  
Principalmente ingenieros de QA, auditores de seguridad junior y desarrolladores backend.

**3.3 Entorno de usuario**  
Plataforma basada en web, compatible con navegadores modernos (Chrome, Firefox, Edge), optimizada para su uso en estaciones de trabajo de desarrollo.

**3.4 Perfiles de los interesados**  
Usuarios con perfil técnico que buscan métricas de seguridad claras para la toma de decisiones en el despliegue de software.

**3.5 Perfiles de los Usuarios**  
Profesionales de TI interesados en integrar la seguridad como un atributo de calidad desde las fases tempranas del desarrollo.

**3.6 Necesidades de los interesados y usuarios**  
Identificación de riesgos en tiempo real, reportes interpretables y recomendaciones de mitigación.

---

## **4. Vista General del Producto**

**4.1 Perspectiva del producto**  
Es una herramienta autónoma que actúa como intermediaria entre el analista y la aplicación objetivo, enviando peticiones HTTP controladas.

**4.2 Resumen de capacidades**  
Detección de vulnerabilidades SSL, análisis de cabeceras de seguridad y escaneo de parámetros críticos.

**4.3 Suposiciones y dependencias**  
Se asume que el servidor objetivo permite el tráfico automatizado y que el usuario posee los permisos legales para auditar la URL.

**4.4 Costos y precios**  
Al ser un proyecto académico de la UPT, el costo de adquisición es cero, basándose en tecnologías de código abierto.

**4.5 Licenciamiento e instalación**  
Se distribuirá bajo licencia MIT. No requiere instalación compleja al ser una solución web (SaaS).

---

## **5. Características del producto**  
* Rastreo inteligente de enlaces (Spidering).  
* Identificación de cabeceras HTTP inseguras.  
* Validación de certificados SSL/TLS.  
* Categorización de riesgos mediante colores (Semaforización).

---

## **6. Restricciones**  
* No se realizarán ataques intrusivos de Denegación de Servicio (DoS).  
* El sistema está limitado a aplicaciones que operen bajo el protocolo HTTP/HTTPS.

---

## **7. Rangos de calidad**  
Cumplimiento estricto de la **ISO/IEC 25010** en las subcaracterísticas de **Confidencialidad**, **Integridad** y **Responsabilidad**. El tiempo de respuesta de escaneo no deberá exceder los 120 segundos para sitios estándar.

---

## **8. Precedencia y Prioridad**  
1. **Prioridad Alta:** Escaneo de vulnerabilidades críticas (SQLi, XSS).  
2. **Prioridad Media:** Generación de reportes PDF/Web.  
3. **Prioridad Baja:** Historial de escaneos anteriores.

---

## **9. Otros requerimientos del producto**  
* **Estándares legales:** Alineación con la Ley de Protección de Datos Personales.  
* **Seguridad:** Los resultados de las auditorías deben ser volátiles o estar protegidos por cifrado.

---

## **CONCLUSIONES**  
El desarrollo de ScanGuard UPT demuestra que la seguridad es un pilar fundamental de la calidad del software. Mediante el uso de tecnologías modernas como $.NET\ 8$ y $Angular$, se ha logrado una herramienta que democratiza el acceso a la ciberseguridad en la región de Tacna, permitiendo reducir los riesgos de explotación en plataformas locales.

---

## **RECOMENDACIONES**  
Se sugiere la actualización constante de la base de datos de firmas de ataque y la integración del motor de escaneo en procesos de integración continua (CI/CD) para una auditoría constante durante el desarrollo.

---

## **BIBLIOGRAFÍA**  
1. ISO/IEC 25010:2011 - Systems and software Quality Requirements.  
2. OWASP Top 10 Reference Guide (2025).  
3. Microsoft Documentation: Security best practices for ASP.NET Core 8.0.
