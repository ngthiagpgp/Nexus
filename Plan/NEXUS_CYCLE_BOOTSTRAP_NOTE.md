# NEXUS_CYCLE_BOOTSTRAP_NOTE

## Purpose

Record the conservative implementation decision for the first `cycle` CLI slice.

## Note

The schema requires only:

- `type`
- `start_date`

The CLI spec also implies an id derived from the cycle itself, but the examples are not fully consistent:

- `cycle-daily-2026-03-13`
- `cycle-weekly-2026-W11`

To avoid inventing calendar logic too early, the first `cycle create` implementation uses a deterministic id based only on the schema-required inputs:

- `cycle-{type}-{YYYY-MM-DD}`

This keeps the slice narrow and sufficient for downstream references such as:

- `nexus activity create --cycle-id ...`

This implementation intentionally does not add:

- ISO week inference
- auto-generated monthly or strategic naming schemes
- scheduling semantics beyond explicit start and optional end

Richer cycle naming and time semantics should be handled in a later dedicated slice.
