<center>

![Logo UPT](media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto: Analizador de Vulnerabilidades Web — VulnScan Pro**

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

**Sistema: Analizador de Vulnerabilidades Web — VulnScan Pro**

**Estándar de Programación**

Versión 1.0

| CONTROL DE VERSIONES | | | | | |
|:---:|:---|:---|:---|:---|:---|
| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| 1.0 | M. Ramos | M. Calloticona | | 04/04/2026 | Versión Original |

<div style="page-break-after: always;"></div>

---

## ÍNDICE GENERAL

[1. Introducción](#1-introducción)

[2. Stack Tecnológico](#2-stack-tecnológico)

[3. Estándares de Nomenclatura](#3-estándares-de-nomenclatura)

- [3.1 Backend — Python / FastAPI](#31-backend--python--fastapi)
- [3.2 Frontend — TypeScript / Next.js](#32-frontend--typescript--nextjs)
- [3.3 Base de Datos — MySQL](#33-base-de-datos--mysql)
- [3.4 API REST — Endpoints](#34-api-rest--endpoints)

[4. Estructura de Archivos](#4-estructura-de-archivos)

[5. Estilo de Código](#5-estilo-de-código)

- [5.1 Python (PEP 8)](#51-python-pep-8)
- [5.2 TypeScript (Next.js)](#52-typescript-nextjs)

[6. Estándares de Documentación](#6-estándares-de-documentación)

[7. Manejo de Errores](#7-manejo-de-errores)

[8. Seguridad en el Código](#8-seguridad-en-el-código)

[9. Control de Versiones (Git)](#9-control-de-versiones-git)

[10. Pruebas](#10-pruebas)

<div style="page-break-after: always;"></div>

---

## 1. Introducción

El presente documento establece los estándares, convenciones y buenas prácticas de programación adoptados por el equipo de desarrollo del sistema **VulnScan Pro**. Su objetivo es garantizar la uniformidad, legibilidad, mantenibilidad y seguridad del código fuente en ambas capas del sistema (backend Python y frontend TypeScript).

Todos los integrantes del equipo deben adherirse a estas normas durante el desarrollo, revisión de código y pruebas. El incumplimiento de estos estándares deberá ser corregido antes de integrar código a la rama `main`.

**Ámbito de aplicación:**
- Backend: `backend/` — Python 3.11, FastAPI, SQLAlchemy
- Frontend: `frontend/` — TypeScript, Next.js 16, TailwindCSS
- Base de datos: MySQL 8.0
- Infraestructura: scripts Bash, configuración Nginx y systemd

---

## 2. Stack Tecnológico

| Capa | Tecnología | Versión | Propósito |
|:-----|:-----------|:-------:|:----------|
| Frontend | Next.js | 16.x | Framework React con App Router |
| Frontend | TypeScript | 5.x | Tipado estático |
| Frontend | TailwindCSS | 3.x | Estilos utilitarios |
| Frontend | Chart.js | 4.x | Gráficos del dashboard |
| Backend | Python | 3.11 | Lenguaje principal |
| Backend | FastAPI | 0.110+ | Framework API REST asíncrono |
| Backend | SQLAlchemy | 2.0 | ORM para base de datos |
| Backend | Pydantic | 2.x | Validación de datos y esquemas |
| Backend | python-jose | 3.x | Generación y verificación JWT |
| Backend | bcrypt / passlib | — | Hasheo de contraseñas |
| Backend | httpx | 0.27+ | Cliente HTTP asíncrono para módulos OWASP |
| Backend | WeasyPrint | 61+ | Generación de reportes PDF |
| Base de datos | MySQL | 8.0 | Motor de base de datos relacional |
| Infraestructura | Nginx | 1.24 | Proxy reverso, SSL, rate limiting |
| Infraestructura | Gunicorn | — | Servidor WSGI — 4 workers pre-fork |
| Infraestructura | PM2 | — | Process manager para Next.js |
| Infraestructura | systemd | — | Servicio del backend en producción |
| IA | DeepSeek AI | deepseek-chat | Análisis de vulnerabilidades |
| Testing | pytest | — | Framework de pruebas backend |
| Testing | pytest-cov | — | Cobertura de pruebas |
| Testing | mutmut | — | Pruebas de mutación |
| Testing | Playwright | — | Pruebas E2E del frontend |
| CI/CD | GitHub Actions | — | Pipeline de integración continua |

---

## 3. Estándares de Nomenclatura

### 3.1 Backend — Python / FastAPI

#### Variables y Atributos

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Variable local | `snake_case` | `scan_id`, `user_email` | `scanId`, `UserEmail` |
| Constante global | `UPPER_SNAKE_CASE` | `MAX_SCAN_TIMEOUT`, `JWT_ALGORITHM` | `max_timeout`, `jwtAlgorithm` |
| Atributo privado | `_snake_case` | `_cached_result` | `__cached_result`, `cachedResult` |
| Variable de entorno | `UPPER_SNAKE_CASE` | `DATABASE_URL`, `DEEPSEEK_API_KEY` | `database_url` |

#### Funciones y Métodos

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Función de negocio | `snake_case` + verbo | `run_full_scan()`, `calculate_risk_score()` | `fullScan()`, `riskScore()` |
| Función de ruta FastAPI | `snake_case` + sustantivo | `get_scan()`, `create_scan()`, `delete_user()` | `GetScan()`, `createScan()` |
| Función de módulo OWASP | `run_` + nombre_vuln | `run_sql_injection_scan()`, `run_xss_scan()` | `sqlInjectionScan()`, `checkXSS()` |
| Función auxiliar | `snake_case` | `validate_url()`, `build_prompt()` | `ValidateURL()`, `BuildPrompt()` |

#### Clases

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Modelo SQLAlchemy | `PascalCase`, singular | `User`, `Scan`, `Vulnerability` | `users`, `scan_model` |
| Esquema Pydantic | `PascalCase` + sufijo | `ScanCreate`, `UserResponse`, `VulnDetail` | `scan_create`, `userresp` |
| Clase de servicio | `PascalCase` + `Service` | `AIService`, `ScannerService` | `aiservice`, `scanner` |
| Excepción personalizada | `PascalCase` + `Error` | `ScanNotFoundError`, `AuthError` | `scan_error` |

#### Archivos y Módulos Python

| Tipo | Convención | Ejemplo |
|:-----|:-----------|:--------|
| Archivo de módulo | `snake_case.py` | `scan_routes.py`, `ai_service.py` |
| Archivo de prueba | `test_` + nombre | `test_scanner.py`, `test_auth.py` |
| Paquete | `snake_case/` con `__init__.py` | `routes/`, `services/` |

---

### 3.2 Frontend — TypeScript / Next.js

#### Variables y Constantes

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Variable local | `camelCase` | `scanId`, `userEmail`, `isLoading` | `scan_id`, `ScanId` |
| Constante de módulo | `UPPER_SNAKE_CASE` | `API_BASE_URL`, `MAX_RETRIES` | `apiBaseUrl`, `maxRetries` |
| Variable booleana | `is` / `has` / `can` + nombre | `isLoading`, `hasError`, `canExport` | `loading`, `error`, `exportable` |

#### Funciones y Hooks

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Función de lógica | `camelCase` + verbo | `startScan()`, `fetchResults()` | `start_scan()`, `StartScan()` |
| Hook personalizado | `use` + `PascalCase` | `useAuth()`, `useScanStatus()` | `authHook()`, `ScanHook()` |
| Handler de evento | `handle` + Evento | `handleSubmit()`, `handleClick()` | `onSubmit()`, `clickHandler()` |
| Función de API call | `camelCase` descriptivo | `getScanById()`, `createScan()` | `GetScan()`, `get_scan()` |

#### Componentes React

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Componente | `PascalCase` | `ScannerPage`, `SeverityBadge` | `scannerPage`, `severitybadge` |
| Archivo de componente | `PascalCase.tsx` | `Navbar.tsx`, `SeverityBadge.tsx` | `navbar.tsx`, `severity-badge.tsx` |
| Prop de componente | `camelCase` | `scanId`, `onSuccess`, `isVisible` | `scan_id`, `on_success` |

#### Interfaces y Tipos TypeScript

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Interface de datos | `PascalCase` | `ScanResult`, `VulnerabilityDetail` | `scan_result`, `vulndetail` |
| Type alias | `PascalCase` | `Severity`, `ScanStatus` | `severity`, `scan_status` |
| Props de componente | `PascalCase` + `Props` | `ScannerFormProps`, `BadgeProps` | `scannerProps`, `badge_props` |
| Enum TypeScript | `PascalCase` | `Role`, `ScanDepth` | `role`, `SCAN_DEPTH` |

#### Archivos y Rutas Next.js

| Tipo | Convención | Ejemplo |
|:-----|:-----------|:--------|
| Página (App Router) | `page.tsx` dentro de carpeta | `app/scanner/page.tsx` |
| Ruta dinámica | `[param]/page.tsx` | `app/scanner/[id]/page.tsx` |
| Layout | `layout.tsx` | `app/layout.tsx` |
| Componente reutilizable | `PascalCase.tsx` en `components/` | `components/Navbar.tsx` |
| Hook personalizado | `use*.ts` en `hooks/` | `hooks/useAuth.ts` |
| Utilidades API | `*.ts` en `lib/` | `lib/api.ts` |

---

### 3.3 Base de Datos — MySQL

| Tipo | Convención | Ejemplo correcto | Ejemplo incorrecto |
|:-----|:-----------|:-----------------|:-------------------|
| Nombre de tabla | `snake_case`, plural | `users`, `audit_logs`, `password_resets` | `User`, `AuditLogs`, `PasswordReset` |
| Nombre de columna | `snake_case` | `user_id`, `created_at`, `is_active` | `userId`, `CreatedAt`, `IsActive` |
| Clave primaria | `id` (siempre) | `id INT AUTO_INCREMENT PRIMARY KEY` | `user_id`, `pk_id` |
| Clave foránea | `{tabla_singular}_id` | `user_id`, `scan_id` | `userId`, `fkUser` |
| Índice | `idx_{tabla}_{columna}` | `idx_scans_user_id` | `scan_user_index` |
| Índice único | `uq_{tabla}_{columna}` | `uq_users_email` | `unique_email` |
| ENUM | `lowercase`, guion bajo | `'in_progress'`, `'local_fallback'` | `'InProgress'`, `'LOCAL_FALLBACK'` |

---

### 3.4 API REST — Endpoints

Los endpoints siguen la convención REST con sustantivos en plural y verbos HTTP para las acciones:

| Acción | Método HTTP | Patrón URL | Ejemplo |
|:-------|:-----------:|:-----------|:--------|
| Listar recursos | `GET` | `/recursos` | `GET /scans` |
| Obtener uno | `GET` | `/recursos/{id}` | `GET /scans/42` |
| Crear | `POST` | `/recursos` | `POST /scans` |
| Actualizar completo | `PUT` | `/recursos/{id}` | `PUT /admin/users/7` |
| Actualizar parcial | `PATCH` | `/recursos/{id}/accion` | `PATCH /admin/users/7/lock` |
| Eliminar | `DELETE` | `/recursos/{id}` | `DELETE /admin/users/7` |

**Prefijos por subsistema:**

| Prefijo | Módulo | Ejemplo |
|:--------|:-------|:--------|
| `/auth` | Autenticación | `POST /auth/login`, `GET /auth/me` |
| `/scans` | Escaneos | `POST /scans`, `GET /scans/{id}` |
| `/reports` | Reportes | `GET /reports/{scan_id}/pdf` |
| `/admin` | Administración | `GET /admin/users`, `GET /admin/audit-logs` |
| `/solutions` | Soluciones IA | `GET /solutions/{vuln_id}` |

**Códigos de respuesta HTTP usados:**

| Código | Significado | Cuándo usarlo |
|:------:|:------------|:--------------|
| `200` | OK | Operación exitosa con cuerpo de respuesta |
| `201` | Created | Recurso creado exitosamente |
| `202` | Accepted | Solicitud aceptada (escaneo en background iniciado) |
| `204` | No Content | Eliminación exitosa |
| `400` | Bad Request | Solicitud inválida (URL privada, datos incorrectos) |
| `401` | Unauthorized | Token JWT ausente, inválido o expirado |
| `403` | Forbidden | Rol insuficiente para la operación |
| `404` | Not Found | Recurso no encontrado |
| `409` | Conflict | Conflicto de estado (escaneo ya activo) |
| `422` | Unprocessable Entity | Error de validación de Pydantic |
| `429` | Too Many Requests | Rate limit excedido (Nginx) |
| `500` | Internal Server Error | Error no manejado del servidor |

---

## 4. Estructura de Archivos

```
vulnerabilidad/
│
├── backend/                        ← Subsistema Backend
│   ├── main.py                     ← Entrypoint: lifespan, CORS, middleware, routers
│   ├── database.py                 ← Conexión MySQL: engine, SessionLocal, Base
│   ├── models.py                   ← 7 modelos SQLAlchemy
│   ├── auth.py                     ← JWT: create/verify_token, get_current_user, require_role
│   ├── scanner.py                  ← Motor OWASP: 13 funciones + run_full_scan()
│   ├── ai_service.py               ← DeepSeek API client + AIService + fallback
│   ├── solutions_routes.py         ← Endpoints de soluciones IA
│   ├── requirements.txt            ← Dependencias Python con versiones fijas
│   ├── .env.example                ← Template de variables de entorno
│   ├── setup.cfg                   ← Configuración de pytest y mutmut
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_scanner.py         ← Pruebas del motor de escaneo
│   │   └── test_auth.py            ← Pruebas de autenticación
│   └── routes/
│       ├── auth_routes.py          ← /auth/*
│       ├── scan_routes.py          ← /scans/*
│       ├── admin_routes.py         ← /admin/*
│       └── report_routes.py        ← /reports/*
│
├── frontend/                       ← Subsistema Frontend
│   ├── package.json
│   ├── next.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── src/
│       ├── lib/
│       │   └── api.ts              ← Cliente API centralizado + tipos TypeScript
│       ├── hooks/
│       │   └── useAuth.ts          ← Hook de autenticación global
│       ├── components/
│       │   ├── Navbar.tsx
│       │   └── SeverityBadge.tsx
│       └── app/                    ← App Router Next.js
│           ├── layout.tsx
│           ├── page.tsx
│           ├── login/page.tsx
│           ├── register/page.tsx
│           ├── dashboard/page.tsx
│           ├── scanner/
│           │   ├── page.tsx
│           │   └── [id]/page.tsx
│           ├── admin/page.tsx
│           └── profile/page.tsx
│
├── .github/workflows/ci.yml        ← Pipeline GitHub Actions
├── nginx.conf                      ← Configuración Nginx
├── vulnscan-backend.service        ← Unidad systemd
├── deploy.sh                       ← Script de despliegue
└── docs/                           ← Documentación académica
```

---

## 5. Estilo de Código

### 5.1 Python (PEP 8)

#### Indentación y Longitud

```python
# CORRECTO — 4 espacios, líneas máximo 100 caracteres
def run_sql_injection_scan(url: str, timeout: int = 10) -> list[dict]:
    payloads = ["'", "\"", "1 OR 1=1", "1' OR '1'='1"]
    results = []
    for payload in payloads:
        try:
            response = httpx.get(url, params={"id": payload}, timeout=timeout)
            if any(err in response.text for err in SQL_ERROR_PATTERNS):
                results.append({"payload": payload, "evidence": response.text[:200]})
        except httpx.TimeoutException:
            continue
    return results

# INCORRECTO — tabs, líneas largas sin justificación
def run_sql_injection_scan(url,timeout=10):
	payloads=["'","\"","1 OR 1=1","1' OR '1'='1"]; results=[]
```

#### Imports

```python
# CORRECTO — orden: stdlib → third-party → local, agrupados
import os
import json
from datetime import datetime
from typing import Optional

import httpx
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Scan, Vulnerability
from auth import get_current_user
```

#### Type Hints — Obligatorios en funciones públicas

```python
# CORRECTO — type hints en parámetros y retorno
async def create_scan(
    scan_data: ScanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScanResponse:
    ...

# INCORRECTO — sin tipos
async def create_scan(scan_data, db, current_user):
    ...
```

#### Manejo de Excepciones

```python
# CORRECTO — excepciones específicas con mensaje claro
try:
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
except httpx.TimeoutException:
    raise HTTPException(status_code=408, detail="Timeout al conectar con el objetivo")
except httpx.HTTPStatusError as exc:
    raise HTTPException(status_code=502, detail=f"Error del servidor objetivo: {exc.response.status_code}")

# INCORRECTO — captura genérica sin manejo
try:
    response = httpx.get(url)
except Exception:
    pass
```

#### Constantes de Módulo

```python
# Al inicio del archivo, antes de funciones
SQL_ERROR_PATTERNS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
]

MAX_CRAWL_DEPTH = 2
DEFAULT_TIMEOUT = 10
```

---

### 5.2 TypeScript (Next.js)

#### Interfaces — Siempre sobre `any`

```typescript
// CORRECTO — interfaz tipada
interface ScanResult {
  id: number;
  target_url: string;
  status: "pending" | "in_progress" | "completed" | "failed";
  risk_score: number;
  vulnerabilities: VulnerabilityDetail[];
}

// INCORRECTO — any elimina el tipado
const scan: any = await getScanById(id);
```

#### Componentes — Props tipadas

```typescript
// CORRECTO
interface SeverityBadgeProps {
  severity: "critical" | "high" | "medium" | "low" | "info";
  className?: string;
}

export default function SeverityBadge({ severity, className }: SeverityBadgeProps) {
  const colors = {
    critical: "bg-red-600 text-white",
    high: "bg-orange-500 text-white",
    medium: "bg-yellow-400 text-black",
    low: "bg-green-500 text-white",
    info: "bg-blue-400 text-white",
  };
  return <span className={`px-2 py-1 rounded text-xs font-bold ${colors[severity]} ${className ?? ""}`}>{severity.toUpperCase()}</span>;
}
```

#### Llamadas a la API — Siempre con try/catch y tipos de retorno

```typescript
// CORRECTO — async/await con manejo de error
export async function createScan(data: ScanCreate): Promise<ScanResponse> {
  const response = await fetch("/api/scans", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail ?? "Error al crear el escaneo");
  }
  return response.json();
}
```

#### Hooks — Un hook por responsabilidad

```typescript
// CORRECTO — hook con responsabilidad única
export function useAuth() {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchCurrentUser(token).then(setUser).catch(() => setUser(null)).finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  return { user, isLoading, isAuthenticated: !!user };
}
```

---

## 6. Estándares de Documentación

### 6.1 Comentarios en Python

```python
# Solo cuando el "por qué" no es obvio — no documentar el "qué"

# CORRECTO — explica una decisión no obvia
# DeepSeek a veces retorna JSON mal formado dentro de markdown;
# extraemos el primer bloque ```json...``` antes de parsear
def parse_ai_response(raw: str) -> dict:
    match = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
    content = match.group(1) if match else raw
    return json.loads(content)

# INCORRECTO — comenta lo que ya dice el código
# Itera sobre la lista de payloads
for payload in payloads:
    ...
```

### 6.2 Comentarios en TypeScript/TSX

```typescript
// CORRECTO — documenta comportamiento no obvio
// El polling se detiene automáticamente al montar/desmontar;
// usar ref para evitar stale closure en el intervalo
const intervalRef = useRef<NodeJS.Timeout | null>(null);

// INCORRECTO — el nombre ya lo dice todo
// Establece el estado de carga en true
setIsLoading(true);
```

### 6.3 Docstrings Python — Solo en funciones públicas complejas

```python
def run_full_scan(scan_id: int, url: str, depth: str, tech_stack: str | None, use_ai: bool) -> None:
    """Ejecuta el ciclo completo de escaneo DAST para un Scan dado.

    Corre los 13 módulos OWASP secuencialmente, registra vulnerabilidades
    en BD, opcionalmente las analiza con DeepSeek AI, calcula el risk_score
    y actualiza el Scan a status='completed'.

    Args:
        scan_id: ID del registro Scan en la base de datos.
        url: URL objetivo validada (no IP privada).
        depth: Nivel de profundidad ('basic', 'standard', 'full').
        tech_stack: Stack tecnológico declarado o None.
        use_ai: Si True, llama a AIService por cada vulnerabilidad.
    """
```

---

## 7. Manejo de Errores

### 7.1 Backend — FastAPI

**Jerarquía de errores:**

| Error | Código HTTP | Cuándo usarlo |
|:------|:-----------:|:--------------|
| `HTTPException(400)` | 400 | URL privada, datos lógicamente inválidos |
| `HTTPException(401)` | 401 | Token ausente o inválido |
| `HTTPException(403)` | 403 | Rol insuficiente |
| `HTTPException(404)` | 404 | Recurso no encontrado |
| `HTTPException(409)` | 409 | Conflicto de estado |
| `HTTPException(422)` | 422 | Error Pydantic (automático) |
| `HTTPException(500)` | 500 | Error interno no previsto |

```python
# CORRECTO — error específico con mensaje en español
def get_scan_or_404(scan_id: int, user_id: int, db: Session) -> Scan:
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == user_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail=f"Escaneo {scan_id} no encontrado")
    return scan
```

### 7.2 Frontend — TypeScript

```typescript
// CORRECTO — estado de error visible al usuario
const [error, setError] = useState<string | null>(null);

try {
  const result = await createScan(formData);
  router.push(`/scanner/${result.id}`);
} catch (err) {
  setError(err instanceof Error ? err.message : "Error inesperado al iniciar el escaneo");
}

// En el JSX
{error && (
  <div className="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}
```

---

## 8. Seguridad en el Código

### 8.1 Reglas Obligatorias de Seguridad

| # | Regla | Descripción |
|:-:|:------|:------------|
| S-01 | **Sin secretos en código** | Nunca escribir API keys, contraseñas o tokens directamente en el código. Usar variables de entorno (`.env`). |
| S-02 | **Validar URL objetivo** | Antes de escanear, verificar que la URL no apunta a IP privadas (10.x, 172.16-31.x, 192.168.x, 127.x, localhost). |
| S-03 | **Hasheo obligatorio** | Nunca almacenar contraseñas en texto plano. Usar `bcrypt` con cost=10 mínimo. |
| S-04 | **Verificar propiedad** | Antes de retornar un escaneo o reporte, verificar que `scan.user_id == current_user.id`. |
| S-05 | **RBAC en cada endpoint** | Usar `require_role("admin")` en todos los endpoints de administración. |
| S-06 | **Sin eval/exec dinámico** | Prohibido usar `eval()`, `exec()`, `subprocess.call(shell=True)` con input del usuario. |
| S-07 | **Escapar salidas HTML** | En reportes HTML, usar Jinja2 autoescaping o funciones de escape explícitas. |
| S-08 | **Rate limiting en login** | El endpoint `/auth/login` debe estar bajo la zona de rate limiting estricto de Nginx (5 req/min). |
| S-09 | **Headers de seguridad** | Nginx debe enviar: `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`, `Strict-Transport-Security`. |
| S-10 | **AuditLog en acciones críticas** | Toda acción que modifique datos de usuarios, inicie escaneos o exporte reportes debe registrarse en `audit_logs`. |

### 8.2 Patrones Prohibidos

```python
# PROHIBIDO — secretos hardcodeados
JWT_SECRET = "mi_clave_secreta_123"
DEEPSEEK_KEY = "sk-abc123xyz"

# CORRECTO — desde variables de entorno
import os
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

# PROHIBIDO — shell injection
import subprocess
subprocess.call(f"ping {user_input}", shell=True)

# PROHIBIDO — SQL raw con interpolación
db.execute(f"SELECT * FROM users WHERE email = '{user_email}'")

# CORRECTO — ORM con parámetros
db.query(User).filter(User.email == user_email).first()
```

---

## 9. Control de Versiones (Git)

### 9.1 Estrategia de Ramas

| Rama | Propósito |
|:-----|:----------|
| `main` | Código en producción — protegida, requiere PR |
| `develop` | Integración de features — rama base para PRs |
| `feature/nombre-descriptivo` | Nueva funcionalidad |
| `fix/nombre-del-bug` | Corrección de errores |
| `docs/nombre-documento` | Cambios solo en documentación |

### 9.2 Convención de Commits (Conventional Commits)

**Formato:** `tipo(alcance): descripción breve en español`

| Tipo | Cuándo usarlo |
|:-----|:--------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Cambio en documentación |
| `refactor` | Refactorización sin cambio de funcionalidad |
| `test` | Agregar o corregir pruebas |
| `ci` | Cambios en pipeline CI/CD |
| `chore` | Tareas de mantenimiento (deps, config) |

**Ejemplos correctos:**

```
feat(scanner): agrega módulo de detección de SSRF
fix(auth): corrige bloqueo de cuenta que no se reseteaba tras login exitoso
test(scanner): agrega pruebas de mutación para módulo SQLi
docs(fd03): agrega diagramas de secuencia para UC-01 a UC-13
ci(actions): migra deploy de gh-pages a native GitHub Pages
```

### 9.3 Pull Requests

- El título del PR sigue la misma convención que los commits
- El cuerpo incluye: resumen de cambios, cómo probar, screenshots si aplica
- Todo PR debe pasar el pipeline CI/CD antes de hacer merge
- Al menos un integrante del equipo debe revisar el PR

---

## 10. Pruebas

### 10.1 Backend — pytest

**Estructura de pruebas:**

```python
# tests/test_scanner.py — patrón Arrange / Act / Assert
def test_run_headers_scan_detects_missing_csp(mock_response):
    # Arrange
    mock_response.headers = {"Content-Type": "text/html"}
    url = "https://example.com"

    # Act
    result = run_headers_scan(url)

    # Assert
    assert any(v["vuln_type"] == "Missing Content-Security-Policy" for v in result)
```

**Cobertura mínima requerida:** 70% (configurado en `setup.cfg`)

**Ejecutar pruebas:**
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html
```

### 10.2 Pruebas de Mutación — mutmut

```bash
cd backend
mutmut run
mutmut results
```

**Configuración en `setup.cfg`:**
```ini
[mutmut]
paths_to_mutate=app/scanner.py
runner=python -m pytest tests/test_scanner.py -x -q --no-cov
tests_dir=tests/
```

### 10.3 Frontend — Playwright (E2E)

```typescript
// tests/e2e/scanner.spec.ts — patrón Page Object
test("usuario puede iniciar escaneo y ver resultados", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[name="email"]', "test@upt.pe");
  await page.fill('[name="password"]', "Test1234!");
  await page.click('button[type="submit"]');
  await page.waitForURL("/dashboard");

  await page.goto("/scanner");
  await page.fill('[name="url"]', "https://example.com");
  await page.click('button:has-text("Iniciar Escaneo")');
  await page.waitForURL(/\/scanner\/\d+/);
  await expect(page.locator('[data-testid="risk-score"]')).toBeVisible({ timeout: 60000 });
});
```

### 10.4 Criterios de Calidad del CI/CD

| Verificación | Herramienta | Umbral mínimo |
|:-------------|:------------|:-------------:|
| Pruebas unitarias | pytest | 100% pasos |
| Cobertura de código | pytest-cov | ≥ 70% |
| Pruebas de mutación | mutmut | Ejecutadas |
| Análisis estático | SonarCloud | Sin bloqueantes |
| Análisis SAST | Semgrep | Sin críticos |
| Pruebas E2E | Playwright | Flujos principales OK |
