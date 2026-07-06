# Web Vulnerability Scanner para VS Code

Escanea una URL en busca de vulnerabilidades web (XSS, SQLi, CSRF, cabeceras de
seguridad faltantes, open redirect, exposicion de informacion) sin salir de VS Code,
usando el backend de [Web Vulnerability Scanner](https://vulnerabilidad-web.sytes.net).

## Uso (panel lateral, recomendado)

1. En la barra de actividad (el margen vertical izquierdo de VS Code) aparece un
   icono de escudo — **Web Vulnerability Scanner**. Click ahi.
2. Escribe la URL objetivo y dale a **Escanear**.
3. La primera vez te pide correo y contrasena para crear tu cuenta (o iniciar sesion
   si ya la tenias) — se hace una sola vez, sin salir de VS Code.
4. Los resultados aparecen en el mismo panel, con color por severidad: modulo, la
   URL/parametro exacto donde se detecto cada hallazgo, evidencia real (por ejemplo
   el payload reflejado en un XSS) cuando aplica, y la recomendacion.
5. Boton **Exportar ultimo reporte** para guardarlo como Markdown o HTML.
6. Arriba del formulario aparece un mini dashboard: total de escaneos, vulnerabilidades
   por severidad, e historial de tus ultimos 10 escaneos (click en uno para volver a
   ver su reporte).

## Uso (paleta de comandos, alternativa)

1. `Ctrl+Shift+P` → **WVS: Iniciar Escaneo** → introduce la URL objetivo.
2. El resultado se muestra en el panel de salida **"Web Vulnerability Scanner"**
   (`View > Output`).
3. `Ctrl+Shift+P` → **WVS: Exportar ultimo reporte a archivo** para guardarlo.

## Comandos avanzados (opcionales)

No los necesitas para el uso normal — "Iniciar Escaneo" ya configura la cuenta solo:

- **WVS: Configurar mi cuenta**: repetir el registro/login manualmente (por ejemplo
  para cambiar de cuenta).
- **WVS: Usar una credencial existente**: pegar una API key ya generada desde el
  dashboard web o por `POST /api/api-keys`, en vez de crear una cuenta nueva.

## Configuracion

| Setting | Default | Descripcion |
|---|---|---|
| `wvs.apiUrl` | `https://vulnerabilidad-web.sytes.net/backend` | URL base del backend del scanner |

Cambiala en `Settings > Extensions > Web Vulnerability Scanner` si usas tu propia
instancia (por ejemplo un backend local en `http://127.0.0.1:8000`).

## Solo escanea sitios que tengas autorizacion para auditar.
