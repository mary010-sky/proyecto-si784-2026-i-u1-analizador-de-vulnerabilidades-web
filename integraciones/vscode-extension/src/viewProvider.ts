import * as vscode from 'vscode';
import {
    ensureApiKey,
    exportReportToFile,
    fetchScanDetail,
    fetchScans,
    fetchStats,
    getApiUrl,
    getLastReport,
    runScanPipeline,
    setLastReport,
    ScanDetail
} from './scanCore';

export class ScannerViewProvider implements vscode.WebviewViewProvider {
    private view?: vscode.WebviewView;

    constructor(private readonly context: vscode.ExtensionContext) {}

    resolveWebviewView(webviewView: vscode.WebviewView): void {
        this.view = webviewView;
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = this.renderHtml();

        webviewView.webview.onDidReceiveMessage(async (message) => {
            if (message.type === 'scan') {
                await this.handleScan(message.url);
            } else if (message.type === 'export') {
                const report = getLastReport();
                if (!report) {
                    vscode.window.showWarningMessage('Todavia no hay ningun reporte para exportar.');
                    return;
                }
                await exportReportToFile(report);
            } else if (message.type === 'loadScan') {
                await this.handleLoadScan(message.scanId, message.targetUrl);
            } else if (message.type === 'refreshDashboard') {
                await this.loadDashboard();
            }
        });

        const existing = getLastReport();
        if (existing) {
            this.postResult(existing.targetUrl, existing.detail);
        }
        void this.loadDashboard();
    }

    private postStatus(message: string) {
        this.view?.webview.postMessage({ type: 'status', message });
    }

    private postError(message: string) {
        this.view?.webview.postMessage({ type: 'error', message });
    }

    private postResult(targetUrl: string, detail: ScanDetail) {
        this.view?.webview.postMessage({ type: 'result', targetUrl, detail });
    }

    private async loadDashboard() {
        const apiUrl = getApiUrl();
        const apiKey = await this.context.secrets.get('wvs.apiKey');
        if (!apiKey) {
            this.view?.webview.postMessage({ type: 'dashboard', stats: null, scans: [] });
            return;
        }
        try {
            const [stats, scans] = await Promise.all([
                fetchStats(apiUrl, apiKey),
                fetchScans(apiUrl, apiKey)
            ]);
            this.view?.webview.postMessage({ type: 'dashboard', stats, scans: scans.slice(0, 10) });
        } catch {
            // El dashboard es informativo: si falla, simplemente no se muestra.
        }
    }

    private async handleScan(targetUrl: string) {
        if (!targetUrl) return;
        const apiUrl = getApiUrl();

        this.postStatus('Verificando tu cuenta...');
        const apiKey = await ensureApiKey(this.context, apiUrl);
        if (!apiKey) {
            this.postStatus('');
            return;
        }

        try {
            this.postStatus(`Escaneando ${targetUrl}...`);
            const detail = await runScanPipeline(apiUrl, apiKey, targetUrl, (msg) => this.postStatus(msg));

            if (detail.status === 'failed') {
                this.postError(`El escaneo fallo: ${detail.error_message ?? 'error desconocido'}`);
                return;
            }

            setLastReport({ targetUrl, detail });
            this.postResult(targetUrl, detail);
            void this.loadDashboard();
        } catch (error: any) {
            this.postError(`Error de conexion con la API: ${error.message}`);
        }
    }

    private async handleLoadScan(scanId: number, targetUrl: string) {
        const apiUrl = getApiUrl();
        const apiKey = await this.context.secrets.get('wvs.apiKey');
        if (!apiKey) return;

        try {
            this.postStatus('Cargando escaneo anterior...');
            const detail = await fetchScanDetail(apiUrl, apiKey, scanId);
            this.postStatus('');
            setLastReport({ targetUrl, detail });
            this.postResult(targetUrl, detail);
        } catch (error: any) {
            this.postError(`No se pudo cargar el escaneo: ${error.message}`);
        }
    }

    private renderHtml(): string {
        return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
    body {
        font-family: var(--vscode-font-family);
        color: var(--vscode-foreground);
        padding: 0.5rem;
    }
    input {
        width: 100%;
        box-sizing: border-box;
        padding: 6px;
        margin-bottom: 6px;
        background: var(--vscode-input-background);
        color: var(--vscode-input-foreground);
        border: 1px solid var(--vscode-input-border, transparent);
        border-radius: 3px;
    }
    button {
        width: 100%;
        padding: 6px;
        margin-bottom: 4px;
        background: var(--vscode-button-background);
        color: var(--vscode-button-foreground);
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }
    button:hover { background: var(--vscode-button-hoverBackground); }
    button.secondary {
        background: var(--vscode-button-secondaryBackground);
        color: var(--vscode-button-secondaryForeground);
    }
    h3 { font-size: 11px; text-transform: uppercase; opacity: 0.7; margin: 14px 0 6px 0; }
    #status { margin: 8px 0; font-size: 12px; opacity: 0.85; min-height: 16px; }
    #error { color: var(--vscode-errorForeground); font-size: 12px; margin-bottom: 8px; }
    .summary { font-size: 12px; margin-bottom: 10px; }
    .card {
        border-left: 4px solid #8a8a8a;
        background: var(--vscode-editorWidget-background, rgba(127,127,127,0.08));
        padding: 8px 10px;
        border-radius: 4px;
        margin-bottom: 8px;
        font-size: 12px;
    }
    .card h4 { margin: 0 0 4px 0; font-size: 13px; }
    .card p { margin: 2px 0; }
    code {
        background: rgba(127,127,127,0.2);
        padding: 1px 4px;
        border-radius: 3px;
        word-break: break-all;
    }
    .stats-row { display: flex; gap: 6px; flex-wrap: wrap; font-size: 11px; margin-bottom: 6px; }
    .stat-chip {
        background: rgba(127,127,127,0.15);
        padding: 3px 8px;
        border-radius: 10px;
    }
    .sev-chip { color: #fff; font-weight: 600; }
    .history-item {
        display: flex;
        justify-content: space-between;
        gap: 6px;
        padding: 5px 6px;
        border-radius: 3px;
        font-size: 11px;
        cursor: pointer;
    }
    .history-item:hover { background: rgba(127,127,127,0.15); }
    .history-url { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
    .history-empty { font-size: 11px; opacity: 0.6; }
</style>
</head>
<body>
    <div id="dashboard">
        <div class="stats-row" id="statsRow"></div>
        <h3>Historial reciente</h3>
        <div id="history"><p class="history-empty">Aun no has corrido ningun escaneo.</p></div>
    </div>

    <h3>Nuevo escaneo</h3>
    <input id="url" type="text" placeholder="https://ejemplo.com" />
    <button id="scanBtn">Escanear</button>
    <button id="exportBtn" class="secondary">Exportar ultimo reporte</button>
    <div id="status"></div>
    <div id="error"></div>
    <div id="summary" class="summary"></div>
    <div id="results"></div>

<script>
    const vscode = acquireVsCodeApi();
    const urlInput = document.getElementById('url');
    const statusEl = document.getElementById('status');
    const errorEl = document.getElementById('error');
    const summaryEl = document.getElementById('summary');
    const resultsEl = document.getElementById('results');
    const statsRowEl = document.getElementById('statsRow');
    const historyEl = document.getElementById('history');

    const severityColors = { critical: '#f14c4c', high: '#e07a3f', medium: '#e5c33b', low: '#3794ff', info: '#8a8a8a' };
    const severityRank = { critical: 4, high: 3, medium: 2, low: 1, info: 0 };

    function escapeHtml(text) {
        return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    document.getElementById('scanBtn').addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (!url) return;
        errorEl.textContent = '';
        resultsEl.innerHTML = '';
        summaryEl.textContent = '';
        vscode.postMessage({ type: 'scan', url });
    });

    document.getElementById('exportBtn').addEventListener('click', () => {
        vscode.postMessage({ type: 'export' });
    });

    window.addEventListener('message', (event) => {
        const message = event.data;
        if (message.type === 'status') {
            statusEl.textContent = message.message;
        } else if (message.type === 'error') {
            statusEl.textContent = '';
            errorEl.textContent = message.message;
        } else if (message.type === 'result') {
            statusEl.textContent = '';
            errorEl.textContent = '';
            renderResult(message.targetUrl, message.detail);
        } else if (message.type === 'dashboard') {
            renderDashboard(message.stats, message.scans);
        }
    });

    function renderDashboard(stats, scans) {
        if (!stats) {
            statsRowEl.innerHTML = '';
        } else {
            let chips = '<span class="stat-chip">' + stats.total_scans + ' escaneos</span>' +
                '<span class="stat-chip">' + stats.total_vulnerabilities + ' vulnerabilidades</span>';
            if (stats.running_scans > 0) {
                chips += '<span class="stat-chip">' + stats.running_scans + ' en curso</span>';
            }
            for (const sev of ['critical', 'high', 'medium', 'low', 'info']) {
                const count = (stats.by_severity || {})[sev];
                if (count) {
                    chips += '<span class="stat-chip sev-chip" style="background:' + severityColors[sev] + '">' + sev + ': ' + count + '</span>';
                }
            }
            statsRowEl.innerHTML = chips;
        }

        if (!scans || scans.length === 0) {
            historyEl.innerHTML = '<p class="history-empty">Aun no has corrido ningun escaneo.</p>';
            return;
        }

        historyEl.innerHTML = scans.map((s) => {
            const color = s.vulnerability_count > 0 ? (severityColors['high']) : '#3fb950';
            return '<div class="history-item" data-id="' + s.id + '" data-url="' + escapeHtml(s.target_url) + '">' +
                '<span class="history-url">' + escapeHtml(s.target_url) + '</span>' +
                '<span style="color:' + color + '">' + s.vulnerability_count + '</span>' +
                '</div>';
        }).join('');

        historyEl.querySelectorAll('.history-item').forEach((el) => {
            el.addEventListener('click', () => {
                const id = parseInt(el.getAttribute('data-id'), 10);
                const targetUrl = el.getAttribute('data-url');
                errorEl.textContent = '';
                vscode.postMessage({ type: 'loadScan', scanId: id, targetUrl });
            });
        });
    }

    function renderResult(targetUrl, detail) {
        const vulns = (detail.vulnerabilities || []).slice().sort(
            (a, b) => (severityRank[b.severity] || 0) - (severityRank[a.severity] || 0)
        );
        summaryEl.innerHTML = '<strong>' + escapeHtml(targetUrl) + '</strong><br>' +
            'Riesgo: ' + detail.risk_score + '/100 — ' + vulns.length + ' hallazgo(s)';

        if (vulns.length === 0) {
            resultsEl.innerHTML = '<p>No se encontraron vulnerabilidades.</p>';
            return;
        }

        resultsEl.innerHTML = vulns.map((v, i) => {
            const color = severityColors[String(v.severity).toLowerCase()] || '#8a8a8a';
            let html = '<div class="card" style="border-left-color:' + color + '">';
            html += '<h4>' + (i + 1) + '. [' + escapeHtml(String(v.severity).toUpperCase()) + '] ' + escapeHtml(v.title) + '</h4>';
            html += '<p><strong>Modulo:</strong> ' + escapeHtml(v.module) + '</p>';
            html += '<p><strong>Ubicacion:</strong> ' + escapeHtml(v.url) + (v.parameter ? ' (param: <code>' + escapeHtml(v.parameter) + '</code>)' : '') + '</p>';
            html += '<p>' + escapeHtml(v.description) + '</p>';
            if (v.evidence) {
                html += '<p><strong>Evidencia:</strong> <code>' + escapeHtml(v.evidence) + '</code></p>';
            }
            html += '<p><strong>Recomendacion:</strong> ' + escapeHtml(v.remediation) + '</p>';
            html += '</div>';
            return html;
        }).join('');
    }
</script>
</body>
</html>`;
    }
}
