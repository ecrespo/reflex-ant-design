# 01 — Product Requirements Document (PRD)

**Feature:** `reflex-ant-design` component library.
**Author:** Ernesto Crespo.
**Audience:** maintainers, contributors, evaluating Reflex developers.
**Status:** approved (0.1.0).

## 1. Problem

Reflex ships a solid core component set (built on Radix), but teams that have
standardized on **Ant Design** — one of the most popular enterprise React UI
systems — cannot reuse its components, design language, or muscle memory in
Reflex. They would otherwise re-implement tables, forms, date pickers, and
overlays by hand.

## 2. Goal

Provide an idiomatic, Pythonic wrapper around the Ant Design React components so
Reflex developers can build enterprise UIs with `antd` widgets, theming, and
behavior — without writing JavaScript.

## 3. Target users

- **Reflex app developers** who prefer or require the Ant Design look and feel.
- **Teams migrating** an existing antd React app to Reflex.
- **Python developers** who want a batteries-included component set (rich Table,
  Form, DatePicker, Transfer, Tree) beyond the Reflex core.

## 4. User stories

- As a developer, I can render an antd `Button`/`Table`/`Select` from Python and
  bind it to Reflex state.
- As a developer, I can theme the whole app (primary color, radius, size) with a
  single `ConfigProvider`.
- As a developer, I can handle component events (`on_change`, `on_click`,
  `on_finish`) in Python event handlers and receive serializable payloads.
- As a developer, I can discover the API two ways: a flat factory import and an
  `antd.*` namespace.

## 5. Requirements

### MUST (0.1.0)

| ID | Requirement | Acceptance criteria |
| --- | --- | --- |
| R1 | Wrap the core antd component set across all 6 categories | ≥ 60 components/factories exported; each renders to valid JSX |
| R2 | Compound components work | `Input.TextArea`, `Typography.Title`, `Layout.Header`, etc. import the left-most name and render the dotted tag |
| R3 | State binding | Interactive components expose `value`/`on_change` (or antd equivalent) usable with Reflex `State` |
| R4 | Serializable events | Event specs return JSON-serializable payloads (e.g. `e.target.value`, the new value, date string) |
| R5 | Theming | `ConfigProvider` accepts a `theme` token dict and re-themes nested components |
| R6 | Single pinned npm dep | `antd` pinned once; reset CSS injected exactly once |
| R7 | Two import styles | Flat factories and an `antd` namespace, both covering the same set |
| R8 | Reflex custom-component packaging | Builds with `reflex component build` into wheel + sdist; publishable to PyPI with `uv` |
| R9 | Demo app | A runnable demo exercises every category |
| R10 | Tests | Catalog + component tests pass under `pytest`; `ruff` clean |

### SHOULD

- Type stubs (`.pyi`) shipped for editor/type-checker support.
- An `icon()` factory over `@ant-design/icons`.
- Docs: SDD set + usage/compatibility guides.

### COULD (future)

- Imperative `message`/`notification`/`Modal.confirm` helpers via hooks.
- First-class `dayjs` value conversion for date/time pickers.
- A Reflex-native `Form` binding bridge.

## 6. Out of scope (0.1.0)

- Re-implementing antd internals or styling; we wrap the upstream package.
- Pro components (`@ant-design/pro-components`), charts (`@ant-design/charts`).
- Server-side antd locale bundles beyond passing a `locale` dict.
- Guaranteeing every single prop of every component (we cover the high-value
  props; advanced props remain reachable via `custom_attrs`).

## 7. Success metrics

- A developer can build a themed dashboard (table + form + overlays) using only
  this package and Reflex core.
- Adding a new component takes < 30 minutes following `CONTRIBUTING.md`.
- `make lint test` and `reflex component build` are green in CI.
