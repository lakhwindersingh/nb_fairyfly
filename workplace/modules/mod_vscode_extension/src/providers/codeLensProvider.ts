import * as vscode from 'vscode';

export class PercipienceCodeLensProvider implements vscode.CodeLensProvider {
  provideCodeLenses(
    document: vscode.TextDocument,
    _token: vscode.CancellationToken
  ): vscode.CodeLens[] | Thenable<vscode.CodeLens[]> {
    const codeLenses: vscode.CodeLens[] = [];
    if (document.fileName.includes('.nb/context/contracts')) {
      const topOfFile = new vscode.Range(0, 0, 0, 0);
      codeLenses.push(
        new vscode.CodeLens(topOfFile, {
          title: '▶ Verify Invariant Schema',
          command: 'percipience.executeWorkflow'
        })
      );
    }
    return codeLenses;
  }
}
