---
name: vuln-scanner
description: Escanea una URL en busca de vulnerabilidades web (XSS, SQLi, CSRF, cabeceras faltantes, open redirect, exposicion de informacion) usando el backend Web Vulnerability Scanner. Usar cuando el usuario pida escanear, auditar o analizar la seguridad de un sitio/URL.
---

# Vuln Scanner (Custom Agent de GitHub Copilot)

Lanza un escaneo de seguridad contra una URL objetivo usando la API de integraciones del
Web Vulnerability Scanner (`/api/integrations/scans`) y devuelve un reporte legible.

## Requisitos previos

Necesitas una API key propia (no viene incluida en este agente, por seguridad):

- `WVS_API_KEY` (obligatoria): genera una desde el dashboard del scanner en
  `https://vulnerabilidad-web.sytes.net` (seccion API Keys) o con
  `POST /api/api-keys` autenticado con tu usuario.
- `WVS_API_URL` (opcional): por defecto usa el backend de produccion
  `https://vulnerabilidad-web.sytes.net/backend`.

Si `WVS_API_KEY` no esta definida como variable de entorno, pide al usuario que la
configure antes de continuar.

## Uso

Este repositorio ya incluye el script `.claude/skills/vuln-scanner/scripts/scan.py`
(relativo a la raiz del repo). Ejecutalo con el interprete de Python disponible en el
sistema. Prueba primero `python3`; si el comando falla porque no existe (comun en
Windows, donde normalmente solo esta disponible `python`), reintenta con `python`:

```bash
python3 .claude/skills/vuln-scanner/scripts/scan.py <target_url> [--depth N] [--modules m1,m2,...] [--timeout N]
# si falla por no existir python3:
python .claude/skills/vuln-scanner/scripts/scan.py <target_url> [--depth N] [--modules m1,m2,...] [--timeout N]
```

- `target_url` (obligatorio): URL completa a escanear, ej. `https://ejemplo.com`.
- `--depth`: profundidad de rastreo, 0-3 (default 1).
- `--modules`: lista separada por comas de modulos a ejecutar. Por defecto:
  `xss,sqli,headers,csrf,open_redirect,info_disclosure`.
- `--timeout`: timeout por request del scanner en segundos, 3-30 (default 10).

El script crea el escaneo, hace polling hasta que termina (`completed` o `failed`) y
finalmente imprime en stdout un reporte en Markdown con severidad, ubicacion, evidencia
(cuando aplica) y recomendacion de cada vulnerabilidad encontrada. Muestra ese reporte
al usuario.

## Notas

- Un escaneo puede tardar desde varios segundos hasta un par de minutos; informa al
  usuario que puede tomar un momento.
- Si el backend responde 401/403, la API key es invalida o fue revocada.
- Solo se debe escanear URLs que el usuario tenga autorizacion para auditar.
