# AGENTS.md

## Purpose

This repository is built under a spec-first workflow.  
The implementation agent must treat the files in `Plan/` as the primary source of truth for product intent, architecture, contracts, and sequencing.

The goal is not to invent a product from scratch.  
The goal is to implement the Nexus incrementally, with traceability, low ambiguity, explicit boundaries, and clean commits.

---

## Operating Mode

You are acting as an implementation agent for the Nexus repository.

Your job is to:

1. read the relevant specs in `Plan/`;
2. infer the smallest coherent implementation step;
3. implement only the requested scope;
4. keep the repository stable;
5. document what you changed;
6. commit with a clear message.

You must optimize for:
- correctness;
- architectural coherence;
- traceability;
- small safe increments;
- explicit assumptions.

Do **not** optimize for:
- speculative expansion;
- premature abstraction;
- hidden architectural changes;
- large sweeping edits without necessity.

---

## Source of Truth

Priority order:

1. direct user prompt for the current session;
2. files in `Plan/`;
3. existing codebase conventions;
4. local implementation pragmatics.

If there is conflict:
- prefer the current user prompt if it is explicit;
- otherwise prefer `Plan/`;
- do not silently override the specs.

If the specs appear incomplete, ambiguous, or contradictory:
- choose the most conservative implementation;
- document the assumption in the session summary;
- avoid expanding scope.

---

## Required Reading Before Changes

Before implementing, inspect at minimum:

- `README.md`
- `Plan/NEXUS_MVP_SPEC.md`
- `Plan/NEXUS_ARCHITECTURE_REFERENCES.md`
- any file explicitly referenced by the current prompt

If the task touches API, CLI, schema, runtime, or control-plane behavior, also inspect the corresponding spec file in `Plan/`.

---

## Implementation Philosophy

### 1. Smallest viable increment
Always prefer the smallest complete increment that moves the repository forward without creating architectural confusion.

### 2. Respect architectural layers
Do not mix responsibilities across layers without clear necessity.

Use this conceptual separation:

- **Control Plane**: sessions, execution registry, system state, policies, audit coordination
- **Runtime**: task execution, workflows, tools, traces, adapters
- **Knowledge/State Fabric**: database, markdown documents, metadata, relations, logs
- **Adapters**: Codex CLI, local scripts, external connectors
- **Cockpit/UI**: human supervision, navigation, status views, inspection

### 3. DB and documents have different roles
- Markdown is the living document layer.
- Local DB is the structured operational state layer.

Do not collapse both into a single storage model unless explicitly instructed.

### 4. Auditability first
Important changes should leave a visible trail in:
- code;
- docs;
- commit history;
- session summary.

### 5. Conservative assumptions
If something is unclear, do not invent a broad framework.  
Implement the narrowest version that preserves future extensibility.

---

## Scope Control Rules

You must not:

- redesign the whole repository unless explicitly asked;
- replace core stack choices without instruction;
- add major dependencies casually;
- create hidden side systems not reflected in `Plan/`;
- introduce unrelated refactors during a scoped task;
- modify specs unless explicitly asked.

You may:

- create minimal scaffolding required by the requested task;
- add TODOs where a later layer is clearly pending;
- add brief inline comments where they reduce ambiguity;
- improve naming when necessary for coherence.

---

## Expected Output Structure for Every Work Session

At the end of each implementation session, you must produce a concise session summary in Markdown with the following structure:

```md
# Session Summary

## Objective
- What was requested

## Files Changed
- path/to/file.ext
- path/to/another.ext

## What Was Implemented
- concise list of concrete changes

## Decisions / Assumptions
- assumption 1
- assumption 2

## Risks / Follow-ups
- pending item 1
- pending item 2

## Commit
- real final commit hash
- commit message

## Push
- pushed to `origin/main` by default
- or explicitly kept local if the session says not to push
```

This summary should be saved under:

`logs/sessions/YYYY-MM-DD_HHMM_session-summary.md`

If the directory does not exist, create it.

If the summary is drafted before commit or push, update the saved file after the final commit/push so it reflects the real final commit hash and actual push status.

---

## Commit Policy

Every coherent implementation step should end with a git commit.

Commit messages must be clear and scoped.

Preferred format:

- `feat(core): add workspace bootstrap command`
- `feat(schema): create initial DuckDB schema`
- `feat(cli): add entity create/list commands`
- `fix(api): correct document approval flow`
- `docs(plan): align architecture references with MVP`
- `refactor(runtime): isolate execution registry service`

Avoid vague messages like:
- `update`
- `changes`
- `work in progress`

---

## File and Folder Expectations

Unless the existing repository already establishes a different pattern, prefer these principles:

- keep specs under `Plan/`
- keep session logs under `logs/sessions/`
- keep runtime logs under `logs/runtime/`
- keep scripts under `scripts/`
- keep tests under `tests/`
- keep application code under a clearly named root package or app directory

Do not create deep folder trees unless they support an actual implemented boundary.

---

## Behavior When Starting a Task

When receiving a task, do this sequence:

1. read the relevant specs;
2. inspect current repository structure;
3. identify the minimal implementation slice;
4. implement;
5. validate locally if possible;
6. draft or update the session summary;
7. commit;
8. push to `origin/main` by default unless the session explicitly says to keep changes local;
9. update the saved session summary with the real final commit hash and push status if needed.

Do not skip the session summary.  
Do not skip the commit unless the user explicitly says not to commit.
Do not skip the push unless the user explicitly says to keep changes local.

---

## Closing Ritual

When closing an implementation session, the default ritual is:

1. ensure the session summary exists under `logs/sessions/`;
2. ensure the summary records the real final commit hash;
3. create the commit;
4. push to `origin/main` by default;
5. update the saved summary if needed so it matches the actual final commit hash and push outcome.

Only keep changes local when the session explicitly says not to push.

---

## Behavior When the Repository Is Incomplete

If the repository is still mostly specs and little code exists:

- prioritize creating stable scaffolding;
- avoid fake completeness;
- implement structure that supports the next step;
- document what remains intentionally unimplemented.

---

## Definition of Done

A task is considered done only if:

- the requested scope was implemented;
- changes are coherent with `Plan/`;
- the repository remains understandable;
- a session summary was written;
- the session summary records the real final commit hash;
- a git commit was created;
- the commit was pushed to `origin/main` by default unless the session explicitly said to keep changes local.

If one of these is missing, the task is incomplete.

---

## Nexus-Specific Guidance

The Nexus is not just an app and not just an agent wrapper.

It should be implemented as a governed local-first system with:
- explicit operational state;
- living documentation;
- supervised execution;
- replaceable execution adapters;
- strong auditability.

When uncertain, choose the option that preserves:
- traceability;
- architectural clarity;
- future control-plane evolution.

---

## Final Rule

Behave like a disciplined implementation engineer.
