# Requirements — reflex-ant-design

**Feature:** `reflex-ant-design` component library.
**Author:** Ernesto Crespo.
**Audience:** maintainers, contributors, evaluating Reflex developers.
**Status:** approved (0.1.0).
**Source:** migrated from `docs/sdd/01-prd.md` (Phase 1 — Requirements).

## Problem

Reflex ships a solid core component set (built on Radix), but teams that have
standardized on **Ant Design** — one of the most popular enterprise React UI
systems — cannot reuse its components, design language, or muscle memory in
Reflex. They would otherwise re-implement tables, forms, date pickers, and
overlays by hand.

## Goal

Provide an idiomatic, Pythonic wrapper around the Ant Design React components so
Reflex developers can build enterprise UIs with `antd` widgets, theming, and
behavior — without writing JavaScript.

## Target users

- **Reflex app developers** who prefer or require the Ant Design look and feel.
- **Teams migrating** an existing antd React app to Reflex.
- **Python developers** who want a batteries-included component set (rich Table,
  Form, DatePicker, Transfer, Tree) beyond the Reflex core.

## User stories

- **As a developer**, I want to render an antd `Button`/`Table`/`Select` from
  Python and bind it to Reflex state, so that I can build UIs without JS.
- **As a developer**, I want to theme the whole app (primary color, radius,
  size) with a single `ConfigProvider`, so that the look is consistent.
- **As a developer**, I want to handle component events (`on_change`,
  `on_click`, `on_finish`) in Python event handlers and receive serializable
  payloads, so that state stays in Python.
- **As a developer**, I want to discover the API two ways — a flat factory
  import and an `antd.*` namespace — so that I can use whichever fits my style.

## Acceptance criteria (EARS)

EARS = Easy Approach to Requirements Syntax. Each criterion is testable.

### R1 — Component breadth (MUST, 0.1.0)

1. WHEN the package is imported THEN the system SHALL export ≥ 60
   components/factories spanning all 6 antd categories (General, Layout,
   Navigation, Data Entry, Data Display, Feedback).
2. WHEN any exported factory is rendered THEN the system SHALL emit valid JSX.

### R2 — Compound components (MUST, 0.1.0)

1. WHEN a compound member factory (e.g. `text_area`, `title`, `header`) is
   rendered THEN the system SHALL import the left-most antd name and render the
   dotted tag (`Input.TextArea`, `Typography.Title`, `Layout.Header`).

### R3 — State binding (MUST, 0.1.0)

1. WHEN an interactive component is given a `value` bound to Reflex `State` THEN
   the system SHALL render the current state value.
2. WHEN the user interacts with that component THEN the system SHALL invoke the
   bound `on_change` (or antd equivalent) handler.

### R4 — Serializable events (MUST, 0.1.0)

1. WHEN a component event fires THEN the system SHALL deliver a JSON-serializable
   payload to the Python handler (e.g. `e.target.value`, the new value, a date
   string).
2. IF the native antd argument is non-serializable (DOM event, `dayjs`, antd
   `Color`) THEN the system SHALL extract the primitive/string instead of
   forwarding the raw object.

### R5 — Theming (MUST, 0.1.0)

1. WHEN `config_provider` is given a `theme` token dict THEN the system SHALL
   re-theme every nested component.

### R6 — Single pinned npm dependency (MUST, 0.1.0)

1. WHEN any antd component is used THEN the system SHALL resolve a single,
   centrally pinned `antd` version.
2. WHEN one or more antd components render on a page THEN the system SHALL inject
   the antd reset CSS exactly once.

### R7 — Two import styles (MUST, 0.1.0)

1. WHEN a developer imports from the package THEN the system SHALL offer both
   flat factories and an `antd` namespace covering the same set.

### R8 — Reflex custom-component packaging (MUST, 0.1.0)

1. WHEN `reflex component build` runs THEN the system SHALL produce a wheel and
   an sdist publishable to PyPI with `uv`.

### R9 — Demo app (MUST, 0.1.0)

1. WHEN the demo app runs THEN the system SHALL exercise every antd category with
   live state and theming.

### R10 — Tests & lint (MUST, 0.1.0)

1. WHEN `pytest` runs THEN the catalog and component tests SHALL pass.
2. WHEN `ruff` runs THEN the system SHALL report no lint violations.

## SHOULD (non-blocking for 0.1.0)

- Type stubs (`.pyi`) shipped for editor/type-checker support.
- An `icon()` factory over `@ant-design/icons`.
- Docs: SDD set + usage/compatibility guides.

## COULD (future)

- Imperative `message`/`notification`/`Modal.confirm` helpers via hooks.
- First-class `dayjs` value conversion for date/time pickers.
- A Reflex-native `Form` binding bridge.

## Out of scope (0.1.0)

- Re-implementing antd internals or styling; we wrap the upstream package.
- Pro components (`@ant-design/pro-components`), charts (`@ant-design/charts`).
- Server-side antd locale bundles beyond passing a `locale` dict.
- Guaranteeing every single prop of every component (we cover the high-value
  props; advanced props remain reachable via `custom_attrs`).

## Validation status (2026-06-18)

A full audit of the implementation against the current Ant Design component menu
was performed. Result:

- **Declarative components: full parity.** Every Ant Design component that ships
  as a renderable React element is wrapped (102 factories). The audit closed the
  two remaining gaps — `Calendar` (Data Display) and `Affix` (Other) — which are
  now implemented, exported via both APIs, and covered by tests.
- **Imperative APIs: remaining work (Phase 6).** `message`, `notification`, and
  `Modal.confirm` are hook-driven imperative APIs with no JSX element, so they
  cannot be wrapped as factories. They stay roadmapped in
  [tasks.md](tasks.md) Phase 6 with a documented custom-code workaround.

## Success metrics

- A developer can build a themed dashboard (table + form + overlays) using only
  this package and Reflex core.
- Adding a new component takes < 30 minutes following `CONTRIBUTING.md`.
- `make lint test` and `reflex component build` are green in CI.
