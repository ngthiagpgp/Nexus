# NEXUS Document Reconciliation Note

## Purpose

Define the first controlled reconciliation slice for file-backed documents without introducing automatic repair.

## What reconciliation does in this slice

Reconciliation is explicit and targeted to one document at a time.

When the current backing Markdown file is readable, the flow may:

- update `documents.content_hash` to the current file hash;
- update `documents.path` to the canonical path derived from document type and title, but only when that canonical path already resolves to the same backing file.

Every successful reconciliation writes an explicit `audit_log` entry.

## What reconciliation does not do in this slice

This flow does not:

- edit Markdown content;
- move or rename files automatically;
- scan arbitrary files outside the registered document path;
- perform bulk repair;
- choose between competing candidate files silently.

## Refusal conditions

Reconciliation must refuse clearly when:

- the document record does not exist;
- the backing Markdown file is missing;
- the selector is ambiguous;
- both the stored path and the canonical path exist as different files;
- only path drift exists but the canonical file is not present yet, making a DB-only path rewrite unsafe.

## Rationale

This keeps reconciliation grounded in the current file-backed state and preserves the separation between:

- Markdown as living content;
- DuckDB as structured operational metadata.
