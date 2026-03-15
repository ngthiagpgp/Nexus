# Nexus MVP

Nexus is a local-first operational workspace built on:

- DuckDB for structured state
- Markdown files for living documents
- Typer for local CLI operations
- FastAPI for the local API and cockpit

The current MVP already supports:

- workspace bootstrap with `nexus init`
- demo workspace seeding with `nexus demo-seed`
- local API + cockpit with `nexus serve`
- CLI/API/cockpit inspection for entities, documents, cycles, activities, relations, and audit trail
- controlled status updates for activities and documents
- document integrity verification and explicit reconciliation

## Install

```bash
python -m pip install -e .
```

Preferred command path when the console script is available:

```bash
nexus ...
```

Safe fallback that works even when `nexus` is not yet on `PATH`:

```bash
python -m nexus ...
```

## 5-minute quickstart

1. Create a fresh workspace:

```bash
python -m nexus init ./sandbox-workspace
cd ./sandbox-workspace
```

2. Seed a coherent demo dataset:

```bash
python -m nexus demo-seed
```

3. Start the local API and cockpit:

```bash
python -m nexus serve
```

4. Open the cockpit:

```text
http://127.0.0.1:3000/
```

5. Inspect the workspace from the CLI:

```bash
python -m nexus status
python -m nexus audit --limit 20
```

## Core local commands

```bash
python -m nexus init ./sandbox-workspace
python -m nexus demo-seed
python -m nexus serve
python -m nexus status
python -m nexus audit --limit 20
```

## Cockpit and API

- Cockpit: `http://127.0.0.1:3000/`
- Health: `http://127.0.0.1:3000/api/health`
- Workspace status: `http://127.0.0.1:3000/api/system/status`

## Human test guide

See [reports/TESTING_GUIDE.md](reports/TESTING_GUIDE.md) for the manual MVP validation script.
