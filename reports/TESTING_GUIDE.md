# Nexus MVP Testing Guide

## Purpose

This is the canonical human test script for the current local MVP.

It validates:

- installation
- workspace bootstrap
- technical demo seeding
- rich demo seeding
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
- the local package installs successfully

Note:

- prefer `python -m nexus ...` for the human test flow
- `nexus ...` is still the preferred console-script form when it is already available on `PATH`

Failure signals:

- `No module named nexus`
- pip dependency resolution failure
- `nexus` not found after install

## 2. Initialize a fresh workspace

Run:

```bash
python -m nexus init ./sandbox-workspace
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

## 3. Seed technical demo data

Run:

```bash
python -m nexus demo-seed
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

Use this seed for:

- smoke checks
- regression checks
- low-noise validation

## 4. Seed rich demo data in a fresh workspace

Run this in a separate fresh workspace when you want the cockpit to feel operationally dense:

```bash
python -m nexus init ./sandbox-workspace-rich
cd ./sandbox-workspace-rich
python -m nexus demo-seed-rich
```

Expected:

- output includes `Rich demo seed ready` or `Rich demo seed already present`
- counts include at least:
  - `cycles 4`
  - `activities 10`
  - `entities 7`
  - `documents 9`
- the seeded workspace includes active, completed, and archived cycles
- at least one document integrity issue is visible later in the cockpit

Failure signals:

- command exits non-zero
- counts remain close to the small technical seed
- cockpit later shows a nearly empty or overly perfect scenario

Use this seed for:

- human evaluation
- demos
- screenshot capture
- checking whether the cockpit helps a reviewer reason about tension, blockage, and document drift

## 5. Check workspace status

Run:

```bash
python -m nexus status
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

## 6. Inspect audit trail

Run:

```bash
python -m nexus audit --limit 20
```

Expected:

- table header:
  `Timestamp | Action | Entity Type | Entity ID | Agent`
- recent `create` rows for seeded records

Failure signals:

- command exits non-zero
- no table output in a seeded workspace
- obvious missing audit rows after successful seed

## 7. Serve the local MVP

Run:

```bash
python -m nexus serve
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

## 8. Open the cockpit

Open:

```text
http://127.0.0.1:3000/
```

Expected:

- cockpit page loads
- workspace status is visible
- counts for entities, documents, relations, cycles, and activities are visible
- cycles, activities, documents, and audit panel all render data
- in the rich seed workspace, the cockpit shows:
  - more than one cycle state
  - a blocked activity
  - at least one draft and one archived document
  - at least one document with an integrity problem

Failure signals:

- blank page
- API errors rendered in the shell
- counts missing despite seeded workspace
- audit panel stays empty in a seeded workspace

## 9. Verify the local API directly

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
