# Percipience CLI Quickstart Guide

Get up and running with Percipience in less than 90 seconds.

## 1. Installation
```bash
npm install -g @neutronbinary/percipience
# or use the pre-compiled binary:
chmod +x workplace/bin/percipience
```

## 2. Bootstrapping Your Repository
To initialize your codebase into the Quad-Space architecture:
```bash
percipience init --mode multi_module --parent-plan .nb/percipience_parent.nbpack
```

## 3. Auditing State & Context Health
```bash
percipience audit --enforce-merkle-chain --min-maturity 0.85
```

## 4. Running Verification Gates on PRs
```bash
percipience gate
```
