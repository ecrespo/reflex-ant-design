# Tasks — reflex-ant-design

**Status:** Phases 0–4 complete in 0.1.0; phases 5+ are the roadmap.
**Source:** migrated from `docs/sdd/05-implementation-plan.md` (Phase 3 — Tasks).

Each phase has a verifiable "Done" gate. Checked boxes are delivered in 0.1.0;
unchecked are the roadmap. `_Requirements:_` references trace back to
[requirements.md](requirements.md).

## Phase 0 — Project scaffold

- [x] 0. Project scaffold
- [x] 0.1 Create the Reflex custom-component layout (`custom_components/`, demo app)
- [x] 0.2 Configure `pyproject.toml` (setuptools, package discovery, ruff, pytest)
- [x] 0.3 Set up `uv` env, git on `main`, CI workflow
  - **Done when:** `uv run python -c "import reflex_ant_design"` works; `git`
    repo on `main`; CI file present.
  - _Requirements: R8_

## Phase 1 — Base & theming

- [x] 1. Base & theming
- [x] 1.1 `AntdComponent` base with pinned `library` + reset CSS
- [x] 1.2 `ConfigProvider` and `App` providers; shared literal types
  - **Done when:** a themed `config_provider(button(...))` renders to JSX.
  - _Requirements: R5, R6_

## Phase 2 — Core component breadth

- [x] 2. Core component breadth
- [x] 2.1 Wrap every category to a useful depth (General, Layout, Navigation,
      Data Entry, Data Display, Feedback)
- [x] 2.2 Compound components via dotted tags
- [x] 2.3 `icon()` factory
- [x] 2.4 Close declarative-coverage gaps vs. the antd component menu: add
      `Calendar` (Data Display) and `Affix` (grouped with Navigation; antd
      lists it under "Other"). Brings the wrapped set to full parity with Ant
      Design's **declarative** components.
  - **Done when:** ≥ 60 factories exported (currently 102); all render; flat +
    namespace APIs match; no declarative antd component is unwrapped.
  - _Requirements: R1, R2, R7_

## Phase 3 — Demo & tests

- [x] 3. Demo & tests
- [x] 3.1 Demo app exercising all six categories with live state and theming
- [x] 3.2 `tests/test_catalog.py` (every factory renders)
- [x] 3.3 `tests/test_components.py` (tags, dotted imports, events)
  - **Done when:** `pytest` green, `ruff` clean, demo page renders.
  - _Requirements: R3, R4, R9, R10_

## Phase 4 — Packaging & docs

- [x] 4. Packaging & docs
- [x] 4.1 README (PyPI page), SDD docs, usage + compatibility guides, CHANGELOG
- [x] 4.2 Buildable with `reflex component build`
  - **Done when:** `dist/*.whl` + `*.tar.gz` produced; docs complete.
  - _Requirements: R8_

## Phase 5 — Type stubs & polish ⏳

- [ ] 5. Type stubs & polish
- [ ] 5.1 Ship generated `.pyi` stubs (`reflex component build` / PyiGenerator)
      and `py.typed`
- [ ] 5.2 Expand prop coverage on Table, Form, Tree from real-world usage
  - **Done when:** editors autocomplete props; stubs shipped in the wheel.
  - _Requirements: SHOULD (type stubs)_

## Phase 6 — Imperative feedback ⏳

- [ ] 6. Imperative feedback
- [ ] 6.1 Provide `message` / `notification` / `Modal.confirm` via a
      hook-backed helper (custom code + an event-trigger bridge)
  - **Done when:** `State`-triggered toast appears without manual JS.
  - _Requirements: COULD (imperative helpers)_

## Phase 7 — Date/Form ergonomics ⏳

- [ ] 7. Date/Form ergonomics
- [ ] 7.1 Optional `dayjs` value conversion for pickers (Python
      `date`/`datetime` ↔ dayjs) behind a `value`/`value_format` convenience
- [ ] 7.2 A Reflex-native `Form` binding bridge
  - **Done when:** a `datetime` round-trips through DatePicker without strings.
  - _Requirements: COULD (dayjs conversion, Form bridge)_

## Phase 8 — Release ⏳

- [ ] 8. Release
- [ ] 8.1 Tag `v0.1.0`, `reflex component build`, `uv publish` to PyPI,
      `reflex component share` to the gallery
  - **Done when:** `pip install reflex-ant-design` installs the published
    package.
  - _Requirements: R8_

## Task dependency map

```
P0 ─► P1 ─► P2 ─► P3 ─► P4 ─► P8
                   └─► P5
                   └─► P6
                   └─► P7
```
