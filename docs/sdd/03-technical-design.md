# 03 — Technical Design (the How)

## 1. Strategy

Reflex can wrap any React component by subclassing `rx.Component` and declaring
`library` (npm package) + `tag` (export name). Ant Design is a pure React
component library distributed as the `antd` npm package, so it is an ideal
wrapping target: almost every component is a named export.

We therefore build a thin, declarative wrapper layer — no custom JS bundle —
and let Reflex's compiler emit the imports and JSX.

## 2. Module layout

```
custom_components/reflex_ant_design/
├── base.py          # AntdComponent base, ConfigProvider, App, version pin
├── general.py       # Button, FloatButton, Typography, icon()
├── layout.py        # Divider, Flex, Row/Col, Layout/*, Space, Splitter
├── navigation.py    # Anchor, Breadcrumb, Dropdown, Menu, Pagination, Steps, Tabs
├── data_entry.py    # Input/*, Select, pickers, toggles, Form/*
├── data_display.py  # Avatar, Badge, Card, Table, Tag, Tree, ...
├── feedback.py      # Alert, Drawer, Modal, Progress, Spin, ...
├── namespace.py     # the `antd` SimpleNamespace
└── __init__.py      # flat factories + __all__ + version
```

One module per Ant Design category mirrors the upstream documentation, keeping
the mapping obvious and contributions localized.

## 3. The base component

```python
class AntdComponent(rx.Component):
    library = "antd@^6.0.0"          # pinned once, inherited everywhere
    def _get_custom_code(self) -> str:
        return 'import "antd/dist/reset.css";'
```

- `library` is declared once; every component inherits the same pinned version.
  Reflex de-duplicates the npm dependency.
- `_get_custom_code` injects the antd reset stylesheet. Reflex emits identical
  custom code only once, so importing it from the base is safe regardless of how
  many antd components a page uses.

## 4. Key decisions

### D1 — Compound components use dot-qualified tags

Antd exposes many subcomponents as members (`Input.TextArea`, `Layout.Header`,
`Typography.Title`). Reflex's import logic imports only the **left-most** name of
a dotted tag and renders the full member access:

```python
class TextArea(Input):
    tag = "Input.TextArea"   # imports { Input } from antd, renders <Input.TextArea/>
```

*Alternative considered:* one wrapper per subexport with `alias`. Rejected —
antd does not export `TextArea` directly, so the import would fail.

### D2 — Event specs extract serializable payloads

Antd handlers pass DOM events or rich objects. We declare an `rx.EventHandler`
spec per event that selects the serializable part:

```python
_on_input  = lambda e: [e.target.value]      # text inputs
_on_checked = lambda e: [e.target.checked]    # checkbox/radio
_on_value  = lambda value: [value]            # value-first controls
_on_date   = lambda date, s: [s]              # pickers → formatted string
```

*Why:* the Python backend can only receive JSON. Passing the raw `dayjs` object
or DOM event would fail to serialize.

### D3 — `data`-driven props stay as Python lists/dicts

Antd v5+ favors `items`/`columns`/`options`/`treeData` arrays of objects over
nested children. We expose these as `rx.Var[list[dict]]`, so the entire
structure can be computed in Reflex state. This is the most natural fit for
Reflex's data flow.

### D4 — Icons via a cached factory

`@ant-design/icons` has hundreds of exports. Rather than hand-wrap each, the
`icon(name)` factory builds (and caches) a small `rx.Component` subclass with
`tag=name` and `library="@ant-design/icons"`. One function covers the whole set.

### D5 — Theming is data, not code

`ConfigProvider.theme` is a plain dict (design tokens). This serializes cleanly
and can be a computed `rx.var`. The dark/light **algorithm** needs an antd
function reference, which is documented as an advanced custom-code step rather
than wrapped as a string (see usage guide).

### D6 — No `NoSSRComponent` by default

Antd renders fine under SSR, so components extend `rx.Component`. Should a
specific component need client-only rendering, it can switch to
`rx.NoSSRComponent` without affecting the rest.

## 5. Packaging

This is a Reflex **custom component** (`reflex component init` layout):

- Source under `custom_components/reflex_ant_design/` (declared in
  `pyproject.toml` via `[tool.setuptools.packages.find] where = ["custom_components"]`).
- Demo app under `reflex_ant_design_demo/`.
- Build with `reflex component build` → `dist/*.whl` + `*.tar.gz`.
- Publish with `uv publish` (or `twine`).

## 6. Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| antd major bump breaks props | Version pinned in `base.py`; compatibility guide documents v5/v6 |
| `dayjs` value round-tripping | Pickers expose formatted strings via `on_change`; advanced dayjs path documented |
| React 18 vs 19 peer mismatch | Default `antd@^6` (React 19); `antd@^5` documented for React 18 |
| Imperative APIs (message/notification) | Out of scope for 0.1.0; documented workaround with custom code |
