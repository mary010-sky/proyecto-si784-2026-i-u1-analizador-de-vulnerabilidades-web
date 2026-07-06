# Changelog

## 0.0.5

- Mini dashboard en el panel lateral: totales de escaneos/vulnerabilidades, desglose
  por severidad, e historial de los ultimos 10 escaneos. Click en un escaneo anterior
  para volver a ver su reporte completo sin re-escanear.

## 0.0.4

- Icono propio en la barra de actividad de VS Code con un panel lateral: escanea y ve
  resultados con colores por severidad sin usar la paleta de comandos.
- Nuevo comando/boton **Exportar reporte** (Markdown o HTML) para guardar el resultado
  como archivo, util para adjuntarlo como evidencia.

## 0.0.3

- `WVS: Iniciar Escaneo` ya no requiere configurar nada antes: si es la primera vez,
  pide correo/contrasena y arma la cuenta sola, sin exponer el concepto de "API key".
- Reporte mucho mas detallado: ahora muestra el modulo, la URL/parametro exacto donde
  se encontro cada hallazgo, y la evidencia real (payload reflejado en XSS, patron de
  error en SQLi) cuando el backend la reporta. Ordenado por severidad.

## 0.0.2

- Nuevo comando `WVS: Registrarse y Configurar`: crea la cuenta (o inicia sesion si ya
  existe) y genera + guarda la API key automaticamente, sin salir de VS Code.

## 0.0.1

- Comandos `WVS: Configurar API Key` y `WVS: Iniciar Escaneo`.
- Reporte completo (severidad, descripcion, recomendacion) en panel de salida.
- Backend de produccion por defecto (`https://vulnerabilidad-web.sytes.net/backend`).
