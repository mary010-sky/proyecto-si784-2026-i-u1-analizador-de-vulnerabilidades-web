"""
Pruebas unitarias para app/scanner.py -- el motor real desplegado en produccion.
Estrategia anti-mutantes:
  - Cada constante global verificada con test que la usa directamente.
  - Cada rama True/False cubierta con par de tests (positivo + negativo).
  - Valores exactos de severidad y modulo verificados, no solo presencia.
  - Cada patron de deteccion probado individualmente.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch, call
import pytest
import requests as req_lib

from app.scanner import (
    FetchedPage,
    build_vulnerability,
    calculate_risk_score,
    check_command_injection,
    check_csrf,
    check_error_disclosure,
    check_headers,
    check_http_methods,
    check_info_disclosure,
    check_lfi,
    check_open_redirect,
    check_reflected_xss,
    check_sqli,
    check_ssrf,
    normalize_url,
    probe_sensitive_files,
    replace_param,
    same_origin,
    SQL_ERROR_PATTERNS,
    OPEN_REDIRECT_PARAMS,
    CSRF_NAMES,
    LFI_PAYLOADS,
    LFI_INDICATORS,
    CMD_INJECTION_PAYLOADS,
    CMD_INJECTION_INDICATORS,
    SSRF_PARAM_NAMES,
    SSRF_INTERNAL_PROBE,
    SSRF_INDICATORS,
    DANGEROUS_HTTP_METHODS,
    ERROR_DISCLOSURE_INDICATORS,
    SEVERITY_POINTS,
    SENSITIVE_FILE_PROBES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _mock_response(status=200, headers=None, text="", url="http://example.com/"):
    resp = MagicMock(spec=req_lib.Response)
    resp.status_code = status
    resp.headers = headers or {}
    resp.text = text
    resp.url = url
    return resp


def _page(url="http://example.com/", headers=None, text="", status=200):
    resp = _mock_response(status=status, headers=headers, text=text, url=url)
    return FetchedPage(url=url, response=resp, body=text)


# ── Constantes globales ───────────────────────────────────────────────────────

class TestConstants:
    """Verifica que las constantes tienen los valores exactos esperados.
    Mata mutantes que cambien strings o eliminen elementos de listas."""

    def test_sql_error_patterns_contains_mysql(self):
        assert "you have an error in your sql syntax" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_warning_mysql(self):
        assert "warning: mysql" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_unclosed(self):
        assert "unclosed quotation mark" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_quoted_string(self):
        assert "quoted string not properly terminated" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_sqlite(self):
        assert "sqlite error" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_postgresql(self):
        assert "postgresql query failed" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_ora(self):
        assert "ora-01756" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_sqlstate(self):
        assert "sqlstate" in SQL_ERROR_PATTERNS

    def test_sql_error_patterns_contains_mysql_fetch(self):
        assert "mysql_fetch" in SQL_ERROR_PATTERNS

    def test_open_redirect_params_contains_next(self):
        assert "next" in OPEN_REDIRECT_PARAMS

    def test_open_redirect_params_contains_url(self):
        assert "url" in OPEN_REDIRECT_PARAMS

    def test_open_redirect_params_contains_redirect(self):
        assert "redirect" in OPEN_REDIRECT_PARAMS

    def test_open_redirect_params_contains_return(self):
        assert "return" in OPEN_REDIRECT_PARAMS

    def test_open_redirect_params_contains_dest(self):
        assert "dest" in OPEN_REDIRECT_PARAMS

    def test_csrf_names_contains_csrf(self):
        assert "csrf" in CSRF_NAMES

    def test_csrf_names_contains_csrf_token(self):
        assert "csrf_token" in CSRF_NAMES

    def test_csrf_names_contains_underscore_csrf(self):
        assert "_csrf" in CSRF_NAMES

    def test_csrf_names_contains_authenticity_token(self):
        assert "authenticity_token" in CSRF_NAMES

    def test_lfi_indicators_contains_root(self):
        assert "root:x:0:0" in LFI_INDICATORS

    def test_lfi_indicators_contains_bin_bash(self):
        assert "/bin/bash" in LFI_INDICATORS

    def test_lfi_indicators_contains_daemon(self):
        assert "daemon:" in LFI_INDICATORS

    def test_cmd_indicators_contains_uid(self):
        assert "uid=" in CMD_INJECTION_INDICATORS

    def test_cmd_indicators_contains_gid(self):
        assert "gid=" in CMD_INJECTION_INDICATORS

    def test_cmd_indicators_contains_www_data(self):
        assert "www-data" in CMD_INJECTION_INDICATORS

    def test_ssrf_param_names_contains_url(self):
        assert "url" in SSRF_PARAM_NAMES

    def test_ssrf_param_names_contains_src(self):
        assert "src" in SSRF_PARAM_NAMES

    def test_ssrf_param_names_contains_host(self):
        assert "host" in SSRF_PARAM_NAMES

    def test_ssrf_param_names_contains_proxy(self):
        assert "proxy" in SSRF_PARAM_NAMES

    def test_ssrf_internal_probe_is_metadata_url(self):
        assert "169.254.169.254" in SSRF_INTERNAL_PROBE

    def test_ssrf_indicators_contains_ami_id(self):
        assert "ami-id" in SSRF_INDICATORS

    def test_ssrf_indicators_contains_instance_id(self):
        assert "instance-id" in SSRF_INDICATORS

    def test_ssrf_indicators_contains_iam(self):
        assert "iam/security-credentials" in SSRF_INDICATORS

    def test_dangerous_methods_contains_put(self):
        assert "PUT" in DANGEROUS_HTTP_METHODS

    def test_dangerous_methods_contains_delete(self):
        assert "DELETE" in DANGEROUS_HTTP_METHODS

    def test_dangerous_methods_contains_trace(self):
        assert "TRACE" in DANGEROUS_HTTP_METHODS

    def test_dangerous_methods_contains_connect(self):
        assert "CONNECT" in DANGEROUS_HTTP_METHODS

    def test_error_indicators_contains_traceback(self):
        assert "traceback (most recent call last)" in ERROR_DISCLOSURE_INDICATORS

    def test_error_indicators_contains_stack_trace(self):
        assert "stack trace" in ERROR_DISCLOSURE_INDICATORS

    def test_error_indicators_contains_fatal_error(self):
        assert "fatal error" in ERROR_DISCLOSURE_INDICATORS

    def test_error_indicators_contains_syntax_error(self):
        assert "syntax error" in ERROR_DISCLOSURE_INDICATORS

    def test_severity_points_critical(self):
        assert SEVERITY_POINTS["critical"] == 40

    def test_severity_points_high(self):
        assert SEVERITY_POINTS["high"] == 25

    def test_severity_points_medium(self):
        assert SEVERITY_POINTS["medium"] == 12

    def test_severity_points_low(self):
        assert SEVERITY_POINTS["low"] == 5

    def test_severity_points_info(self):
        assert SEVERITY_POINTS["info"] == 1


# ── build_vulnerability() ─────────────────────────────────────────────────────

class TestBuildVulnerability:
    def test_todos_los_campos_obligatorios(self):
        v = build_vulnerability("sqli", "high", "SQL Injection", "desc", "evid", "remediation", "http://x.com")
        assert v["module"] == "sqli"
        assert v["severity"] == "high"
        assert v["title"] == "SQL Injection"
        assert v["description"] == "desc"
        assert v["evidence"] == "evid"
        assert v["remediation"] == "remediation"
        assert v["url"] == "http://x.com"
        assert v["parameter"] is None

    def test_parametro_none_por_defecto(self):
        v = build_vulnerability("csrf", "medium", "T", "d", None, "sol", "http://x.com")
        assert v["parameter"] is None

    def test_parametro_explicito(self):
        v = build_vulnerability("xss", "high", "T", "d", "payload", "sol", "http://x.com", "q")
        assert v["parameter"] == "q"

    def test_evidence_puede_ser_none(self):
        v = build_vulnerability("headers", "low", "T", "d", None, "sol", "http://x.com")
        assert v["evidence"] is None

    def test_severity_exacto(self):
        for sev in ("critical", "high", "medium", "low", "info"):
            v = build_vulnerability("m", sev, "t", "d", None, "s", "http://x.com")
            assert v["severity"] == sev


# ── normalize_url() ───────────────────────────────────────────────────────────

class TestNormalizeUrl:
    def test_normaliza_https(self):
        assert normalize_url("https://example.com") == "https://example.com/"

    def test_normaliza_http(self):
        assert normalize_url("http://example.com/path?q=1") == "http://example.com/path?q=1"

    def test_rechaza_ftp(self):
        with pytest.raises(ValueError):
            normalize_url("ftp://example.com")

    def test_rechaza_sin_host(self):
        with pytest.raises(ValueError):
            normalize_url("https://")

    def test_rechaza_sin_esquema(self):
        with pytest.raises(ValueError):
            normalize_url("example.com/path")

    def test_conserva_query_string(self):
        result = normalize_url("https://site.com/search?q=hello&page=2")
        assert "q=hello" in result
        assert "page=2" in result

    def test_path_vacio_se_convierte_en_slash(self):
        result = normalize_url("https://example.com")
        assert result.endswith("/")


# ── same_origin() ─────────────────────────────────────────────────────────────

class TestSameOrigin:
    def test_mismo_dominio_es_true(self):
        assert same_origin("https://example.com/a", "https://example.com/b") is True

    def test_distinto_dominio_es_false(self):
        assert same_origin("https://example.com", "https://evil.com") is False

    def test_subdominio_es_false(self):
        assert same_origin("https://example.com", "https://sub.example.com") is False

    def test_mismo_dominio_distinto_esquema_es_true(self):
        # same_origin solo compara netloc, no esquema
        assert same_origin("https://example.com", "http://example.com") is True

    def test_esquema_invalido_es_false(self):
        assert same_origin("https://example.com", "ftp://example.com") is False

    def test_javascript_es_false(self):
        assert same_origin("https://example.com", "javascript:void(0)") is False


# ── replace_param() ───────────────────────────────────────────────────────────

class TestReplaceParam:
    def test_reemplaza_param_existente(self):
        url = "http://example.com/search?q=hello&page=1"
        result = replace_param(url, "q", "PAYLOAD")
        assert "q=PAYLOAD" in result
        assert "page=1" in result

    def test_no_modifica_otros_params(self):
        url = "http://example.com/?a=1&b=2&c=3"
        result = replace_param(url, "b", "X")
        assert "a=1" in result
        assert "b=X" in result
        assert "c=3" in result

    def test_conserva_esquema_y_host(self):
        url = "https://mysite.com/path?x=1"
        result = replace_param(url, "x", "test")
        assert result.startswith("https://mysite.com/path")

    def test_url_sin_param_objetivo_no_cambia_otros(self):
        url = "http://x.com/?a=1"
        result = replace_param(url, "nonexistent", "val")
        assert "a=1" in result


# ── calculate_risk_score() ────────────────────────────────────────────────────

class TestCalculateRiskScore:
    def test_cero_sin_hallazgos(self):
        assert calculate_risk_score([]) == 0

    def test_critico_vale_40(self):
        assert calculate_risk_score([{"severity": "critical"}]) == 40

    def test_high_vale_25(self):
        assert calculate_risk_score([{"severity": "high"}]) == 25

    def test_medium_vale_12(self):
        assert calculate_risk_score([{"severity": "medium"}]) == 12

    def test_low_vale_5(self):
        assert calculate_risk_score([{"severity": "low"}]) == 5

    def test_info_vale_1(self):
        assert calculate_risk_score([{"severity": "info"}]) == 1

    def test_suma_varias_severidades(self):
        vulns = [{"severity": "critical"}, {"severity": "low"}]
        assert calculate_risk_score(vulns) == 45

    def test_tope_en_100(self):
        vulns = [{"severity": "critical"}] * 10
        assert calculate_risk_score(vulns) == 100

    def test_severidad_desconocida_suma_cero(self):
        assert calculate_risk_score([{"severity": "unknown"}]) == 0

    def test_severidad_en_mayusculas_suma_cero(self):
        # La funcion hace .lower() — este test verifica que la normalizacion funciona
        assert calculate_risk_score([{"severity": "CRITICAL"}]) == 40


# ── check_headers() ───────────────────────────────────────────────────────────

class TestCheckHeaders:
    def test_detecta_csp_faltante(self):
        findings = check_headers(_page(headers={}))
        assert any("Content-Security-Policy" in f["title"] for f in findings)

    def test_detecta_xframe_faltante(self):
        findings = check_headers(_page(headers={}))
        assert any("X-Frame-Options" in f["title"] for f in findings)

    def test_detecta_x_content_type_faltante(self):
        findings = check_headers(_page(headers={}))
        assert any("X-Content-Type-Options" in f["title"] for f in findings)

    def test_detecta_referrer_policy_faltante(self):
        findings = check_headers(_page(headers={}))
        assert any("Referrer-Policy" in f["title"] for f in findings)

    def test_detecta_permissions_policy_faltante(self):
        findings = check_headers(_page(headers={}))
        assert any("Permissions-Policy" in f["title"] for f in findings)

    def test_detecta_hsts_faltante_en_https(self):
        page = _page(url="https://example.com/", headers={})
        findings = check_headers(page)
        assert any("Strict-Transport-Security" in f["title"] for f in findings)

    def test_hsts_no_aplica_en_http(self):
        headers = {
            "content-security-policy": "x", "x-frame-options": "DENY",
            "x-content-type-options": "nosniff", "referrer-policy": "x",
            "permissions-policy": "x",
        }
        page = _page(url="http://example.com/", headers=headers)
        findings = check_headers(page)
        assert not any("Strict-Transport-Security" in f["title"] for f in findings)

    def test_no_falso_positivo_con_headers_completos_https(self):
        headers = {
            "x-frame-options": "DENY",
            "content-security-policy": "default-src 'self'",
            "strict-transport-security": "max-age=31536000",
            "x-content-type-options": "nosniff",
            "referrer-policy": "strict-origin-when-cross-origin",
            "permissions-policy": "camera=()",
        }
        assert check_headers(_page(url="https://example.com/", headers=headers)) == []

    def test_modulo_es_headers(self):
        findings = check_headers(_page(headers={}))
        assert all(f["module"] == "headers" for f in findings)

    def test_csp_severity_es_medium(self):
        findings = check_headers(_page(headers={}))
        csp = next(f for f in findings if "Content-Security-Policy" in f["title"])
        assert csp["severity"] == "medium"

    def test_xframe_severity_es_medium(self):
        findings = check_headers(_page(headers={}))
        xf = next(f for f in findings if "X-Frame-Options" in f["title"])
        assert xf["severity"] == "medium"

    def test_x_content_type_severity_es_low(self):
        findings = check_headers(_page(headers={}))
        xct = next(f for f in findings if "X-Content-Type-Options" in f["title"])
        assert xct["severity"] == "low"

    def test_hsts_severity_es_medium(self):
        page = _page(url="https://example.com/", headers={})
        findings = check_headers(page)
        hsts = next(f for f in findings if "Strict-Transport-Security" in f["title"])
        assert hsts["severity"] == "medium"

    def test_url_del_finding_es_la_del_page(self):
        page = _page(url="http://target.com/", headers={})
        findings = check_headers(page)
        assert all(f["url"] == "http://target.com/" for f in findings)


# ── check_info_disclosure() ──────────────────────────────────────────────────

class TestCheckInfoDisclosure:
    def test_detecta_server_header(self):
        findings = check_info_disclosure(_page(headers={"server": "nginx/1.18.0"}))
        assert any("Server" in f["title"] for f in findings)

    def test_server_severity_es_low(self):
        findings = check_info_disclosure(_page(headers={"server": "Apache/2.4"}))
        srv = next(f for f in findings if "Server" in f["title"])
        assert srv["severity"] == "low"

    def test_server_evidence_es_el_valor(self):
        findings = check_info_disclosure(_page(headers={"server": "nginx/1.18.0"}))
        srv = next(f for f in findings if "Server" in f["title"])
        assert srv["evidence"] == "nginx/1.18.0"

    def test_detecta_x_powered_by(self):
        findings = check_info_disclosure(_page(headers={"x-powered-by": "PHP/8.1.0"}))
        assert any("X-Powered-By" in f["title"] for f in findings)

    def test_x_powered_by_severity_es_low(self):
        findings = check_info_disclosure(_page(headers={"x-powered-by": "Express"}))
        xp = next(f for f in findings if "X-Powered-By" in f["title"])
        assert xp["severity"] == "low"

    def test_detecta_traceback_en_body(self):
        page = _page(text="Traceback (most recent call last): ...")
        findings = check_info_disclosure(page)
        assert any("tecnico" in f["title"].lower() for f in findings)

    def test_detecta_stack_trace_en_body(self):
        page = _page(text="stack trace at app.js:42")
        findings = check_info_disclosure(page)
        assert any(f["module"] == "info_disclosure" for f in findings)

    def test_detecta_fatal_error_en_body(self):
        page = _page(text="Fatal error: Call to undefined function")
        findings = check_info_disclosure(page)
        assert any(f["module"] == "info_disclosure" for f in findings)

    def test_detecta_database_error(self):
        page = _page(text="database error on line 42")
        findings = check_info_disclosure(page)
        assert any(f["module"] == "info_disclosure" for f in findings)

    def test_sin_hallazgos_en_respuesta_limpia(self):
        assert check_info_disclosure(_page(headers={}, text="<html>todo bien</html>")) == []

    def test_break_despues_del_primer_indicador(self):
        page = _page(text="traceback (most recent call last)\nstack trace\nfatal error")
        findings = check_info_disclosure(page)
        # Solo un finding por pagina (break despues de primer match)
        tech_findings = [f for f in findings if "tecnico" in f["title"].lower()]
        assert len(tech_findings) == 1

    def test_modulo_es_info_disclosure(self):
        findings = check_info_disclosure(_page(headers={"server": "nginx"}))
        assert all(f["module"] == "info_disclosure" for f in findings)


# ── check_csrf() ──────────────────────────────────────────────────────────────

class TestCheckCsrf:
    def test_detecta_form_post_sin_token(self):
        html = "<form method='post' action='/login'><input name='user'></form>"
        findings = check_csrf(_page(text=html))
        assert len(findings) == 1
        assert findings[0]["module"] == "csrf"

    def test_detecta_multiples_forms_sin_token(self):
        html = (
            "<form method='post' action='/a'><input name='x'></form>"
            "<form method='post' action='/b'><input name='y'></form>"
        )
        findings = check_csrf(_page(text=html))
        assert len(findings) == 2

    def test_no_reporta_con_csrf_token(self):
        html = "<form method='post'><input type='hidden' name='csrf_token' value='abc'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_no_reporta_con_csrf(self):
        html = "<form method='post'><input type='hidden' name='csrf' value='xyz'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_no_reporta_con_underscore_csrf(self):
        html = "<form method='post'><input type='hidden' name='_csrf' value='xyz'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_no_reporta_con_authenticity_token(self):
        html = "<form method='post'><input type='hidden' name='authenticity_token' value='xyz'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_no_reporta_con_xsrf_token(self):
        html = "<form method='post'><input type='hidden' name='xsrf_token' value='xyz'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_ignora_forms_get(self):
        html = "<form method='get' action='/search'><input name='q'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_form_sin_method_tratado_como_get(self):
        html = "<form action='/do'><input name='x'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_token_debe_ser_hidden(self):
        # Token no-hidden no debe contar como proteccion
        html = "<form method='post'><input type='text' name='csrf_token' value='abc'></form>"
        findings = check_csrf(_page(text=html))
        assert len(findings) == 1

    def test_severity_csrf_es_medium(self):
        html = "<form method='post'><input name='user'></form>"
        findings = check_csrf(_page(text=html))
        assert findings[0]["severity"] == "medium"


# ── check_reflected_xss() ────────────────────────────────────────────────────

class TestCheckReflectedXss:
    def test_detecta_reflejo_de_payload(self):
        page = _page(url="http://example.com/search?q=hello")
        response = _mock_response(text="...<script>alert(1337)</script>...")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_reflected_xss(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "xss"
        assert findings[0]["parameter"] == "q"
        assert findings[0]["severity"] == "high"

    def test_sin_parametros_retorna_lista_vacia(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_reflected_xss(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()

    def test_no_reporta_si_no_hay_reflejo(self):
        page = _page(url="http://example.com/search?q=hello")
        response = _mock_response(text="<html>pagina normal sin payload</html>")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_reflected_xss(page, timeout=5)
        assert findings == []

    def test_payload_es_el_script_alert(self):
        page = _page(url="http://example.com/?q=x")
        response = _mock_response(text="<script>alert(1337)</script>")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_reflected_xss(page, timeout=5)
        assert findings[0]["evidence"] == "<script>alert(1337)</script>"

    def test_request_exception_no_rompe(self):
        page = _page(url="http://example.com/?q=x")
        with patch.object(req_lib.Session, "get", side_effect=req_lib.RequestException("err")):
            findings = check_reflected_xss(page, timeout=5)
        assert findings == []

    def test_limita_a_8_parametros(self):
        url = "http://x.com/?" + "&".join(f"p{i}=v{i}" for i in range(12))
        page = _page(url=url)
        call_count = [0]
        def fake_get(self, u, **kw):
            call_count[0] += 1
            return _mock_response(text="safe")
        with patch.object(req_lib.Session, "get", fake_get):
            check_reflected_xss(page, timeout=5)
        assert call_count[0] <= 8


# ── check_sqli() ──────────────────────────────────────────────────────────────

class TestCheckSqli:
    def test_detecta_error_mysql(self):
        page = _page(url="http://example.com/item?id=1", text="clean page")
        resp = _mock_response(text="you have an error in your sql syntax near '1'")
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_sqli(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "sqli"
        assert findings[0]["severity"] == "high"

    def test_detecta_warning_mysql(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        resp = _mock_response(text="Warning: mysql_fetch_array()")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_sqli(page, timeout=5)) == 1

    def test_detecta_unclosed_quotation(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        resp = _mock_response(text="unclosed quotation mark after 'test'")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_sqli(page, timeout=5)) == 1

    def test_detecta_sqlite_error(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        resp = _mock_response(text="sqlite error: near 'DROP': syntax error")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_sqli(page, timeout=5)) == 1

    def test_detecta_postgresql_query_failed(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        resp = _mock_response(text="postgresql query failed: ERROR")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_sqli(page, timeout=5)) == 1

    def test_detecta_sqlstate(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        resp = _mock_response(text="sqlstate[HY000]: General error")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_sqli(page, timeout=5)) == 1

    def test_no_reporta_si_error_ya_en_baseline(self):
        error = "you have an error in your sql syntax"
        page = _page(url="http://example.com/item?id=1", text=error)
        resp = _mock_response(text=error)
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert check_sqli(page, timeout=5) == []

    def test_sin_parametros_retorna_vacio(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_sqli(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()

    def test_request_exception_no_rompe(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        with patch.object(req_lib.Session, "get", side_effect=req_lib.RequestException("err")):
            assert check_sqli(page, timeout=5) == []

    def test_finding_tiene_nombre_de_parametro(self):
        page = _page(url="http://x.com/?id=1", text="clean")
        resp = _mock_response(text="you have an error in your sql syntax")
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_sqli(page, timeout=5)
        assert findings[0]["parameter"] == "id"


# ── check_open_redirect() ────────────────────────────────────────────────────

class TestCheckOpenRedirect:
    def test_detecta_redireccion_a_next_externo(self):
        page = _page(url="http://example.com/go?next=/home")
        resp = _mock_response(status=302, headers={"location": "https://example.com/malicious"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_open_redirect(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "open_redirect"
        assert findings[0]["severity"] == "medium"

    def test_detecta_redireccion_302(self):
        page = _page(url="http://x.com/?redirect=http://x.com")
        resp = _mock_response(status=302, headers={"location": "https://example.com/ok"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_open_redirect(page, timeout=5)
        assert len(findings) == 1

    def test_detecta_redireccion_301(self):
        page = _page(url="http://x.com/?url=http://x.com")
        resp = _mock_response(status=301, headers={"location": "https://example.com/ok"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_open_redirect(page, timeout=5)
        assert len(findings) == 1

    def test_detecta_redireccion_303(self):
        page = _page(url="http://x.com/?return=http://x.com")
        resp = _mock_response(status=303, headers={"location": "https://example.com/ok"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_open_redirect(page, timeout=5)) == 1

    def test_detecta_redireccion_307(self):
        page = _page(url="http://x.com/?dest=http://x.com")
        resp = _mock_response(status=307, headers={"location": "https://example.com/ok"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_open_redirect(page, timeout=5)) == 1

    def test_detecta_redireccion_308(self):
        page = _page(url="http://x.com/?next=http://x.com")
        resp = _mock_response(status=308, headers={"location": "https://example.com/ok"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_open_redirect(page, timeout=5)) == 1

    def test_no_reporta_200(self):
        page = _page(url="http://x.com/?next=http://x.com")
        resp = _mock_response(status=200, headers={"location": "https://example.com"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert check_open_redirect(page, timeout=5) == []

    def test_ignora_parametros_no_en_lista(self):
        page = _page(url="http://example.com/item?id=1")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_open_redirect(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()

    def test_sin_parametros_retorna_vacio(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            assert check_open_redirect(page, timeout=5) == []
        mock_get.assert_not_called()

    def test_location_debe_iniciar_con_payload(self):
        page = _page(url="http://x.com/?next=http://x.com")
        # Location empieza con algo diferente al payload
        resp = _mock_response(status=302, headers={"location": "/relative/path"})
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert check_open_redirect(page, timeout=5) == []


# ── check_lfi() ───────────────────────────────────────────────────────────────

class TestCheckLfi:
    def test_detecta_root_x_0_0(self):
        page = _page(url="http://example.com/view?file=readme.txt")
        resp = _mock_response(text="root:x:0:0:root:/root:/bin/bash")
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_lfi(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "lfi"
        assert findings[0]["severity"] == "critical"
        assert "CWE-22" in findings[0]["description"]

    def test_detecta_root_exclamacion(self):
        page = _page(url="http://x.com/?file=x")
        resp = _mock_response(text="root:!:18000:0:99999:7:::")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_lfi(page, timeout=5)) == 1

    def test_detecta_daemon_colon(self):
        page = _page(url="http://x.com/?file=x")
        resp = _mock_response(text="daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_lfi(page, timeout=5)) == 1

    def test_detecta_bin_bash(self):
        page = _page(url="http://x.com/?file=x")
        resp = _mock_response(text="nobody:x:65534:65534::/nonexistent:/bin/bash")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_lfi(page, timeout=5)) == 1

    def test_retorna_vacio_sin_indicador(self):
        page = _page(url="http://x.com/?file=x")
        resp = _mock_response(text="<html>normal page</html>")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert check_lfi(page, timeout=5) == []

    def test_sin_parametros_retorna_vacio(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            assert check_lfi(page, timeout=5) == []
        mock_get.assert_not_called()

    def test_request_exception_no_rompe(self):
        page = _page(url="http://x.com/?file=x")
        with patch.object(req_lib.Session, "get", side_effect=req_lib.RequestException("err")):
            assert check_lfi(page, timeout=5) == []

    def test_retorna_maximo_un_finding(self):
        page = _page(url="http://x.com/?file=x")
        resp = _mock_response(text="root:x:0:0")
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_lfi(page, timeout=5)
        assert len(findings) == 1


# ── check_command_injection() ────────────────────────────────────────────────

class TestCheckCommandInjection:
    def test_detecta_uid_igual(self):
        page = _page(url="http://example.com/ping?host=localhost")
        resp = _mock_response(text="uid=33(www-data) gid=33(www-data)")
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_command_injection(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "command_injection"
        assert findings[0]["severity"] == "critical"
        assert "CWE-78" in findings[0]["description"]

    def test_detecta_gid_igual(self):
        page = _page(url="http://x.com/?cmd=x")
        resp = _mock_response(text="gid=0(root)")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_command_injection(page, timeout=5)) == 1

    def test_detecta_www_data(self):
        page = _page(url="http://x.com/?cmd=x")
        resp = _mock_response(text="user is www-data")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_command_injection(page, timeout=5)) == 1

    def test_detecta_root_x_0_0(self):
        page = _page(url="http://x.com/?cmd=x")
        resp = _mock_response(text="root:x:0:0:root")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_command_injection(page, timeout=5)) == 1

    def test_retorna_vacio_sin_indicador(self):
        page = _page(url="http://x.com/?cmd=x")
        resp = _mock_response(text="<html>normal</html>")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert check_command_injection(page, timeout=5) == []

    def test_sin_parametros_retorna_vacio(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            assert check_command_injection(page, timeout=5) == []
        mock_get.assert_not_called()

    def test_request_exception_no_rompe(self):
        page = _page(url="http://x.com/?cmd=x")
        with patch.object(req_lib.Session, "get", side_effect=req_lib.RequestException("err")):
            assert check_command_injection(page, timeout=5) == []

    def test_retorna_maximo_un_finding(self):
        page = _page(url="http://x.com/?cmd=x")
        resp = _mock_response(text="uid=0(root)")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_command_injection(page, timeout=5)) == 1


# ── check_ssrf() ─────────────────────────────────────────────────────────────

class TestCheckSsrf:
    def test_detecta_ami_id(self):
        page = _page(url="http://example.com/fetch?url=http://placeholder")
        resp = _mock_response(text='ami-id: ami-0123456789abcdef0')
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_ssrf(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "ssrf"
        assert findings[0]["severity"] == "critical"
        assert "CWE-918" in findings[0]["description"]

    def test_detecta_instance_id(self):
        page = _page(url="http://x.com/?url=http://x.com")
        resp = _mock_response(text='{"instance-id": "i-0123456789"}')
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_ssrf(page, timeout=5)) == 1

    def test_detecta_iam_security_credentials(self):
        page = _page(url="http://x.com/?proxy=http://x.com")
        resp = _mock_response(text='iam/security-credentials/role')
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_ssrf(page, timeout=5)) == 1

    def test_probe_con_param_src(self):
        page = _page(url="http://x.com/?src=http://x.com")
        resp = _mock_response(text='ami-id: ami-abc')
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_ssrf(page, timeout=5)) == 1

    def test_probe_con_param_host(self):
        page = _page(url="http://x.com/?host=http://x.com")
        resp = _mock_response(text='instance-id: i-abc')
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert len(check_ssrf(page, timeout=5)) == 1

    def test_retorna_vacio_sin_indicador(self):
        page = _page(url="http://x.com/?url=http://x.com")
        resp = _mock_response(text="<html>normal</html>")
        with patch.object(req_lib.Session, "get", return_value=resp):
            assert check_ssrf(page, timeout=5) == []

    def test_ignora_params_no_en_lista(self):
        page = _page(url="http://x.com/?id=1&name=foo")
        with patch.object(req_lib.Session, "get") as mock_get:
            assert check_ssrf(page, timeout=5) == []
        mock_get.assert_not_called()

    def test_sin_parametros_retorna_vacio(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            assert check_ssrf(page, timeout=5) == []
        mock_get.assert_not_called()

    def test_request_exception_no_rompe(self):
        page = _page(url="http://x.com/?url=x")
        with patch.object(req_lib.Session, "get", side_effect=req_lib.RequestException("err")):
            assert check_ssrf(page, timeout=5) == []

    def test_evidencia_contiene_url_interna(self):
        page = _page(url="http://x.com/?url=http://x.com")
        resp = _mock_response(text="ami-id: ami-abc")
        with patch.object(req_lib.Session, "get", return_value=resp):
            findings = check_ssrf(page, timeout=5)
        assert "169.254.169.254" in findings[0]["evidence"]


# ── check_http_methods() ─────────────────────────────────────────────────────

class TestCheckHttpMethods:
    def test_detecta_put(self):
        resp = _mock_response(headers={"allow": "GET, POST, PUT"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert any("PUT" in f["evidence"] for f in findings)

    def test_detecta_delete(self):
        resp = _mock_response(headers={"allow": "GET, DELETE"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert any("DELETE" in f["evidence"] for f in findings)

    def test_detecta_trace(self):
        resp = _mock_response(headers={"allow": "GET, TRACE"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert len(findings) == 1
        assert "TRACE" in findings[0]["evidence"]

    def test_detecta_connect(self):
        resp = _mock_response(headers={"allow": "GET, CONNECT"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert len(findings) == 1

    def test_no_reporta_metodos_seguros(self):
        resp = _mock_response(headers={"allow": "GET, POST, HEAD, OPTIONS"})
        with patch("app.scanner.requests.options", return_value=resp):
            assert check_http_methods("http://example.com", timeout=5) == []

    def test_exception_retorna_vacio(self):
        with patch("app.scanner.requests.options", side_effect=req_lib.RequestException("err")):
            assert check_http_methods("http://example.com", timeout=5) == []

    def test_severity_es_medium(self):
        resp = _mock_response(headers={"allow": "TRACE"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert findings[0]["severity"] == "medium"

    def test_modulo_es_http_methods(self):
        resp = _mock_response(headers={"allow": "PUT"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert findings[0]["module"] == "http_methods"

    def test_usa_access_control_allow_methods(self):
        resp = _mock_response(headers={"allow": "GET", "access-control-allow-methods": "PUT"})
        with patch("app.scanner.requests.options", return_value=resp):
            findings = check_http_methods("http://example.com", timeout=5)
        assert len(findings) == 1


# ── check_error_disclosure() ─────────────────────────────────────────────────

class TestCheckErrorDisclosure:
    def test_detecta_traceback(self):
        resp = _mock_response(text="Traceback (most recent call last):\n  File app.py")
        with patch("app.scanner.requests.get", return_value=resp):
            findings = check_error_disclosure("http://example.com", timeout=5)
        assert len(findings) == 1
        assert "CWE-209" in findings[0]["description"]

    def test_detecta_stack_trace(self):
        resp = _mock_response(text="stack trace at line 42")
        with patch("app.scanner.requests.get", return_value=resp):
            assert len(check_error_disclosure("http://example.com", timeout=5)) == 1

    def test_detecta_fatal_error(self):
        resp = _mock_response(text="fatal error: Call to undefined function doSomething()")
        with patch("app.scanner.requests.get", return_value=resp):
            assert len(check_error_disclosure("http://example.com", timeout=5)) == 1

    def test_detecta_syntax_error(self):
        resp = _mock_response(text="syntax error near token 'DROP'")
        with patch("app.scanner.requests.get", return_value=resp):
            assert len(check_error_disclosure("http://example.com", timeout=5)) == 1

    def test_detecta_undefined_variable(self):
        resp = _mock_response(text="undefined variable: $foo at line 3")
        with patch("app.scanner.requests.get", return_value=resp):
            assert len(check_error_disclosure("http://example.com", timeout=5)) == 1

    def test_detecta_exception_in_thread(self):
        resp = _mock_response(text="exception in thread main java.lang.NullPointerException")
        with patch("app.scanner.requests.get", return_value=resp):
            assert len(check_error_disclosure("http://example.com", timeout=5)) == 1

    def test_sin_hallazgos_en_pagina_generica(self):
        resp = _mock_response(status=404, text="<html>Pagina no encontrada</html>")
        with patch("app.scanner.requests.get", return_value=resp):
            assert check_error_disclosure("http://example.com", timeout=5) == []

    def test_exception_retorna_vacio(self):
        with patch("app.scanner.requests.get", side_effect=req_lib.RequestException("err")):
            assert check_error_disclosure("http://example.com", timeout=5) == []

    def test_severity_es_medium(self):
        resp = _mock_response(text="traceback (most recent call last)")
        with patch("app.scanner.requests.get", return_value=resp):
            findings = check_error_disclosure("http://example.com", timeout=5)
        assert findings[0]["severity"] == "medium"

    def test_url_probe_es_ruta_inexistente(self):
        calls = []
        def fake_get(url, **kw):
            calls.append(url)
            return _mock_response(text="")
        with patch("app.scanner.requests.get", fake_get):
            check_error_disclosure("http://example.com", timeout=5)
        assert len(calls) == 1
        assert "inexistente" in calls[0] or "12345" in calls[0]


# ── probe_sensitive_files() ──────────────────────────────────────────────────

class TestProbeSensitiveFiles:
    def _make_session_get(self, match_url_substring, match_text):
        def fake_get(self_inner, url, **kw):
            if match_url_substring in url:
                return _mock_response(status=200, text=match_text)
            return _mock_response(status=404, text="")
        return fake_get

    def test_detecta_env_con_db_password(self):
        fake = self._make_session_get("/.env", "db_password=supersecret")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert any(".env" in f["title"].lower() for f in findings)

    def test_detecta_env_con_secret(self):
        fake = self._make_session_get("/.env", "secret=abc123")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert any(".env" in f["title"].lower() for f in findings)

    def test_detecta_env_con_app_key(self):
        fake = self._make_session_get("/.env", "app_key=base64:abc")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert any(".env" in f["title"].lower() for f in findings)

    def test_detecta_git_head_con_ref(self):
        fake = self._make_session_get("/.git/HEAD", "ref: refs/heads/main")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert any("git" in f["title"].lower() for f in findings)

    def test_no_detecta_env_sin_indicador(self):
        fake = self._make_session_get("/.env", "USER=alice\nHOME=/home/alice\nPATH=/usr/bin")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        env_f = [f for f in findings if ".env" in f["title"].lower()]
        assert len(env_f) == 0

    def test_no_detecta_cuando_404(self):
        with patch.object(req_lib.Session, "get", return_value=_mock_response(status=404)):
            assert probe_sensitive_files("http://example.com", timeout=5) == []

    def test_no_detecta_cuando_302(self):
        with patch.object(req_lib.Session, "get", return_value=_mock_response(status=302)):
            assert probe_sensitive_files("http://example.com", timeout=5) == []

    def test_env_severity_es_critical(self):
        fake = self._make_session_get("/.env", "db_password=secret")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        env_f = next(f for f in findings if ".env" in f["title"].lower())
        assert env_f["severity"] == "critical"

    def test_git_severity_es_critical(self):
        fake = self._make_session_get("/.git/HEAD", "ref: refs/heads/main")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        git_f = next(f for f in findings if "git" in f["title"].lower())
        assert git_f["severity"] == "critical"

    def test_modulo_es_info_disclosure(self):
        fake = self._make_session_get("/.env", "db_password=x")
        with patch.object(req_lib.Session, "get", fake):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert all(f["module"] == "info_disclosure" for f in findings)

    def test_request_exception_no_rompe(self):
        with patch.object(req_lib.Session, "get", side_effect=req_lib.RequestException("err")):
            assert probe_sensitive_files("http://example.com", timeout=5) == []
