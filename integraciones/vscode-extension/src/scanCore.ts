import * as vscode from 'vscode';
import * as http from 'http';
import * as https from 'https';

export interface Vulnerability {
    module: string;
    severity: string;
    title: string;
    description: string;
    evidence: string | null;
    remediation: string;
    url: string;
    parameter: string | null;
}

export interface ScanDetail {
    id: number;
    status: string;
    risk_score: number;
    error_message?: string | null;
    vulnerabilities?: Vulnerability[];
}

export interface LastReport {
    targetUrl: string;
    detail: ScanDetail;
}

export interface ScanSummary {
    id: number;
    target_url: string;
    status: string;
    risk_score: number;
    vulnerability_count: number;
    created_at: string;
}

export interface Stats {
    total_scans: number;
    completed_scans: number;
    running_scans: number;
    total_vulnerabilities: number;
    by_severity: Record<string, number>;
    by_module: Record<string, number>;
}

let lastReport: LastReport | undefined;

export function setLastReport(report: LastReport): void {
    lastReport = report;
}

export function getLastReport(): LastReport | undefined {
    return lastReport;
}

export function getApiUrl(): string {
    const config = vscode.workspace.getConfiguration('wvs');
    return config.get<string>('apiUrl', 'https://vulnerabilidad-web.sytes.net/backend');
}

export function severityRank(severity: string): number {
    const order: Record<string, number> = { critical: 4, high: 3, medium: 2, low: 1, info: 0 };
    return order[String(severity).toLowerCase()] ?? 0;
}

export function severityColor(severity: string): string {
    const colors: Record<string, string> = {
        critical: '#f14c4c',
        high: '#e07a3f',
        medium: '#e5c33b',
        low: '#3794ff',
        info: '#8a8a8a'
    };
    return colors[String(severity).toLowerCase()] ?? '#8a8a8a';
}

export function sortBySeverity(vulns: Vulnerability[]): Vulnerability[] {
    return [...vulns].sort((a, b) => severityRank(b.severity) - severityRank(a.severity));
}

/**
 * Crea (o inicia sesion en) la cuenta y guarda la credencial resultante, sin exponer
 * el concepto de "API key" al usuario: solo pide correo y contrasena.
 */
export async function provisionAccount(context: vscode.ExtensionContext, apiUrl: string): Promise<string | undefined> {
    const email = await vscode.window.showInputBox({
        title: 'Configura tu cuenta de Web Vulnerability Scanner (una sola vez)',
        prompt: 'Correo electronico',
        placeHolder: 'tucorreo@ejemplo.com',
        validateInput: (v) => (v.includes('@') ? null : 'Correo invalido')
    });
    if (!email) return undefined;

    const defaultUsername = email.split('@')[0].padEnd(2, '_');
    const username = await vscode.window.showInputBox({
        prompt: 'Nombre de usuario',
        value: defaultUsername
    });
    if (!username) return undefined;

    const password = await vscode.window.showInputBox({
        prompt: 'Contrasena (minimo 8 caracteres). Si ya tienes cuenta, escribe la misma para iniciar sesion.',
        password: true,
        validateInput: (v) => (v.length >= 8 ? null : 'Minimo 8 caracteres')
    });
    if (!password) return undefined;

    return vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Configurando tu cuenta...',
        cancellable: false
    }, async () => {
        try {
            let token: string;
            try {
                const registerRes = await registerUser(apiUrl, email, username, password);
                token = registerRes.access_token;
            } catch (err: any) {
                if (String(err.message).includes('HTTP 409')) {
                    const loginRes = await loginUser(apiUrl, email, password);
                    token = loginRes.access_token;
                } else {
                    throw err;
                }
            }

            const apiKeyRes = await createApiKey(apiUrl, token, `vscode-${username}`);
            await context.secrets.store('wvs.apiKey', apiKeyRes.api_key);
            return apiKeyRes.api_key as string;
        } catch (error: any) {
            vscode.window.showErrorMessage(`No se pudo configurar la cuenta: ${error.message}`);
            return undefined;
        }
    });
}

export async function ensureApiKey(context: vscode.ExtensionContext, apiUrl: string): Promise<string | undefined> {
    const existing = await context.secrets.get('wvs.apiKey');
    if (existing) return existing;
    return provisionAccount(context, apiUrl);
}

/**
 * Lanza un escaneo y hace polling hasta que termina. onProgress se llama con mensajes
 * de estado para que quien invoque pueda mostrarlos (notificacion, webview, etc.).
 */
export async function runScanPipeline(
    apiUrl: string,
    apiKey: string,
    targetUrl: string,
    onProgress?: (message: string) => void
): Promise<ScanDetail> {
    const scanId = await startScan(apiUrl, apiKey, targetUrl);
    onProgress?.('Escaneo iniciado, analizando...');

    let detail: ScanDetail;
    while (true) {
        await new Promise((resolve) => setTimeout(resolve, 3000));
        detail = await checkStatus(apiUrl, apiKey, scanId);
        if (detail.status === 'completed' || detail.status === 'failed') break;
    }
    return detail;
}

export function fetchStats(apiUrl: string, apiKey: string): Promise<Stats> {
    return makeRequest(`${apiUrl}/api/integrations/stats`, {
        method: 'GET',
        headers: { 'X-API-Key': apiKey }
    });
}

export function fetchScans(apiUrl: string, apiKey: string): Promise<ScanSummary[]> {
    return makeRequest(`${apiUrl}/api/integrations/scans`, {
        method: 'GET',
        headers: { 'X-API-Key': apiKey }
    });
}

export function fetchScanDetail(apiUrl: string, apiKey: string, scanId: number): Promise<ScanDetail> {
    return checkStatus(apiUrl, apiKey, scanId);
}

export function buildMarkdownReport(targetUrl: string, detail: ScanDetail): string {
    const vulns = sortBySeverity(detail.vulnerabilities || []);
    const lines = [
        `# Reporte de Web Vulnerability Scanner`,
        '',
        `- **Objetivo:** ${targetUrl}`,
        `- **Escaneo:** #${detail.id}`,
        `- **Puntuacion de riesgo:** ${detail.risk_score}/100`,
        `- **Hallazgos:** ${vulns.length}`,
        `- **Generado:** ${new Date().toISOString()}`,
        '',
        '---',
        ''
    ];

    if (vulns.length === 0) {
        lines.push('No se encontraron vulnerabilidades.');
    } else {
        vulns.forEach((v, index) => {
            lines.push(`## ${index + 1}. [${v.severity.toUpperCase()}] ${v.title}`);
            lines.push('');
            lines.push(`- **Modulo:** ${v.module}`);
            lines.push(`- **Ubicacion:** ${v.url}${v.parameter ? ` (parametro: \`${v.parameter}\`)` : ''}`);
            lines.push(`- **Descripcion:** ${v.description}`);
            if (v.evidence) {
                lines.push(`- **Evidencia:** \`${v.evidence}\``);
            }
            lines.push(`- **Recomendacion:** ${v.remediation}`);
            lines.push('');
        });
    }

    return lines.join('\n');
}

export function buildHtmlReport(targetUrl: string, detail: ScanDetail): string {
    const vulns = sortBySeverity(detail.vulnerabilities || []);
    const rows = vulns.map((v, index) => `
        <div class="card" style="border-left: 4px solid ${severityColor(v.severity)}">
            <h3>${index + 1}. [${escapeHtml(v.severity.toUpperCase())}] ${escapeHtml(v.title)}</h3>
            <p><strong>Modulo:</strong> ${escapeHtml(v.module)}</p>
            <p><strong>Ubicacion:</strong> ${escapeHtml(v.url)}${v.parameter ? ` (parametro: <code>${escapeHtml(v.parameter)}</code>)` : ''}</p>
            <p><strong>Descripcion:</strong> ${escapeHtml(v.description)}</p>
            ${v.evidence ? `<p><strong>Evidencia:</strong> <code>${escapeHtml(v.evidence)}</code></p>` : ''}
            <p><strong>Recomendacion:</strong> ${escapeHtml(v.remediation)}</p>
        </div>
    `).join('\n');

    return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reporte WVS - ${escapeHtml(targetUrl)}</title>
<style>
    body { font-family: system-ui, sans-serif; margin: 2rem; color: #1e1e1e; background: #fff; }
    h1 { margin-bottom: 0.2rem; }
    .meta { color: #555; margin-bottom: 1.5rem; }
    .card { background: #f7f7f7; padding: 1rem 1.2rem; border-radius: 6px; margin-bottom: 1rem; }
    code { background: #eee; padding: 1px 4px; border-radius: 3px; }
</style>
</head>
<body>
    <h1>Reporte de Web Vulnerability Scanner</h1>
    <p class="meta">
        Objetivo: <strong>${escapeHtml(targetUrl)}</strong><br>
        Escaneo #${detail.id} — Puntuacion de riesgo: <strong>${detail.risk_score}/100</strong> —
        ${vulns.length} hallazgo(s)<br>
        Generado: ${new Date().toLocaleString()}
    </p>
    ${vulns.length === 0 ? '<p>No se encontraron vulnerabilidades.</p>' : rows}
</body>
</html>`;
}

export function escapeHtml(text: string): string {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

export async function exportReportToFile(report: LastReport): Promise<void> {
    const format = await vscode.window.showQuickPick(
        [
            { label: 'Markdown (.md)', value: 'md' },
            { label: 'HTML (.html)', value: 'html' }
        ],
        { title: 'Formato del reporte a exportar' }
    );
    if (!format) return;

    const isMd = format.value === 'md';
    const content = isMd ? buildMarkdownReport(report.targetUrl, report.detail) : buildHtmlReport(report.targetUrl, report.detail);
    const safeHost = report.targetUrl.replace(/^https?:\/\//, '').replace(/[^a-zA-Z0-9.-]/g, '_');
    const defaultName = `wvs-reporte-${safeHost}-${report.detail.id}.${isMd ? 'md' : 'html'}`;

    const uri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file(defaultName),
        filters: isMd ? { Markdown: ['md'] } : { HTML: ['html'] }
    });
    if (!uri) return;

    await vscode.workspace.fs.writeFile(uri, Buffer.from(content, 'utf8'));
    const choice = await vscode.window.showInformationMessage(`Reporte guardado en ${uri.fsPath}`, 'Abrir');
    if (choice === 'Abrir') {
        if (isMd) {
            const doc = await vscode.workspace.openTextDocument(uri);
            await vscode.window.showTextDocument(doc);
        } else {
            await vscode.env.openExternal(uri);
        }
    }
}

function makeRequest(urlStr: string, options: http.RequestOptions, body?: any): Promise<any> {
    return new Promise((resolve, reject) => {
        const transport = urlStr.startsWith('https:') ? https : http;
        const req = transport.request(urlStr, options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(JSON.parse(data));
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                }
            });
        });
        req.on('error', reject);
        if (body) {
            req.write(JSON.stringify(body));
        }
        req.end();
    });
}

function makeFormRequest(urlStr: string, fields: Record<string, string>): Promise<any> {
    const bodyStr = Object.entries(fields)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&');
    return new Promise((resolve, reject) => {
        const transport = urlStr.startsWith('https:') ? https : http;
        const req = transport.request(urlStr, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': Buffer.byteLength(bodyStr)
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(JSON.parse(data));
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                }
            });
        });
        req.on('error', reject);
        req.write(bodyStr);
        req.end();
    });
}

function registerUser(apiUrl: string, email: string, username: string, password: string): Promise<any> {
    const options = { method: 'POST', headers: { 'Content-Type': 'application/json' } };
    return makeRequest(`${apiUrl}/api/auth/register`, options, { email, username, password });
}

function loginUser(apiUrl: string, email: string, password: string): Promise<any> {
    return makeFormRequest(`${apiUrl}/api/auth/login`, { username: email, password });
}

function createApiKey(apiUrl: string, token: string, name: string): Promise<any> {
    const options = {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
    };
    return makeRequest(`${apiUrl}/api/api-keys`, options, { name });
}

function startScan(apiUrl: string, apiKey: string, targetUrl: string): Promise<number> {
    const url = `${apiUrl}/api/integrations/scans`;
    const options = {
        method: 'POST',
        headers: {
            'X-API-Key': apiKey,
            'Content-Type': 'application/json'
        }
    };
    return makeRequest(url, options, { target_url: targetUrl, depth: 1 }).then(res => res.id);
}

function checkStatus(apiUrl: string, apiKey: string, scanId: number): Promise<ScanDetail> {
    const url = `${apiUrl}/api/integrations/scans/${scanId}`;
    const options = {
        method: 'GET',
        headers: { 'X-API-Key': apiKey }
    };
    return makeRequest(url, options);
}
