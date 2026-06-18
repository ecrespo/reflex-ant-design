# reflex-ant-design — Spec

**Status:** approved for 0.1.0. **Last updated:** 2026-06-17.
**Audience:** maintainers and contributors.

`reflex-ant-design` wraps the [Ant Design](https://ant.design) React component
library (`antd`) as [Reflex](https://reflex.dev) components, so Reflex apps can
use the full Ant Design system from Python.

This `specs/reflex-ant-design/` folder is the **primary design artifact**,
restructured into the canonical [spec-driven development](https://github.com/)
three-phase flow. It was migrated from the original numbered SDD set, which is
preserved verbatim under [`docs/sdd/`](../../docs/sdd/) for reference.

## The three phases

```
requirements.md (what & why, EARS)
  → design.md (architecture, API contract, data model, component catalog)
    → tasks.md (phased rollout with done-gates, traced to requirements)
```

## Documents

| Phase | Document | Purpose | Migrated from |
| --- | --- | --- | --- |
| 1 | [requirements.md](requirements.md) | Problem, goals, users, EARS acceptance criteria | `01-prd.md` |
| 2 | [design.md](design.md) | Wrapping architecture, public API, type/event mapping, full component catalog | `02-api-spec.md`, `03-technical-design.md`, `04-data-model.md`, `06-component-catalog.md` |
| 3 | [tasks.md](tasks.md) | Phases, milestones, done-criteria, requirement traceability | `05-implementation-plan.md` |
| — | [usage-example.md](usage-example.md) | A worked end-to-end example app | `07-usage-example.md` |

## Non-negotiable principles

1. **One pinned npm dependency.** `antd` version is pinned once in `base.py`.
2. **State-drivable.** Every interactive component exposes `value`/`on_change`
   (or the antd equivalent) so it binds to Reflex state.
3. **Serializable events.** Event specs extract JSON-serializable payloads.
4. **Spec stays in sync.** Adding a component updates the catalog in
   [design.md](design.md) and the tests in the same change.