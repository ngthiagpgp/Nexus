# NEXUS Document Integrity States Note

## Purpose

Clarify the first read-only document integrity verification slice without introducing automatic repair or sync.

## Scope

The integrity flow verifies document records already known to DuckDB against the current workspace filesystem.

This slice does not:

- scan arbitrary Markdown files outside the DB registry
- rewrite DB metadata automatically
- repair path or hash drift
- edit document content

## Integrity states

### `ok`

Returned when all currently supported checks pass:

- DB record exists
- backing Markdown file exists
- DB path matches the current canonical path derived from type and title
- current file content hash matches `documents.content_hash`

### `warning`

Returned when the record is still readable but drift exists that does not yet block basic inspection.

Current warning condition:

- `path_mismatch`

### `error`

Returned when divergence blocks trustworthy inspection of the backing document.

Current error conditions:

- `missing_backing_file`
- `backing_file_unreadable`
- `content_hash_mismatch`

## Rationale

- Keeps integrity verification explicit and inspectable.
- Preserves the separation between Markdown content and DuckDB metadata.
- Creates a conservative foundation for future reconciliation flows.
