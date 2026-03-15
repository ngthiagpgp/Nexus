# Demo Seed Rich Spec

## 1. Why the Current Seed Is Not Enough

The current seed is appropriate for smoke testing and sanity checking:

- one cycle;
- a very small number of activities;
- a very small number of documents;
- limited structural context;
- minimal ambiguity.

That is sufficient to verify that the CLI, API, and cockpit behave coherently.

It is not sufficient for:

- serious human testing;
- evaluating the true capacity of the UI;
- demonstrating the product convincingly;
- introducing real cognitive tension into the operational model.

The current seed proves that the system works. It does not yet prove that the system is powerful or human-legible under richer operational conditions.

## 2. Purpose of a Rich Demo Seed

A rich demo seed should exist to:

- reveal the strength of the UI;
- reveal the strength of the operational model;
- support serious human testing;
- support product demonstrations;
- provide a stable base for screenshots, walkthroughs, and version-to-version comparison.

This is not merely more data. It is a deliberately shaped scenario that stresses whether the cockpit helps a human understand and supervise work.

## 3. Separation of Concerns

The repository should treat the two seeds as different tools:

- technical seed != demo seed;
- the technical seed stays simple, reliable, and low-noise;
- the rich demo seed may be more elaborate, narrative, and operationally loaded.

The technical seed is for repeatable validation.

The rich demo seed is for comprehension, demonstration, and UI evaluation.

## 4. Minimum Scenario Complexity

The rich demo seed should include, at minimum:

- multiple cycles with distinct states;
- activities with priority differences, blocked work, delayed work, and dependency-like tension;
- documents of different types and lifecycle states;
- supporting documents that are meaningfully linked to ongoing work;
- entities and relations sufficient to provide structural context;
- a live-looking audit trail with both routine and sensitive changes;
- some clean cases and some ambiguous or problematic cases.

It should contain enough variation that the cockpit must help the operator distinguish stable work from unstable work.

## 5. Example Narrative World

One plausible narrative world for the rich demo seed is a local coordination workspace for Nexus product delivery and operational supervision.

Example structure:

- one active planning cycle preparing the next operating window;
- one active execution cycle where work is moving now;
- one delayed or recovery cycle carrying unresolved issues;
- one blocked activity waiting on missing evidence or unresolved document drift;
- one document that is outdated relative to current execution;
- one document with reconciliation pending after safe file drift;
- several stakeholder or reference entities linked to decisions, work areas, and supporting material.

This kind of world is useful because it creates mixed states:

- not all work is healthy;
- not all documents are aligned;
- not all cycles are equally relevant;
- not all context is immediately actionable.

That is the right stress case for the cockpit.

## 6. Data Design Guidelines

The rich demo seed should be designed with these rules:

- do not generate only perfect cases;
- include operational tension rather than just completed happy paths;
- include relations that matter for interpretation;
- include contrast across states and urgency;
- include enough material for real inspection, not just list rendering.

Practical implications:

- some activities should feel routine;
- some should feel blocked or risky;
- some documents should clarify work;
- some should create doubt or require validation;
- some entities should matter to the current cycle;
- some should remain background context.

## 7. What the Rich Seed Should Make Visible in the UI

The rich seed should make the following visible in the cockpit:

- operational focus;
- transition or contrast between cycles;
- difference between stable activities and problematic ones;
- the role of supporting documents in decision and execution;
- structural context through entities and relations;
- auditability and confidence signals.

If the seed does not make these things visible, it is not yet rich enough for UI evaluation.

## 8. Acceptance Criteria

The rich demo seed is good enough when it produces a workspace where:

- at least three cycles exist with clearly different operational states;
- at least one cycle feels obviously primary and at least one clearly secondary;
- at least nine activities exist across cycles, with meaningful status contrast;
- at least one activity is blocked by evidence, missing support, or unresolved dependency;
- at least eight documents exist across draft, approved, archived, and drifted states;
- at least one document requires reconcile;
- entities and relations add context that a human can actually use during inspection;
- the audit trail includes enough changes to feel operational rather than synthetic;
- a human reviewer can spend several minutes navigating the cockpit without exhausting the scenario immediately.

## 9. Non-Goals

The rich demo seed does not need to be:

- a performance benchmark;
- a real dataset;
- a perfect world simulation;
- a substitute for the final data model.

Its role is to create enough operational depth to test the product honestly.

## 10. Recommended Next Step

After this spec is approved, the next step should be to implement the rich demo seed as a separate demonstrator path rather than expanding the existing smoke-test seed in place.

That implementation should remain incremental, traceable, and explicitly separate from the technical seed used for fast regression checks.
