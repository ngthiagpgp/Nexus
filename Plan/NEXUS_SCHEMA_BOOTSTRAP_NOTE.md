# NEXUS_SCHEMA_BOOTSTRAP_NOTE

**Status:** Draft  
**Purpose:** Registrar uma observacao tecnica estreita sobre a inicializacao local do schema do Nexus MVP.

---

## Issue observed during bootstrap

The current schema in `Plan/NEXUS_MVP_SCHEMA.sql` defines:

- `system_state.value` as `NOT NULL`

But the same schema also seeds:

- `last_backup`
- `last_sync`

with `NULL`-like operational values.

This creates a real bootstrap inconsistency for a strict DuckDB initialization flow.

---

## Conservative handling adopted in code

The bootstrap layer applies a single targeted compatibility normalization when loading the schema for local initialization:

- `VALUES ('last_backup', NULL)` becomes `VALUES ('last_backup', '')`
- `VALUES ('last_sync', NULL)` becomes `VALUES ('last_sync', '')`

This is intentionally narrow:

- it is applied in one place only, inside the schema bootstrap loader;
- it does not rewrite the original planning/spec files;
- it keeps the substrate runnable while the spec remains under refinement.

---

## Why this note exists

This note makes the compatibility decision explicit so the bootstrap is not silently hiding a schema-level inconsistency.

The product intent is unchanged.

The practical effect is only:

- local initialization remains deterministic;
- the mismatch is documented;
- future spec refinement can resolve it deliberately instead of accidentally.
