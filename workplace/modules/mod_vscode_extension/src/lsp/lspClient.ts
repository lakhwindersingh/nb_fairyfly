import * as path from 'path';
import { ExtensionContext, workspace } from 'vscode';
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
  TransportKind
} from 'vscode-languageclient/node';

export class PercipienceLspClient {
  private client: LanguageClient | undefined;

  constructor(private context: ExtensionContext) {}

  public start() {
    const serverModule = this.context.asAbsolutePath(
      path.join('out', 'lsp', 'lspServer.js')
    );

    const serverOptions: ServerOptions = {
      run: { module: serverModule, transport: TransportKind.ipc },
      debug: { module: serverModule, transport: TransportKind.ipc }
    };

    const clientOptions: LanguageClientOptions = {
      documentSelector: [
        { scheme: 'file', language: 'yaml' },
        { scheme: 'file', language: 'json' }
      ],
      synchronize: {
        fileEvents: workspace.createFileSystemWatcher('**/.nb/**/*.{yaml,json}')
      }
    };

    this.client = new LanguageClient(
      'percipienceLanguageServer',
      'Percipience Language Server',
      serverOptions,
      clientOptions
    );

    this.client.start();
  }

  public stop(): Thenable<void> | undefined {
    if (!this.client) {
      return undefined;
    }
    return this.client.stop();
  }
}
