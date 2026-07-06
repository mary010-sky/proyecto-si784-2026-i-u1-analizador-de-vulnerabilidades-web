"""
Steps BDD para deteccion de vulnerabilidades (features/scanner.feature),
probando el motor real app/scanner.py.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests as req_lib
from pytest_bdd import given, scenarios, then, when

from app.scanner import (
    FetchedPage,
    build_vulnerability,
    check_csrf,
    check_headers,
    check_lfi,
    probe_sensitive_files,
    replace_param,
)

scenarios("../features/scanner.feature")


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


@pytest.fixture
def ctx():
    return {}


# ── GIVENs ────────────────────────────────────────────────────────────────

@given("una pagina sin cabeceras de seguridad configuradas")
def page_no_headers(ctx):
    ctx["page"] = _page(url="https://example.com/", headers={})


@given("una pagina con todas las cabeceras de seguridad configuradas")
def page_all_headers(ctx):
    ctx["page"] = _page(url="https://example.com/", headers={
        "x-frame-options": "DENY",
        "content-security-policy": "default-src 'self'",
        "strict-transport-security": "max-age=31536000",
        "x-content-type-options": "nosniff",
        "referrer-policy": "strict-origin-when-cross-origin",
        "permissions-policy": "camera=()",
    })


@given("una pagina con un formulario POST sin token CSRF")
def page_csrf_no_token(ctx):
    html = "<form method='post' action='/login'><input name='user'></form>"
    ctx["page"] = _page(text=html)


@given("una pagina con un formulario POST con token CSRF")
def page_csrf_with_token(ctx):
    html = "<form method='post'><input type='hidden' name='csrf_token' value='abc'></form>"
    ctx["page"] = _page(text=html)


@given("un parametro vulnerable a path traversal")
def lfi_param(ctx):
    ctx["page"] = _page(url="http://example.com/view?file=readme.txt")
    ctx["lfi_response"] = _mock_response(text="root:x:0:0:root:/root:/bin/bash")


@given("un sitio con el archivo .env accesible publicamente")
def site_env_exposed(ctx):
    def fake_get(self, url, **kwargs):
        if url.endswith("/.env"):
            return _mock_response(status=200, text="DB_PASSWORD=secret\nAPP_KEY=abc")
        return _mock_response(status=404, text="")
    ctx["fake_get"] = fake_get


@given("un hallazgo de tipo sqli con severidad high")
def finding_sqli(ctx):
    ctx["finding"] = build_vulnerability("sqli", "high", "SQL Injection detectado", "Desc", None, "sol", "http://x.com")


@given("una URL con parametros de consulta")
def url_with_params(ctx):
    ctx["url_param"] = "http://example.com/search?q=hello&page=1"


# ── WHENs ─────────────────────────────────────────────────────────────────

@when("analizo las cabeceras de la pagina")
def when_check_headers(ctx):
    ctx["findings"] = check_headers(ctx["page"])


@when("analizo el CSRF de la pagina")
def when_check_csrf(ctx):
    ctx["findings"] = check_csrf(ctx["page"])


@when("pruebo LFI sobre el parametro")
def when_check_lfi(ctx):
    with patch.object(req_lib.Session, "get", return_value=ctx["lfi_response"]):
        ctx["findings"] = check_lfi(ctx["page"], timeout=5)


@when("busco archivos sensibles expuestos")
def when_probe_sensitive_files(ctx):
    with patch.object(req_lib.Session, "get", ctx["fake_get"]):
        ctx["findings"] = probe_sensitive_files("http://example.com", timeout=5)


@when("verifico la estructura del hallazgo")
def when_verify_finding(ctx):
    pass  # el hallazgo ya esta en ctx["finding"]


@when("reemplazo el valor de un parametro")
def when_replace_param(ctx):
    ctx["result_url"] = replace_param(ctx["url_param"], "q", "PAYLOAD")


# ── THENs ─────────────────────────────────────────────────────────────────

@then("debo encontrar al menos una vulnerabilidad de cabecera faltante")
def then_has_header_vuln(ctx):
    assert len(ctx["findings"]) >= 1


@then("no debo encontrar vulnerabilidades de cabecera faltante")
def then_no_header_vuln(ctx):
    assert ctx["findings"] == []


@then("debo encontrar una vulnerabilidad de tipo csrf")
def then_csrf_vuln(ctx):
    found = [f for f in ctx["findings"] if f["module"] == "csrf"]
    assert len(found) >= 1


@then("no debo encontrar vulnerabilidades de csrf")
def then_no_csrf_vuln(ctx):
    assert ctx["findings"] == []


@then("debo encontrar una vulnerabilidad de tipo lfi")
def then_lfi_vuln(ctx):
    found = [f for f in ctx["findings"] if f["module"] == "lfi"]
    assert len(found) == 1


@then("debo encontrar una vulnerabilidad de archivo .env expuesto")
def then_env_vuln(ctx):
    assert any(".env" in f["title"] for f in ctx["findings"])


@then("el modulo del hallazgo debe ser sqli")
def then_type_sqli(ctx):
    assert ctx["finding"]["module"] == "sqli"


@then("la severidad debe ser high")
def then_severity_high(ctx):
    assert ctx["finding"]["severity"] == "high"


@then("el nuevo valor debe aparecer en la URL resultante")
def then_payload_in_url(ctx):
    assert "PAYLOAD" in ctx["result_url"]
