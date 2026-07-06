import * as vscode from 'vscode';
import { ScannerViewProvider } from './viewProvider';
import {
    ensureApiKey,
    exportReportToFile,
    getApiUrl,
    getLastReport,
    provisionAccount,
    runScanPipeline,
    setLastReport,
    sortBySeverity
} from './scanCore';

const outputChannel = vscode.window.createOutputChannel('Web Vulnerability Scanner');

export function activate(context: vscode.ExtensionContext) {
    const viewProvider = new ScannerViewProvider(context);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('wvs.scannerView', viewProvider)
    );

    let configureCmd = vscode.commands.registerCommand('wvs.configure', async () => {
        const apiKey = await vscode.window.showInputBox({
            prompt: 'Introduce tu API Key del Web Vulnerability Scanner (avanzado)',
            password: true
        });
        if (apiKey) {
            await context.secrets.store('wvs.apiKey', apiKey);
            vscode.window.showInformationMessage('Listo.');
        }
    });

    let registerCmd = vscode.commands.registerCommand('wvs.registerAndConfigure', async () => {
        const apiUrl = getApiUrl();
        const key = await provisionAccount(context, apiUrl);
        if (key) {
            vscode.window.showInformationMessage('Cuenta lista. Ya puedes usar "WVS: Iniciar Escaneo".');
        }
    });

    let exportCmd = vscode.commands.registerCommand('wvs.exportReport', async () => {
        const report = getLastReport();
        if (!report) {
            vscode.window.showWarningMessage('Todavia no hay ningun reporte para exportar. Corre un escaneo primero.');
            return;
        }
        await exportReportToFile(report);
    });

    let scanCmd = vscode.commands.registerCommand('wvs.startScan', async () => {
        const apiUrl = getApiUrl();

        // La herramienta se configura sola la primera vez: si no hay cuenta,
        // se crea aqui mismo sin que el usuario tenga que saber que existe una API key.
        const apiKey = await ensureApiKey(context, apiUrl);
        if (!apiKey) return;

        const targetUrl = await vscode.window.showInputBox({
            prompt: 'Introduce la URL a escanear (ej. https://ejemplo.com)',
            placeHolder: 'https://ejemplo.com'
        });

        if (!targetUrl) return;

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `Escaneando ${targetUrl}...`,
            cancellable: false
        }, async (progress) => {
            try {
                const detail = await runScanPipeline(apiUrl, apiKey, targetUrl, (msg) => progress.report({ message: msg }));

                if (detail.status === 'failed') {
                    vscode.window.showErrorMessage(`Fallo el escaneo: ${detail.error_message}`);
                    return;
                }

                setLastReport({ targetUrl, detail });
                const vulns = sortBySeverity(detail.vulnerabilities || []);
                printReport(targetUrl, detail, vulns);

                if (vulns.length > 0) {
                    vscode.window.showWarningMessage(
                        `Escaneo finalizado: ${vulns.length} vulnerabilidad(es) en ${targetUrl} (riesgo ${detail.risk_score}/100). Ver panel "Web Vulnerability Scanner".`,
                        'Ver reporte',
                        'Exportar'
                    ).then(choice => {
                        if (choice === 'Ver reporte') {
                            outputChannel.show();
                        } else if (choice === 'Exportar') {
                            exportReportToFile({ targetUrl, detail });
                        }
                    });
                } else {
                    vscode.window.showInformationMessage(`Escaneo finalizado: sin vulnerabilidades en ${targetUrl}.`);
                }

            } catch (error: any) {
                vscode.window.showErrorMessage(`Error de conexion con la API: ${error.message}`);
            }
        });
    });

    context.subscriptions.push(configureCmd, registerCmd, exportCmd, scanCmd, outputChannel);
}

function printReport(targetUrl: string, detail: any, vulns: any[]) {
    outputChannel.clear();
    outputChannel.appendLine(`ESCANEO #${detail.id} - ${targetUrl}`);
    outputChannel.appendLine(`Puntuacion de riesgo: ${detail.risk_score}/100`);
    outputChannel.appendLine(`Hallazgos: ${vulns.length}`);
    outputChannel.appendLine('='.repeat(60));
    outputChannel.appendLine('');

    if (vulns.length === 0) {
        outputChannel.appendLine('No se encontraron vulnerabilidades.');
    } else {
        vulns.forEach((v, index) => {
            outputChannel.appendLine(`${index + 1}. [${String(v.severity).toUpperCase()}] ${v.title}`);
            outputChannel.appendLine(`   Modulo: ${v.module ?? 'n/d'}`);
            outputChannel.appendLine(`   Ubicacion: ${v.url ?? targetUrl}${v.parameter ? `  (parametro: ${v.parameter})` : ''}`);
            outputChannel.appendLine(`   Descripcion: ${v.description}`);
            if (v.evidence) {
                outputChannel.appendLine(`   Evidencia: ${v.evidence}`);
            }
            outputChannel.appendLine(`   Recomendacion: ${v.remediation}`);
            outputChannel.appendLine('');
        });
    }
    outputChannel.show(true);
}

export function deactivate() {}
