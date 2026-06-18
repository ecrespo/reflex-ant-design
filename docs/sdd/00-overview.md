# reflex-ant-design — SDD Overview

**Document set:** Spec-Driven Design (SDD) for the `reflex-ant-design` library.
**Audience:** maintainers and contributors.
**Status:** approved for 0.1.0.
**Last updated:** 2026-06-17.

## What this is

`reflex-ant-design` wraps the [Ant Design](https://ant.design) React component
library (`antd`) as [Reflex](https://reflex.dev) components, so Reflex apps can
use the full Ant Design system from Python.

This `docs/sdd` folder is the **primary design artifact**. Per the SDD method,
the spec was written and reviewed before the implementation, and is kept in the
repo, version-controlled, and updated when the API changes.

## The SDD flow for this project

```
PRD (what & why)
  → API Spec (the public component/factory contract)
    → Technical Design (how we wrap React in Reflex)
      → Data Model (Python ↔ JS prop/event type mapping)
        → Implementation Plan (phased rollout)
```

## Documents

| # | Document | Purpose |
| --- | --- | --- |
| 01 | [PRD](01-prd.md) | Problem, goals, users, scope, acceptance criteria |
| 02 | [API Spec](02-api-spec.md) | The public Python API: factories, props, events |
| 03 | [Technical Design](03-technical-design.md) | Wrapping architecture & key decisions |
| 04 | [Data Model](04-data-model.md) | Prop/event type mappings and serialization rules |
| 05 | [Implementation Plan](05-implementation-plan.md) | Phases, milestones, done-criteria |
| 06 | [Component Catalog](06-component-catalog.md) | Every antd component → wrapper mapping |
| 07 | [Usage Example](07-usage-example.md) | A worked end-to-end example app |

## Non-negotiable principles

1. **One pinned npm dependency.** `antd` version is pinned once in `base.py`.
2. **State-drivable.** Every interactive component exposes `value`/`on_change`
   (or the antd equivalent) so it binds to Reflex state.
3. **Serializable events.** Event specs extract JSON-serializable payloads.
4. **Spec stays in sync.** Adding a component updates the catalog (doc 06) and
   the tests in the same change.
