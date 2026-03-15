# Nexus MVP Testing Guide

## Purpose

This is the canonical human test script for the current local MVP.

It validates:

- installation
- workspace bootstrap
- demo seeding
- local serve flow
- cockpit access
- workspace status visibility
- audit trail visibility

## Preconditions

- Python 3.11+ available
- terminal opened at the repository root

## 1. Install

Run:

```bash
python -m pip install -e .
```

Expected:

- installation completes without dependency errors
- `nexus` command becomes available in the current environment

Failure signals:

- `No module named nexus`
- pip dependency resolution failure
- `nexus` not found after install

## 2. Initialize a fresh workspace

Run:

```bash
nexus init ./sandbox-workspace
cd ./sandbox-workspace
```

Expected:

- output includes `Nexus workspace ready`
- `nexus.duckdb` exists
- `.nexus/config.yaml` exists
- `documents/` exists

Failure signals:

- command exits non-zero
- database file is missing
- config file is missing

## 3. Seed demo data

Run:

```bash
nexus demo-seed
```

Expected:

- output includes `Demo seed ready` or `Demo seed already present`
- counts include at least:
  - `cycles 1`
  - `activities 3`
  - `entities 3`
  - `documents 3`

Failure signals:

- command exits non-zero
- counts are missing or obviously incomplete

## 4. Check workspace status

Run:

```bash
nexus status
```

Expected:

- output includes `Initialized: yes`
- output shows DB as present
- output shows counts for entities, documents, relations, cycles, and activities
- operational summary is visible

Failure signals:

- workspace reported as not initialized
- counts are all zero after demo seed
- missing path warnings for core workspace files

## 5. Inspect audit trail

Run:

```bash
nexus audit --limit 20
```

Expected:

- table header:
  `Timestamp | Action | Entity Type | Entity ID | Agent`
- recent `create` rows for seeded records

Failure signals:

- command exits non-zero
- no table output in a seeded workspace
- obvious missing audit rows after successful seed

## 6. Serve the local MVP

Run:

```bash
nexus serve
```

Expected:

- output includes:
  - `API: http://127.0.0.1:3000/api/health`
  - `Cockpit: http://127.0.0.1:3000/`
- process stays running until interrupted

Failure signals:

- command exits immediately with an error
- port bind failure
- workspace validation failure inside a valid workspace

## 7. Open the cockpit

Open:

```text
http://127.0.0.1:3000/
```

Expected:

- cockpit page loads
- workspace status is visible
- counts for entities, documents, relations, cycles, and activities are visible
- cycles, activities, documents, and audit panel all render data

Failure signals:

- blank page
- API errors rendered in the shell
- counts missing despite seeded workspace
- audit panel stays empty in a seeded workspace

## 8. Verify the local API directly

Open in browser or curl:

```text
http://127.0.0.1:3000/api/health
http://127.0.0.1:3000/api/system/status
http://127.0.0.1:3000/api/audit-log
```

Expected:

- `health` returns `status: ok`
- `system/status` returns `is_workspace: true`
- `audit-log` returns recent rows ordered newest first

Failure signals:

- non-200 responses
- workspace reported as false inside the seeded workspace
- audit endpoint returns empty data unexpectedly

## End state

The MVP is considered human-test ready when all steps above succeed without manual repair.
