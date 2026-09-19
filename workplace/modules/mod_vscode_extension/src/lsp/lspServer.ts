import {
  createConnection,
  TextDocuments,
  ProposedFeatures,
  InitializeParams,
  InitializeResult,
  TextDocumentSyncKind,
  CodeLens,
  Command
} from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';

const connection = createConnection(ProposedFeatures.all);
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

connection.onInitialize((_params: InitializeParams): InitializeResult => {
  return {
    capabilities: {
      textDocumentSync: TextDocumentSyncKind.Incremental,
      codeLensProvider: {
        resolveProvider: true
      },
      hoverProvider: true
    }
  };
});

connection.onCodeLens((params) => {
  const codeLenses: CodeLens[] = [];
  const doc = documents.get(params.textDocument.uri);
  if (doc && doc.uri.includes('.nb/context/contracts/')) {
    codeLenses.push({
      range: {
        start: { line: 0, character: 0 },
        end: { line: 0, character: 0 }
      },
      command: Command.create(
        '▶ Run Percipience Verification Workflow',
        'percipience.executeWorkflow'
      )
    });
  }
  return codeLenses;
});

documents.listen(connection);
connection.listen();
