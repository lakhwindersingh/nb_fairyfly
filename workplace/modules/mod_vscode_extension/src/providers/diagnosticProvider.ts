import * as vscode from 'vscode';

export class ContractDiagnosticProvider {
  private diagnosticCollection: vscode.DiagnosticCollection;

  constructor() {
    this.diagnosticCollection = vscode.languages.createDiagnosticCollection('percipience-contracts');
  }

  public validateContract(document: vscode.TextDocument) {
    if (!document.fileName.includes('.nb/context/contracts')) {
      return;
    }

    const diagnostics: vscode.Diagnostic[] = [];
    const text = document.getText();
    if (!text.includes('contract_id') && !text.includes('$schema')) {
      const range = new vscode.Range(0, 0, 0, 10);
      const diagnostic = new vscode.Diagnostic(
        range,
        'Missing required contract_id or $schema definition in wire contract.',
        vscode.DiagnosticSeverity.Error
      );
      diagnostics.push(diagnostic);
    }
    this.diagnosticCollection.set(document.uri, diagnostics);
  }
}
