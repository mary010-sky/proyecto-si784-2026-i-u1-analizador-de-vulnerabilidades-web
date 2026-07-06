# Guía: Agente Personalizado de GitHub Copilot

**Actualización importante:** GitHub cambió por completo cómo se crean agentes
personalizados de Copilot. El modelo anterior (una GitHub App con tipo "Agent" +
un servidor HTTP propio) quedó obsoleto. El modelo actual (2026) es mucho más simple:
**un solo archivo Markdown dentro del repositorio**, sin servidor, sin GitHub App,
sin nada que desplegar.

## Dónde vive el agente

```
.github/agents/vuln-scanner.agent.md
```

Ya está creado en este repo. Contiene:
- Frontmatter YAML con `name` y `description` (esto es lo que usa Copilot para saber
  cuándo ofrecer el agente).
- Instrucciones en Markdown debajo, que le dicen a Copilot que ejecute
  `.claude/skills/vuln-scanner/scripts/scan.py` (el mismo script que ya usa la Skill
  de Claude Code — no se duplicó nada).

## Requisitos

- El archivo debe estar comiteado en la rama por defecto (`main`) del repo para que
  Copilot lo detecte.
- Cada usuario necesita su propia `WVS_API_KEY` como variable de entorno (no viene
  incluida en el agente).

## Cómo se usa

Una vez que el archivo está en `main`:

- **github.com**: en el panel/pestaña de agentes de Copilot, hay un selector para
  elegir este agente personalizado en vez del agente por defecto.
- **VS Code / JetBrains / Eclipse / Xcode**: aparece como opción dentro de Copilot
  Chat (función en preview publica).
- **GitHub Copilot CLI**: con el comando `/agent`.
- **Asignar a un issue**: al asignarle Copilot a un issue, se puede elegir este agente
  en el desplegable.

No hace falta instalar nada ni crear ninguna GitHub App — Copilot lo detecta solo por
estar en `.github/agents/`.

## Sobre el servidor Express antiguo (`integraciones/copilot-extension/`)

Ese código (con verificación de firma y streaming SSE) implementaba el protocolo viejo
de "Copilot Extensions" vía GitHub App. Se deja en el repo como referencia histórica,
pero **ya no es necesario ni es el camino recomendado** — el archivo
`.github/agents/vuln-scanner.agent.md` lo reemplaza por completo con muchísimo menos
esfuerzo.
