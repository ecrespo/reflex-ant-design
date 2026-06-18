# 05 — Implementation Plan (phases)

Phased rollout. Each phase has a verifiable "Done" gate. Phases 0–4 are
**complete in 0.1.0**; phases 5+ are the roadmap.

## Phase 0 — Project scaffold ✅

- Create the Reflex custom-component layout (`custom_components/`, demo app).
- Configure `pyproject.toml` (setuptools, package discovery, ruff, pytest).
- Set up `uv` env, git on `main`, CI workflow.

**Done when:** `uv run python -c "import reflex_ant_design"` works; `git` repo on
`main`; CI file present.

## Phase 1 — Base & theming ✅

- `AntdComponent` base with pinned `library` + reset CSS.
- `ConfigProvider` and `App` providers; shared literal types.

**Done when:** a themed `config_provider(button(...))` renders to JSX.

## Phase 2 — Core component breadth ✅

Wrap every category to a useful depth:

- General, Layout, Navigation, Data Entry, Data Display, Feedback.
- Compound components via dotted tags.
- `icon()` factory.

**Done when:** ≥ 60 factories exported; all render; flat + namespace APIs match.

## Phase 3 — Demo & tests ✅

- Demo app exercising all six categories with live state and theming.
- `tests/test_catalog.py` (every factory renders) and
  `tests/test_components.py` (tags, dotted imports, events).

**Done when:** `pytest` green, `ruff` clean, demo page renders.

## Phase 4 — Packaging & docs ✅

- README (PyPI page), SDD docs, usage + compatibility guides, CHANGELOG.
- Buildable with `reflex component build`.

**Done when:** `dist/*.whl` + `*.tar.gz` produced; docs complete.

## Phase 5 — Type stubs & polish ⏳

- Ship generated `.pyi` stubs (`reflex component build` / PyiGenerator) and
  `py.typed`.
- Expand prop coverage on Table, Form, Tree from real-world usage.

**Done when:** editors autocomplete props; stubs shipped in the wheel.

## Phase 6 — Imperative feedback ⏳

- Provide `message` / `notification` / `Modal.confirm` via a hook-backed helper
  (custom code + an event-trigger bridge).

**Done when:** `State`-triggered toast appears without manual JS.

## Phase 7 — Date/Form ergonomics ⏳

- Optional `dayjs` value conversion for pickers (Python `date`/`datetime` ↔
  dayjs) behind a `value`/`value_format` convenience.
- A Reflex-native `Form` binding bridge.

**Done when:** a `datetime` round-trips through DatePicker without strings.

## Phase 8 — Release ⏳

- Tag `v0.1.0`, `reflex component build`, `uv publish` to PyPI,
  `reflex component share` to the gallery.

**Done when:** `pip install reflex-ant-design` installs the published package.

## Task dependency map

```
P0 ─► P1 ─► P2 ─► P3 ─► P4 ─► P8
                   └─► P5
                   └─► P6
                   └─► P7
```
