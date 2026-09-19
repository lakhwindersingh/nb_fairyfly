const esbuild = require('esbuild');

const isProduction = process.argv.includes('--production');

esbuild.build({
  entryPoints: ['./src/extension.ts'],
  bundle: true,
  outfile: './dist/extension.js',
  external: ['vscode'],
  format: 'cjs',
  platform: 'node',
  minify: isProduction,
  sourcemap: !isProduction,
}).catch(() => process.exit(1));
