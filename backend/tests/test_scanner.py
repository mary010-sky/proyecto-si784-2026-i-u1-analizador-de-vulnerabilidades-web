"""
Pruebas unitarias para app/scanner.py -- el motor real desplegado en produccion
(el que usan la Skill, la extension VS Code, el bot de Telegram y el agente de Copilot).
Todas las funciones se prueban con requests simulados -- sin internet.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

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
)


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


# ── build_vulnerability() ───────────────────────────────────────────────────

class TestBuildVulnerability:
    def test_campos_obligatorios(self):
        v = build_vulnerability("sqli", "high", "SQL Injection", "desc", None, "arreglalo", "http://x.com")
        assert v["module"] == "sqli"
        assert v["severity"] == "high"
        assert v["title"] == "SQL Injection"
        assert v["url"] == "http://x.com"

    def test_parametro_por_defecto_es_none(self):
        v = build_vulnerability("csrf", "medium", "T", "d", None, "sol", "http://x.com")
        assert v["parameter"] is None

    def test_parametro_explicito(self):
        v = build_vulnerability("xss", "high", "T", "d", "payload", "sol", "http://x.com", "q")
        assert v["parameter"] == "q"
        assert v["evidence"] == "payload"


# ── normalize_url() / same_origin() ─────────────────────────────────────────

class TestNormalizeUrl:
    def test_normaliza_url_valida(self):
        assert normalize_url("https://example.com") == "https://example.com/"

    def test_rechaza_esquema_invalido(self):
        with pytest.raises(ValueError):
            normalize_url("ftp://example.com")

    def test_rechaza_sin_host(self):
        with pytest.raises(ValueError):
            normalize_url("https://")


class TestSameOrigin:
    def test_mismo_dominio(self):
        assert same_origin("https://example.com/a", "https://example.com/b") is True

    def test_distinto_dominio(self):
        assert same_origin("https://example.com", "https://evil.com") is False


# ── replace_param() ──────────────────────────────────────────────────────────

class TestReplaceParam:
    def test_reemplaza_parametro_existente(self):
        url = "http://example.com/search?q=hello&page=1"
        result = replace_param(url, "q", "PAYLOAD")
        assert "q=PAYLOAD" in result
        assert "page=1" in result

    def test_mantiene_esquema_y_host(self):
        url = "https://mysite.com/path?x=1"
        result = replace_param(url, "x", "test")
        assert result.startswith("https://mysite.com/path")


# ── check_headers() ──────────────────────────────────────────────────────────

class TestCheckHeaders:
    def test_detecta_csp_faltante(self):
        titles = [f["title"] for f in check_headers(_page(headers={}))]
        assert any("Content-Security-Policy" in t for t in titles)

    def test_detecta_xframe_faltante(self):
        titles = [f["title"] for f in check_headers(_page(headers={}))]
        assert any("X-Frame-Options" in t for t in titles)

    def test_detecta_hsts_faltante_en_https(self):
        page = _page(url="https://example.com/", headers={})
        titles = [f["title"] for f in check_headers(page)]
        assert any("Strict-Transport-Security" in t for t in titles)

    def test_hsts_no_aplica_en_http(self):
        headers = {
            "content-security-policy": "x", "x-frame-options": "DENY",
            "x-content-type-options": "nosniff", "referrer-policy": "x", "permissions-policy": "x",
        }
        page = _page(url="http://example.com/", headers=headers)
        titles = [f["title"] for f in check_headers(page)]
        assert not any("Strict-Transport-Security" in t for t in titles)

    def test_no_falso_positivo_con_headers_completos(self):
        headers = {
            "x-frame-options": "DENY",
            "content-security-policy": "default-src 'self'",
            "strict-transport-security": "max-age=31536000",
            "x-content-type-options": "nosniff",
            "referrer-policy": "strict-origin-when-cross-origin",
            "permissions-policy": "camera=()",
        }
        page = _page(url="https://example.com/", headers=headers)
        assert check_headers(page) == []


# ── check_info_disclosure() ──────────────────────────────────────────────────

class TestCheckInfoDisclosure:
    def test_detecta_server_header(self):
        findings = check_info_disclosure(_page(headers={"server": "nginx/1.18.0"}))
        assert any("Server" in f["title"] for f in findings)

    def test_detecta_x_powered_by(self):
        findings = check_info_disclosure(_page(headers={"x-powered-by": "PHP/8.1.0"}))
        assert any("X-Powered-By" in f["title"] for f in findings)

    def test_detecta_traceback_en_body(self):
        page = _page(text="Traceback (most recent call last): ...")
        findings = check_info_disclosure(page)
        assert any("tecnico" in f["title"].lower() for f in findings)

    def test_sin_hallazgos_en_respuesta_limpia(self):
        assert check_info_disclosure(_page(headers={}, text="<html>todo bien</html>")) == []


# ── check_csrf() ──────────────────────────────────────────────────────────────

class TestCheckCsrf:
    def test_detecta_form_post_sin_token(self):
        html = "<form method='post' action='/login'><input name='user'></form>"
        findings = check_csrf(_page(text=html))
        assert len(findings) == 1
        assert findings[0]["module"] == "csrf"

    def test_no_reporta_form_con_token(self):
        html = "<form method='post'><input type='hidden' name='csrf_token' value='abc'></form>"
        assert check_csrf(_page(text=html)) == []

    def test_ignora_forms_get(self):
        html = "<form method='get' action='/search'><input name='q'></form>"
        assert check_csrf(_page(text=html)) == []


# ── check_reflected_xss() ─────────────────────────────────────────────────────

class TestCheckReflectedXss:
    def test_detecta_reflejo_de_payload(self):
        page = _page(url="http://example.com/search?q=hello")
        response = _mock_response(text="...<script>alert(1337)</script>...")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_reflected_xss(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "xss"
        assert findings[0]["parameter"] == "q"

    def test_sin_parametros_no_prueba_nada(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_reflected_xss(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()

    def test_no_reporta_si_no_hay_reflejo(self):
        page = _page(url="http://example.com/search?q=hello")
        response = _mock_response(text="<html>pagina normal</html>")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_reflected_xss(page, timeout=5)
        assert findings == []


# ── check_sqli() ───────────────────────────────────────────────────────────────

class TestCheckSqli:
    def test_detecta_error_sql(self):
        page = _page(url="http://example.com/item?id=1", text="pagina normal")
        response = _mock_response(text="you have an error in your sql syntax near ...")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_sqli(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "sqli"

    def test_no_reporta_si_error_ya_estaba_en_baseline(self):
        page = _page(url="http://example.com/item?id=1", text="you have an error in your sql syntax")
        response = _mock_response(text="you have an error in your sql syntax")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_sqli(page, timeout=5)
        assert findings == []


# ── check_open_redirect() ───────────────────────────────────────────────────

class TestCheckOpenRedirect:
    def test_detecta_redireccion_externa(self):
        page = _page(url="http://example.com/go?next=/home")
        response = _mock_response(status=302, headers={"location": "https://example.com/evil"})
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_open_redirect(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "open_redirect"

    def test_ignora_parametros_no_relacionados(self):
        page = _page(url="http://example.com/item?id=1")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_open_redirect(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()


# ── check_lfi() ─────────────────────────────────────────────────────────────

class TestCheckLfi:
    def test_detecta_path_traversal(self):
        page = _page(url="http://example.com/view?file=readme.txt")
        response = _mock_response(text="root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1::/usr/sbin:/nologin")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_lfi(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "lfi"
        assert "CWE-22" in findings[0]["description"]

    def test_sin_parametros_no_prueba_nada(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_lfi(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()


# ── check_command_injection() ────────────────────────────────────────────────

class TestCheckCommandInjection:
    def test_detecta_ejecucion_de_comandos(self):
        page = _page(url="http://example.com/ping?host=localhost")
        response = _mock_response(text="uid=33(www-data) gid=33(www-data) groups=33(www-data)")
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_command_injection(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "command_injection"
        assert "CWE-78" in findings[0]["description"]

    def test_sin_parametros_no_prueba_nada(self):
        page = _page(url="http://example.com/")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_command_injection(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()


# ── check_ssrf() ──────────────────────────────────────────────────────────────

class TestCheckSsrf:
    def test_detecta_acceso_a_metadata_interna(self):
        page = _page(url="http://example.com/fetch?url=http://placeholder")
        response = _mock_response(text='{"instance-id": "i-0123456789"}')
        with patch.object(req_lib.Session, "get", return_value=response):
            findings = check_ssrf(page, timeout=5)
        assert len(findings) == 1
        assert findings[0]["module"] == "ssrf"

    def test_ignora_parametros_no_relacionados(self):
        page = _page(url="http://example.com/item?id=1")
        with patch.object(req_lib.Session, "get") as mock_get:
            findings = check_ssrf(page, timeout=5)
        assert findings == []
        mock_get.assert_not_called()


# ── check_http_methods() ─────────────────────────────────────────────────────

class TestCheckHttpMethods:
    def test_detecta_metodos_peligrosos(self):
        response = _mock_response(headers={"allow": "GET, POST, PUT, DELETE"})
        with patch("app.scanner.requests.options", return_value=response):
            findings = check_http_methods("http://example.com", timeout=5)
        assert len(findings) == 1
        assert "PUT" in findings[0]["evidence"]
        assert "DELETE" in findings[0]["evidence"]

    def test_no_reporta_metodos_seguros(self):
        response = _mock_response(headers={"allow": "GET, POST, HEAD, OPTIONS"})
        with patch("app.scanner.requests.options", return_value=response):
            findings = check_http_methods("http://example.com", timeout=5)
        assert findings == []


# ── check_error_disclosure() ─────────────────────────────────────────────────

class TestCheckErrorDisclosure:
    def test_detecta_traceback_en_pagina_de_error(self):
        response = _mock_response(text="Traceback (most recent call last): archivo x, linea 1")
        with patch("app.scanner.requests.get", return_value=response):
            findings = check_error_disclosure("http://example.com", timeout=5)
        assert len(findings) == 1
        assert "CWE-209" in findings[0]["description"]

    def test_sin_hallazgos_en_pagina_generica_de_error(self):
        response = _mock_response(status=404, text="<html>Pagina no encontrada</html>")
        with patch("app.scanner.requests.get", return_value=response):
            findings = check_error_disclosure("http://example.com", timeout=5)
        assert findings == []


# ── probe_sensitive_files() ──────────────────────────────────────────────────

class TestProbeSensitiveFiles:
    def test_detecta_env_expuesto(self):
        def fake_get(self, url, **kwargs):
            if url.endswith("/.env"):
                return _mock_response(status=200, text="DB_PASSWORD=secret\nAPP_KEY=abc")
            return _mock_response(status=404, text="")

        with patch.object(req_lib.Session, "get", fake_get):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert any(".env" in f["title"] for f in findings)

    def test_sin_archivos_expuestos(self):
        with patch.object(req_lib.Session, "get", return_value=_mock_response(status=404)):
            findings = probe_sensitive_files("http://example.com", timeout=5)
        assert findings == []


# ── calculate_risk_score() ───────────────────────────────────────────────────

class TestCalculateRiskScore:
    def test_suma_puntos_por_severidad(self):
        assert calculate_risk_score([{"severity": "critical"}, {"severity": "low"}]) == 45

    def test_tope_en_100(self):
        assert calculate_risk_score([{"severity": "critical"}] * 5) == 100

    def test_sin_hallazgos_es_cero(self):
        assert calculate_risk_score([]) == 0
