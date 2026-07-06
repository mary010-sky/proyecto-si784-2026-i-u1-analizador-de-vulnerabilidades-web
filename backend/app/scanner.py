from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from html import unescape
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from .schemas import DEFAULT_MODULES


SEVERITY_POINTS = {"critical": 40, "high": 25, "medium": 12, "low": 5, "info": 1}
SQL_ERROR_PATTERNS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlite error",
    "postgresql query failed",
    "ora-01756",
    "sqlstate",
    "mysql_fetch",
]
OPEN_REDIRECT_PARAMS = {"next", "url", "redirect", "redirect_uri", "return", "returnurl", "dest", "destination"}
CSRF_NAMES = {"csrf", "csrf_token", "_csrf", "_token", "authenticity_token", "xsrf", "xsrf_token"}

LFI_PAYLOADS = ["../../../../etc/passwd", "..%2f..%2f..%2f..%2fetc%2fpasswd", "....//....//....//etc/passwd"]
LFI_INDICATORS = ["root:x:0:0", "root:!:", "daemon:", "/bin/bash"]

CMD_INJECTION_PAYLOADS = ["; id", "| id", "`id`"]
CMD_INJECTION_INDICATORS = ["uid=", "gid=", "www-data", "root:x:0:0"]

SSRF_PARAM_NAMES = {"url", "src", "href", "path", "dest", "image", "file", "host", "proxy", "endpoint", "callback", "target"}
SSRF_INTERNAL_PROBE = "http://169.254.169.254/latest/meta-data/"
SSRF_INDICATORS = ["ami-id", "instance-id", "iam/security-credentials"]

DANGEROUS_HTTP_METHODS = ("PUT", "DELETE", "TRACE", "CONNECT")

ERROR_DISCLOSURE_INDICATORS = [
    "traceback (most recent call last)",
    "stack trace",
    "fatal error",
    "syntax error",
    "undefined variable",
    "warning: include",
    "exception in thread",
]

SENSITIVE_FILE_PROBES = [
    ("/.env", ["db_password", "secret", "app_key"], "critical", "Archivo .env expuesto",
     "Se pudo acceder a un archivo de variables de entorno con posibles secretos (CWE-200)."),
    ("/.git/HEAD", ["ref:"], "critical", "Repositorio Git expuesto",
     "El directorio .git es accesible, lo que puede permitir reconstruir el codigo fuente completo (CWE-200)."),
    ("/phpinfo.php", ["php version"], "high", "phpinfo expuesto",
     "La pagina phpinfo revela configuracion detallada del runtime (CWE-200)."),
    ("/server-status", ["server status"], "medium", "server-status expuesto",
     "El endpoint de estado del servidor parece accesible publicamente (CWE-200)."),
    ("/wp-config.php.bak", ["db_password"], "critical", "Backup de wp-config.php expuesto",
     "Un archivo de respaldo de configuracion con credenciales es accesible (CWE-530)."),
    ("/.htaccess", ["rewriteengine"], "low", "Archivo .htaccess expuesto",
     "El archivo de configuracion .htaccess es accesible publicamente (CWE-200)."),
]


@dataclass
class FetchedPage:
    url: str
    response: requests.Response
    body: str


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("La URL objetivo debe usar http o https.")
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))


def same_origin(base_url: str, candidate: str) -> bool:
    base = urlparse(base_url)
    other = urlparse(candidate)
    return other.scheme in {"http", "https"} and other.netloc == base.netloc


def replace_param(url: str, param: str, value: str) -> str:
    parsed = urlparse(url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    updated = [(key, value if key == param else current) for key, current in params]
    return urlunparse(parsed._replace(query=urlencode(updated, doseq=True)))


def build_vulnerability(
    module: str,
    severity: str,
    title: str,
    description: str,
    evidence: str | None,
    remediation: str,
    url: str,
    parameter: str | None = None,
) -> dict:
    return {
        "module": module,
        "severity": severity,
        "title": title,
        "description": description,
        "evidence": evidence,
        "remediation": remediation,
        "url": url,
        "parameter": parameter,
    }


def crawl_pages(target_url: str, depth: int, timeout: int) -> list[FetchedPage]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "WebVulnerabilityScanner/1.0 (authorized security assessment)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    )

    visited: set[str] = set()
    pages: list[FetchedPage] = []
    queue: deque[tuple[str, int]] = deque([(target_url, 0)])
    max_pages = 20

    while queue and len(pages) < max_pages:
        current_url, current_depth = queue.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = session.get(current_url, timeout=timeout, allow_redirects=True, verify=True)
        except requests.RequestException:
            continue

        body = response.text[:500_000]
        pages.append(FetchedPage(url=response.url, response=response, body=body))

        content_type = response.headers.get("content-type", "")
        if current_depth >= depth or "text/html" not in content_type:
            continue

        soup = BeautifulSoup(body, "html.parser")
        for anchor in soup.find_all("a", href=True):
            href = unescape(anchor.get("href", "")).strip()
            absolute = normalize_discovered_url(target_url, response.url, href)
            if absolute and same_origin(target_url, absolute) and absolute not in visited:
                queue.append((absolute, current_depth + 1))

    if not pages:
        raise RuntimeError("No se pudo obtener ninguna pagina del objetivo.")

    return pages


def normalize_discovered_url(target_url: str, current_url: str, href: str) -> str | None:
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None
    absolute = urljoin(current_url, href)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))


def check_headers(page: FetchedPage) -> list[dict]:
    headers = {key.lower(): value for key, value in page.response.headers.items()}
    checks = [
        (
            "content-security-policy",
            "medium",
            "Content-Security-Policy ausente",
            "La respuesta no define una politica CSP, lo que aumenta el impacto de XSS y carga de recursos no confiables.",
            "Definir una politica CSP restrictiva y monitorear violaciones en modo report-only antes de endurecerla.",
        ),
        (
            "x-frame-options",
            "medium",
            "X-Frame-Options ausente",
            "La aplicacion podria ser embebida en iframes y quedar expuesta a clickjacking.",
            "Configurar X-Frame-Options DENY/SAMEORIGIN o frame-ancestors en CSP.",
        ),
        (
            "x-content-type-options",
            "low",
            "X-Content-Type-Options ausente",
            "El navegador podria intentar interpretar recursos con un tipo distinto al declarado.",
            "Agregar X-Content-Type-Options: nosniff.",
        ),
        (
            "referrer-policy",
            "low",
            "Referrer-Policy ausente",
            "Las URLs completas podrian filtrarse como referrer hacia sitios externos.",
            "Configurar Referrer-Policy, por ejemplo strict-origin-when-cross-origin.",
        ),
        (
            "permissions-policy",
            "low",
            "Permissions-Policy ausente",
            "No se restringe explicitamente el uso de APIs sensibles del navegador.",
            "Definir Permissions-Policy segun las funciones realmente necesarias.",
        ),
    ]

    vulnerabilities = []
    for header, severity, title, description, remediation in checks:
        if header not in headers:
            vulnerabilities.append(
                build_vulnerability(
                    "headers",
                    severity,
                    title,
                    description,
                    None,
                    remediation,
                    page.url,
                )
            )

    if page.url.startswith("https://") and "strict-transport-security" not in headers:
        vulnerabilities.append(
            build_vulnerability(
                "headers",
                "medium",
                "Strict-Transport-Security ausente",
                "El sitio usa HTTPS pero no anuncia HSTS, por lo que clientes recurrentes no quedan protegidos contra downgrade.",
                None,
                "Agregar Strict-Transport-Security con max-age suficiente y evaluar includeSubDomains.",
                page.url,
            )
        )

    return vulnerabilities


def check_info_disclosure(page: FetchedPage) -> list[dict]:
    vulnerabilities = []
    server = page.response.headers.get("server")
    powered_by = page.response.headers.get("x-powered-by")
    if server:
        vulnerabilities.append(
            build_vulnerability(
                "info_disclosure",
                "low",
                "Cabecera Server expone tecnologia",
                "La cabecera Server revela informacion que puede ayudar a perfilar el stack.",
                server[:300],
                "Reducir o eliminar banners de version en el servidor web o proxy.",
                page.url,
            )
        )
    if powered_by:
        vulnerabilities.append(
            build_vulnerability(
                "info_disclosure",
                "low",
                "Cabecera X-Powered-By expone tecnologia",
                "La cabecera X-Powered-By revela framework o runtime de la aplicacion.",
                powered_by[:300],
                "Eliminar X-Powered-By en framework, servidor o proxy.",
                page.url,
            )
        )

    body = page.body.lower()
    indicators = [
        "traceback (most recent call last)",
        "stack trace",
        "debug mode",
        "notice: undefined",
        "warning: include",
        "fatal error",
        "database error",
        "exception in thread",
    ]
    for indicator in indicators:
        if indicator in body:
            vulnerabilities.append(
                build_vulnerability(
                    "info_disclosure",
                    "medium",
                    "Mensaje tecnico visible",
                    "La respuesta contiene trazas o mensajes tecnicos que podrian revelar rutas, consultas o detalles internos.",
                    indicator,
                    "Deshabilitar debug en produccion y retornar paginas de error genericas con logging interno.",
                    page.url,
                )
            )
            break

    return vulnerabilities


def check_csrf(page: FetchedPage) -> list[dict]:
    soup = BeautifulSoup(page.body, "html.parser")
    vulnerabilities = []
    for form in soup.find_all("form"):
        method = (form.get("method") or "get").lower()
        if method != "post":
            continue
        token_found = False
        for input_node in form.find_all("input"):
            name = (input_node.get("name") or "").lower()
            input_type = (input_node.get("type") or "").lower()
            if input_type == "hidden" and any(token in name for token in CSRF_NAMES):
                token_found = True
                break
        if not token_found:
            action = urljoin(page.url, form.get("action") or page.url)
            vulnerabilities.append(
                build_vulnerability(
                    "csrf",
                    "medium",
                    "Formulario POST sin token CSRF visible",
                    "Se detecto un formulario POST sin un campo oculto que parezca token anti-CSRF.",
                    f"action={action}",
                    "Agregar tokens CSRF por sesion o por request y validar SameSite en cookies de autenticacion.",
                    page.url,
                )
            )
    return vulnerabilities


def check_reflected_xss(page: FetchedPage, timeout: int) -> list[dict]:
    parsed = urlparse(page.url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    if not params:
        return []

    vulnerabilities = []
    session = requests.Session()
    payload = "<script>alert(1337)</script>"
    for name, _ in params[:8]:
        test_url = replace_param(page.url, name, payload)
        try:
            response = session.get(test_url, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue
        if payload in response.text:
            vulnerabilities.append(
                build_vulnerability(
                    "xss",
                    "high",
                    "Reflejo directo de payload XSS",
                    "Un parametro se refleja sin codificacion contextual aparente en la respuesta HTML.",
                    payload,
                    "Codificar salida segun contexto, validar entradas y reforzar con CSP.",
                    response.url,
                    name,
                )
            )
    return vulnerabilities


def check_sqli(page: FetchedPage, timeout: int) -> list[dict]:
    parsed = urlparse(page.url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    if not params:
        return []

    vulnerabilities = []
    baseline = page.body.lower()
    session = requests.Session()
    for name, current_value in params[:8]:
        test_url = replace_param(page.url, name, f"{current_value}'")
        try:
            response = session.get(test_url, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue
        body = response.text.lower()
        for pattern in SQL_ERROR_PATTERNS:
            if pattern in body and pattern not in baseline:
                vulnerabilities.append(
                    build_vulnerability(
                        "sqli",
                        "high",
                        "Error SQL inducido por parametro",
                        "El parametro produjo un mensaje de error SQL, senal de posible inyeccion basada en errores.",
                        pattern,
                        "Usar consultas parametrizadas, ORM seguro y manejo de errores generico.",
                        response.url,
                        name,
                    )
                )
                break
    return vulnerabilities


def check_open_redirect(page: FetchedPage, timeout: int) -> list[dict]:
    parsed = urlparse(page.url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    if not params:
        return []

    vulnerabilities = []
    session = requests.Session()
    payload = "https://example.com"
    for name, _ in params[:8]:
        if name.lower() not in OPEN_REDIRECT_PARAMS:
            continue
        test_url = replace_param(page.url, name, payload)
        try:
            response = session.get(test_url, timeout=timeout, allow_redirects=False)
        except requests.RequestException:
            continue
        location = response.headers.get("location", "")
        if response.status_code in {301, 302, 303, 307, 308} and location.startswith(payload):
            vulnerabilities.append(
                build_vulnerability(
                    "open_redirect",
                    "medium",
                    "Redireccion abierta",
                    "La aplicacion redirige hacia un dominio externo controlado por un parametro.",
                    f"Location: {location}",
                    "Permitir solo rutas relativas o destinos externos en lista de confianza.",
                    test_url,
                    name,
                )
            )
    return vulnerabilities


def probe_sensitive_files(target_url: str, timeout: int) -> list[dict]:
    parsed = urlparse(target_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    vulnerabilities = []
    session = requests.Session()
    for path, indicators, severity, title, description in SENSITIVE_FILE_PROBES:
        url = f"{base}{path}"
        try:
            response = session.get(url, timeout=timeout, allow_redirects=False)
        except requests.RequestException:
            continue
        if response.status_code != 200:
            continue
        text = response.text[:5000].lower()
        if not any(indicator in text for indicator in indicators):
            continue
        vulnerabilities.append(
            build_vulnerability(
                "info_disclosure",
                severity,
                title,
                description,
                url,
                f"Restringir el acceso a {path} desde la configuracion del servidor web y eliminar el archivo del webroot si no es necesario.",
                url,
            )
        )
    return vulnerabilities


def check_lfi(page: FetchedPage, timeout: int) -> list[dict]:
    parsed = urlparse(page.url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    if not params:
        return []

    session = requests.Session()
    for name, _ in params[:8]:
        for payload in LFI_PAYLOADS[:2]:
            test_url = replace_param(page.url, name, payload)
            try:
                response = session.get(test_url, timeout=timeout, allow_redirects=True)
            except requests.RequestException:
                continue
            if any(indicator in response.text for indicator in LFI_INDICATORS):
                return [
                    build_vulnerability(
                        "lfi",
                        "critical",
                        "Local File Inclusion (path traversal)",
                        "El parametro devuelve contenido de un archivo del sistema (/etc/passwd) mediante "
                        "path traversal (CWE-22).",
                        payload,
                        "Validar y sanitizar rutas de archivo, usar listas blancas de archivos permitidos y "
                        "evitar concatenar input de usuario directamente en rutas del sistema de archivos.",
                        response.url,
                        name,
                    )
                ]
    return []


def check_command_injection(page: FetchedPage, timeout: int) -> list[dict]:
    parsed = urlparse(page.url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    if not params:
        return []

    session = requests.Session()
    for name, _ in params[:8]:
        for payload in CMD_INJECTION_PAYLOADS[:2]:
            test_url = replace_param(page.url, name, payload)
            try:
                response = session.get(test_url, timeout=timeout, allow_redirects=True)
            except requests.RequestException:
                continue
            if any(indicator in response.text for indicator in CMD_INJECTION_INDICATORS):
                return [
                    build_vulnerability(
                        "command_injection",
                        "critical",
                        "Command Injection detectado",
                        "El servidor parece ejecutar comandos del sistema operativo a partir de un parametro "
                        "de usuario (CWE-78).",
                        payload,
                        "Nunca pasar input de usuario a funciones de shell del sistema; usar APIs seguras del "
                        "lenguaje en vez de invocar comandos externos, y validar/escapar cualquier argumento.",
                        response.url,
                        name,
                    )
                ]
    return []


def check_ssrf(page: FetchedPage, timeout: int) -> list[dict]:
    parsed = urlparse(page.url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    if not params:
        return []

    session = requests.Session()
    for name, _ in params[:8]:
        if name.lower() not in SSRF_PARAM_NAMES:
            continue
        test_url = replace_param(page.url, name, SSRF_INTERNAL_PROBE)
        try:
            response = session.get(test_url, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue
        if any(indicator in response.text for indicator in SSRF_INDICATORS):
            return [
                build_vulnerability(
                    "ssrf",
                    "critical",
                    "Server-Side Request Forgery (SSRF)",
                    "El parametro permite que el servidor realice peticiones hacia la metadata interna de la "
                    "nube u otros hosts internos (CWE-918).",
                    SSRF_INTERNAL_PROBE,
                    "Validar y restringir los destinos salientes con una lista blanca de hosts permitidos; "
                    "bloquear rangos de IP internos y de metadata en la capa de red.",
                    test_url,
                    name,
                )
            ]
    return []


def check_http_methods(target_url: str, timeout: int) -> list[dict]:
    try:
        response = requests.options(target_url, timeout=timeout)
    except requests.RequestException:
        return []

    allow = (response.headers.get("allow", "") + " " + response.headers.get("access-control-allow-methods", "")).upper()
    found = [method for method in DANGEROUS_HTTP_METHODS if method in allow]
    if not found:
        return []

    return [
        build_vulnerability(
            "http_methods",
            "medium",
            "Metodos HTTP peligrosos habilitados",
            f"El servidor permite los metodos {', '.join(found)}, que pueden usarse para modificar o eliminar "
            "recursos, o para ataques de Cross-Site Tracing (CWE-16).",
            allow.strip(),
            "Deshabilitar los metodos HTTP innecesarios (PUT, DELETE, TRACE, CONNECT) a nivel de servidor web "
            "o framework.",
            target_url,
        )
    ]


def check_error_disclosure(target_url: str, timeout: int) -> list[dict]:
    probe_url = target_url.rstrip("/") + "/__pagina_inexistente_12345__"
    try:
        response = requests.get(probe_url, timeout=timeout)
    except requests.RequestException:
        return []

    body = response.text.lower()
    for indicator in ERROR_DISCLOSURE_INDICATORS:
        if indicator in body:
            return [
                build_vulnerability(
                    "info_disclosure",
                    "medium",
                    "Mensajes de error detallados expuestos",
                    f"Una peticion a una ruta inexistente devuelve informacion tecnica interna "
                    f"('{indicator}'), lo que puede revelar rutas, framework o logica de la aplicacion "
                    "(CWE-209).",
                    indicator,
                    "Configurar paginas de error genericas en produccion y registrar el detalle tecnico "
                    "solo en logs internos, nunca en la respuesta al cliente.",
                    probe_url,
                )
            ]
    return []


def calculate_risk_score(vulnerabilities: list[dict]) -> int:
    score = sum(SEVERITY_POINTS.get(item.get("severity", "info").lower(), 0) for item in vulnerabilities)
    return min(score, 100)


def scan_target(target_url: str, modules: list[str], depth: int, timeout: int) -> tuple[list[dict], int]:
    enabled_modules = set(modules or DEFAULT_MODULES)
    normalized = normalize_url(target_url)
    pages = crawl_pages(normalized, depth, timeout)
    vulnerabilities: list[dict] = []

    for page in pages:
        if "headers" in enabled_modules:
            vulnerabilities.extend(check_headers(page))
        if "info_disclosure" in enabled_modules:
            vulnerabilities.extend(check_info_disclosure(page))
        if "csrf" in enabled_modules:
            vulnerabilities.extend(check_csrf(page))
        if "xss" in enabled_modules:
            vulnerabilities.extend(check_reflected_xss(page, timeout))
        if "sqli" in enabled_modules:
            vulnerabilities.extend(check_sqli(page, timeout))
        if "open_redirect" in enabled_modules:
            vulnerabilities.extend(check_open_redirect(page, timeout))
        if "lfi" in enabled_modules:
            vulnerabilities.extend(check_lfi(page, timeout))
        if "command_injection" in enabled_modules:
            vulnerabilities.extend(check_command_injection(page, timeout))
        if "ssrf" in enabled_modules:
            vulnerabilities.extend(check_ssrf(page, timeout))

    if "info_disclosure" in enabled_modules:
        vulnerabilities.extend(probe_sensitive_files(normalized, timeout))
        vulnerabilities.extend(check_error_disclosure(normalized, timeout))
    if "http_methods" in enabled_modules:
        vulnerabilities.extend(check_http_methods(normalized, timeout))

    return vulnerabilities, calculate_risk_score(vulnerabilities)

