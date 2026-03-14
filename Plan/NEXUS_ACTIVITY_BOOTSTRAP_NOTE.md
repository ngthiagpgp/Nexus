# NEXUS_ACTIVITY_BOOTSTRAP_NOTE

## Purpose

Record the conservative implementation decision for the first `activity` CLI slice.

## Note

The current schema makes `activities.cycle_id` mandatory and links it to `cycles.id`.

The current CLI spec also models activities as items that exist inside a cycle:

- `nexus activity add --cycle_id CYCLE_ID <title>`

At this stage of the bootstrap, the repository does not yet expose a user-facing cycle creation flow.

Because of that, the first `activity create` implementation should stay narrow:

- require `--cycle-id`
- validate that the referenced cycle already exists
- persist only the minimal activity fields supported directly by the current schema defaults

This preserves schema intent without inventing fallback behavior such as:

- implicit cycle creation
- nullable `cycle_id`
- auto-assignment to a synthetic cycle

Cycle management should be implemented in a later dedicated slice.
