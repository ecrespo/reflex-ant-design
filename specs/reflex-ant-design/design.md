# Design — reflex-ant-design

**Status:** approved (0.1.0).
**Source:** consolidated from `docs/sdd/02-api-spec.md`, `03-technical-design.md`,
`04-data-model.md`, and `06-component-catalog.md` (Phase 2 — Design).

## Overview

`reflex-ant-design` wraps the Ant Design React library (`antd` npm package) as
Reflex components. Reflex can wrap any React component by subclassing
`rx.Component` and declaring `library` (npm package) + `tag` (export name). Ant
Design is a pure React component library where almost every component is a named
export, making it an ideal wrapping target.

We build a thin, declarative wrapper layer — **no custom JS bundle** — and let
Reflex's compiler emit the imports and JSX. The design covers four concerns:

1. **Architecture** — module layout and the base component.
2. **Public API contract** — the surface a Reflex developer programs against.
3. **Data model** — Python ↔ JS prop/event type mapping and serialization.
4. **Component catalog** — every antd component → wrapper mapping.

## Architecture

### Module layout

```
custom_components/reflex_ant_design/
├── base.py          # AntdComponent base, ConfigProvider, App, version pin
├── general.py       # Button, FloatButton, Typography, icon()
├── layout.py        # Divider, Flex, Row/Col, Layout/*, Space, Splitter
├── navigation.py    # Affix, Anchor, Breadcrumb, Dropdown, Menu, Pagination, Steps, Tabs
├── data_entry.py    # Input/*, Select, pickers, toggles, Form/*
├── data_display.py  # Avatar, Badge, Card, Table, Tag, Tree, ...
├── feedback.py      # Alert, Drawer, Modal, Progress, Spin, ...
├── namespace.py     # the `antd` SimpleNamespace
└── __init__.py      # flat factories + __all__ + version
```

One module per Ant Design category mirrors the upstream documentation, keeping
the mapping obvious and contributions localized.

### The base component

```python
class AntdComponent(rx.Component):
    library = "antd@^6.0.0"          # pinned once, inherited everywhere
    def _get_custom_code(self) -> str:
        return 'import "antd/dist/reset.css";'
```

- `library` is declared once; every component inherits the same pinned version.
  Reflex de-duplicates the npm dependency. **(satisfies R6.1)**
- `_get_custom_code` injects the antd reset stylesheet. Reflex emits identical
  custom code only once, so importing it from the base is safe regardless of how
  many antd components a page uses. **(satisfies R6.2)**

### Packaging

This is a Reflex **custom component** (`reflex component init` layout):

- Source under `custom_components/reflex_ant_design/` (declared in
  `pyproject.toml` via
  `[tool.setuptools.packages.find] where = ["custom_components"]`).
- Demo app under `reflex_ant_design_demo/`.
- Build with `reflex component build` → `dist/*.whl` + `*.tar.gz`. **(R8)**
- Publish with `uv publish` (or `twine`).

## Components and Interfaces (public API contract)

This is the contract a Reflex developer programs against — complete enough that
an app developer can build a UI without reading the wrapper source.

### Imports (R7)

```python
# Namespace (recommended)
from reflex_ant_design import antd
antd.button(...)

# Flat factories
from reflex_ant_design import button, table, config_provider, icon
```

Every factory is a snake_case function returning an `rx.Component`. Names map to
antd component names: `Button → button`, `DatePicker → date_picker`,
`Input.TextArea → text_area`, `List → list_view` (avoids shadowing `list`).

### Calling convention

```python
factory(*children, **props)
```

- `*children` — nested Reflex components or strings (the component body).
- `**props` — snake_case props; converted to antd camelCase at compile time.
- Event handlers — passed as Reflex event handlers/specs (`on_change=State.set_x`).

```python
antd.button("Save", type="primary", size="large", on_click=State.save)
antd.select(value=State.v, on_change=State.set_v, options=[{"label": "A", "value": "a"}])
```

### Props contract

| Python form | antd form | Notes |
| --- | --- | --- |
| `type="primary"` | `type="primary"` | scalar passthrough |
| `allow_clear=True` | `allowClear={true}` | snake_case → camelCase |
| `options=[{"label","value"}]` | `options={[...]}` | list of dicts |
| `theme={"token": {...}}` | `theme={{token:{...}}}` | nested dict |
| `icon=icon("UserOutlined")` | `icon={<UserOutlined/>}` | component prop |
| `style={"width": "200px"}` | `style={{width:"200px"}}` | inline style dict |
| `custom_attrs={...}` | arbitrary attrs | escape hatch for unlisted props |

### Theming & configuration (R5)

```python
antd.config_provider(
    <subtree>,
    theme={"token": {"colorPrimary": "#722ed1", "borderRadius": 8},
           "components": {"Button": {"controlHeight": 40}}},
    component_size="large",         # default size for nested components
    direction="ltr",                # or "rtl"
    locale={...},                   # advanced
)
```

`App` (`antd.app(...)`) wraps content to enable the static feedback context and
apply reset styling. Place it just inside `config_provider`.

### Compound components (R2)

Compound members are exposed as their own factories so children compose
naturally:

```python
antd.layout(
    antd.header(...),
    antd.layout(antd.sider(...), antd.content(...)),
    antd.footer(...),
)
antd.card(antd.card_meta(title="T", description="D"))
antd.list_view(antd.list_item(antd.list_item_meta(title="X")))
```

### The `icon()` factory

```python
icon(name: str, **props) -> rx.Component
```

`name` is any export of `@ant-design/icons` (`"SearchOutlined"`,
`"HeartFilled"`). Supports `spin`, `rotate`, `style`, `on_click`.

### Stability

- Factory names and the documented props/events are the **stable surface**.
- Unlisted antd props are reachable via `custom_attrs` and are **not** part of
  the stability guarantee until promoted to a typed prop.

## Data Models (type & serialization mapping)

For a component library, the "data model" is the **mapping between Python types
and the JS props/events** that cross the Reflex compile and runtime boundary.

### Prop type mapping

| Python annotation | JS prop type | Example |
| --- | --- | --- |
| `Var[str]` | string | `placeholder="Name"` |
| `Var[int]` / `Var[float]` | number | `span=12`, `step=0.5` |
| `Var[bool]` | boolean | `disabled=True` |
| `Var[Size]` (`Literal`) | string enum | `size="large"` |
| `Var[list[dict]]` | array of objects | `options`, `columns`, `items` |
| `Var[dict]` | object | `theme`, `style`, `menu` |
| `Var[list[int]]` | number array | `gutter=[16, 24]` |
| `Var[rx.Component]` | ReactNode | `icon=icon("...")`, `prefix=...` |
| `Var[bool \| dict]` | union | `allow_clear=True` or `{...}` |

Snake_case Python prop names compile to antd camelCase
(`allow_clear → allowClear`, `default_value → defaultValue`,
`max_tag_count → maxTagCount`).

### Shared literal types (`base.py`)

```python
Size      = Literal["small", "middle", "large"]
Status    = Literal["success", "processing", "default", "error", "warning"]
Placement = Literal["top", "left", "right", "bottom"]
Variant   = Literal["outlined", "borderless", "filled", "underlined"]
```

These are reused across modules to keep enums consistent and self-documenting.

### Event payload model (R4)

Event specs define exactly what reaches the Python handler. All payloads are
JSON-serializable.

| Spec | Source signature (antd) | Python receives |
| --- | --- | --- |
| `_on_input` | `(e: ChangeEvent)` | `e.target.value` → `str` |
| `_on_checked` | `(e: ChangeEvent)` | `e.target.checked` → `bool` |
| `_on_value` | `(value)` | `value` (number/str/list/bool) |
| `_on_date` | `(dayjs, dateString)` | `dateString` → `str` |
| range pickers | `(dayjs[], dateStrings)` | `list[str]` |
| color picker | `(color, hex)` | `hex` → `str` |
| `no_args_event_spec` | `()` | nothing |
| menu/tabs/tree | `(info)` / `(keys, info)` | the info dict / key list |

The full per-component event contract:

| Component(s) | Event | Payload delivered to Python |
| --- | --- | --- |
| Input, TextArea, Search | `on_change`, `on_press_enter` | `str` (the input value) |
| InputNumber, Slider, Rate, Switch, Select, Segmented | `on_change` | the new value (number/str/list/bool) |
| Checkbox, Radio | `on_change` | `bool` (checked) |
| RadioGroup | `on_change` | `str` (selected value) |
| DatePicker, TimePicker | `on_change` | `str` (formatted date string) |
| RangePicker | `on_change` | `list[str]` (start, end) |
| ColorPicker | `on_change` | `str` (hex) |
| Button, BackTop, Tag close | `on_click`, `on_close` | no args |
| Modal | `on_ok`, `on_cancel` | no args |
| Drawer, Alert | `on_close` | no args |
| Tabs, Menu, Steps, Collapse, Tree | `on_change`/`on_select` | key(s) / info dict |
| Calendar | `on_change`, `on_select` | `str` (ISO date, via `JSON.stringify(dayjs)`) |
| Calendar | `on_panel_change` | `(str ISO date, str mode)` |
| Affix | `on_change` | `bool` (affixed) |
| Form | `on_finish` | `dict` (collected values) |
| Table | `on_change` | `(pagination, filters, sorter)` |

**Non-serializable values are filtered out.** The `dayjs` object (DatePicker),
the DOM event (`Input`), and the antd `Color` object (ColorPicker) are **never**
sent to the backend; the spec selects the string/primitive instead. This is the
core reason each event has an explicit spec rather than forwarding the raw
argument.

### Structured prop shapes (reference)

Dict shapes used by data-driven props (validated by antd at runtime, documented
here for app developers):

```python
# Select / Checkbox.Group / Radio.Group options
{"label": str, "value": str | int, "disabled": bool}

# Table column
{"title": str, "dataIndex": str, "key": str, "sorter": bool,
 "filters": [{"text": str, "value": str}], "fixed": "left" | "right"}

# Menu / Tabs / Steps / Collapse / Breadcrumb item
{"key": str, "label": str, "icon": ReactNode, "children": [...], "disabled": bool}

# Tree / TreeSelect node
{"title": str, "key": str, "value": str, "children": [...]}

# ConfigProvider theme
{"token": {"colorPrimary": str, "borderRadius": int, ...},
 "components": {"Button": {...}}, "algorithm": <function ref>}
```

### State-binding pattern (R3)

```python
class State(rx.State):
    value: str = ""
    @rx.event
    def set_value(self, v: str):
        self.value = v

antd.input(value=State.value, on_change=State.set_value)
```

The component's `value` reads from state; `on_change` writes back through a
typed event handler — a closed two-way loop entirely in Python.

## Key decisions

### D1 — Compound components use dot-qualified tags

Antd exposes many subcomponents as members (`Input.TextArea`, `Layout.Header`,
`Typography.Title`). Reflex's import logic imports only the **left-most** name of
a dotted tag and renders the full member access:

```python
class TextArea(Input):
    tag = "Input.TextArea"   # imports { Input } from antd, renders <Input.TextArea/>
```

**Context:** antd subcomponents are member accesses, not standalone exports.
**Options considered:** (1) dot-qualified tags; (2) one wrapper per subexport
with `alias`. **Decision:** dot-qualified tags. **Rationale:** antd does not
export `TextArea` directly, so the `alias` import would fail.

### D2 — Event specs extract serializable payloads

Antd handlers pass DOM events or rich objects. We declare an `rx.EventHandler`
spec per event that selects the serializable part:

```python
_on_input  = lambda e: [e.target.value]      # text inputs
_on_checked = lambda e: [e.target.checked]    # checkbox/radio
_on_value  = lambda value: [value]            # value-first controls
_on_date   = lambda date, s: [s]              # pickers → formatted string
```

**Rationale:** the Python backend can only receive JSON. Passing the raw `dayjs`
object or DOM event would fail to serialize. **(satisfies R4)**

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

## Error handling & risks

| Risk | Mitigation |
| --- | --- |
| antd major bump breaks props | Version pinned in `base.py`; compatibility guide documents v5/v6 |
| `dayjs` value round-tripping | Pickers expose formatted strings via `on_change`; advanced dayjs path documented |
| React 18 vs 19 peer mismatch | Default `antd@^6` (React 19); `antd@^5` documented for React 18 |
| Imperative APIs (message/notification) | Out of scope for 0.1.0; documented workaround with custom code |
| Non-serializable event args reach backend | Per-event specs extract primitives (D2); covered by component tests |

## Testing strategy

- `tests/test_catalog.py` — every factory renders to valid JSX (covers R1).
- `tests/test_components.py` — tags, dotted imports, and event specs (covers
  R2, R4).
- Demo app exercises all six categories with live state and theming (R9).
- `ruff` clean and `pytest` green gate every change (R10).

## Component Catalog (antd → wrapper)

Complete mapping of Ant Design components to their `reflex-ant-design` wrappers.
Legend: ✅ wrapped in 0.1.0 · ⏳ planned · ⛔ out of scope.

### General (`general.py`)

| antd | Class | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- | --- |
| Button | `Button` | `button` | type, size, shape, danger, ghost, block, loading, icon, href | on_click | ✅ |
| FloatButton | `FloatButton` | `float_button` | type, shape, description, tooltip, icon, badge | on_click | ✅ |
| FloatButton.Group | `FloatButtonGroup` | `float_button_group` | trigger, open | on_open_change | ✅ |
| FloatButton.BackTop | `BackTop` | `back_top` | visibility_height, target | on_click | ✅ |
| Typography | `Typography` | `typography` | — | — | ✅ |
| Typography.Title | `Title` | `title` | level, type, ellipsis, copyable | — | ✅ |
| Typography.Text | `Text` | `text` | strong, italic, code, mark, type, copyable | — | ✅ |
| Typography.Paragraph | `Paragraph` | `paragraph` | ellipsis, copyable | — | ✅ |
| Typography.Link | `TypographyLink` | `link` | href, target | — | ✅ |
| Icon (`@ant-design/icons`) | `_AntdIcon` | `icon(name)` | spin, rotate, style | on_click | ✅ |

### Layout (`layout.py`)

| antd | Factory | Key props | Status |
| --- | --- | --- | --- |
| Divider | `divider` | type, orientation, dashed, variant, plain | ✅ |
| Flex | `flex` | vertical, wrap, justify, align, gap | ✅ |
| Row | `row` | justify, align, gutter, wrap | ✅ |
| Col | `col` | span, offset, order, push, pull, xs–xxl | ✅ |
| Layout | `layout` | has_sider | ✅ |
| Layout.Header / Content / Footer | `header` / `content` / `footer` | — | ✅ |
| Layout.Sider | `sider` | collapsed, collapsible, width, breakpoint, theme | ✅ (on_collapse) |
| Space | `space` | direction, size, align, wrap, split | ✅ |
| Space.Compact | `space_compact` | direction, size, block | ✅ |
| Splitter | `splitter` | layout | ✅ (on_resize*) |
| Splitter.Panel | `splitter_panel` | default_size, min, max, collapsible | ✅ |

### Navigation (`navigation.py`)

| antd | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- |
| Affix | `affix` | offset_top, offset_bottom | on_change | ✅ |
| Anchor | `anchor` | items, direction, affix, offset_top | on_change, on_click | ✅ |
| Breadcrumb | `breadcrumb` | items, separator | — | ✅ |
| Dropdown | `dropdown` | menu, trigger, placement, arrow, open | on_open_change | ✅ |
| Dropdown.Button | `dropdown_button` | type, size, loading | on_click | ✅ |
| Menu | `menu` | items, mode, theme, selected_keys, open_keys | on_select, on_open_change, on_click | ✅ |
| Pagination | `pagination` | current, total, page_size, show_size_changer | on_change, on_show_size_change | ✅ |
| Steps | `steps` | items, current, direction, status, type | on_change | ✅ |
| Tabs | `tabs` | items, active_key, type, tab_position | on_change, on_tab_click, on_edit | ✅ |

> `Affix` is grouped here for cohesion (it pins navigation elements such as
> `Anchor` on scroll). Upstream Ant Design lists it under the **Other** category
> alongside `App` and `ConfigProvider`.

### Data Entry (`data_entry.py`)

| antd | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- |
| Input | `input` | value, placeholder, size, variant, allow_clear, prefix | on_change, on_press_enter | ✅ |
| Input.TextArea | `text_area` | rows, auto_size, show_count, max_length | on_change | ✅ |
| Input.Search | `search_input` | enter_button, loading | on_search | ✅ |
| Input.Password | `password_input` | visibility_toggle | on_change | ✅ |
| Input.OTP | `input_otp` | length, mask, formatter | on_change | ✅ |
| InputNumber | `input_number` | min, max, step, precision, controls | on_change | ✅ |
| Checkbox | `checkbox` | checked, indeterminate, disabled | on_change | ✅ |
| Checkbox.Group | `checkbox_group` | value, options | on_change | ✅ |
| Radio / Radio.Button | `radio` / `radio_button` | value, checked | on_change | ✅ |
| Radio.Group | `radio_group` | value, options, option_type, button_style | on_change | ✅ |
| Select | `select` | value, options, mode, show_search, allow_clear | on_change, on_search, on_select | ✅ |
| Switch | `switch` | checked, loading, size, checked_children | on_change | ✅ |
| Slider | `slider` | value, min, max, step, range, marks | on_change, on_change_complete | ✅ |
| Rate | `rate` | value, count, allow_half, character | on_change | ✅ |
| DatePicker | `date_picker` | format, picker, show_time, allow_clear | on_change, on_ok | ✅ |
| DatePicker.RangePicker | `range_picker` | format, show_time | on_change | ✅ |
| TimePicker | `time_picker` | format, use12_hours, hour_step | on_change | ✅ |
| AutoComplete | `auto_complete` | options, backfill, filter_option | on_change, on_select, on_search | ✅ |
| Cascader | `cascader` | options, multiple, change_on_select | on_change | ✅ |
| TreeSelect | `tree_select` | tree_data, tree_checkable, multiple | on_change, on_select | ✅ |
| Mentions | `mentions` | options, prefix, split | on_change, on_select, on_search | ✅ |
| ColorPicker | `color_picker` | format, presets, show_text, allow_clear | on_change, on_change_complete | ✅ |
| Transfer | `transfer` | data_source, target_keys, show_search | on_change, on_select_change | ✅ |
| Upload | `upload` | action, accept, list_type, multiple, max_count | on_change, on_remove, on_preview | ✅ |
| Upload.Dragger | `upload_dragger` | (inherits Upload) | on_drop | ✅ |
| Form | `form` | layout, initial_values, label_col, size | on_finish, on_finish_failed, on_values_change | ✅ |
| Form.Item | `form_item` | name, label, rules, required, tooltip | — | ✅ |
| Form.List | `form_list` | name | — | ✅ |

### Data Display (`data_display.py`)

| antd | Factory | Key props | Status |
| --- | --- | --- | --- |
| Avatar / Avatar.Group | `avatar` / `avatar_group` | src, icon, shape, size, max_count | ✅ |
| Badge / Badge.Ribbon | `badge` / `badge_ribbon` | count, dot, status, color, text | ✅ |
| Calendar | `calendar` | fullscreen, show_week, mode | ✅ (on_change, on_select, on_panel_change) |
| Card / Card.Meta / Card.Grid | `card` / `card_meta` / `card_grid` | title, extra, hoverable, loading, cover | ✅ |
| Carousel | `carousel` | autoplay, dots, effect, infinite | ✅ (after/before_change) |
| Collapse | `collapse` | items, accordion, bordered, ghost | ✅ (on_change) |
| Descriptions | `descriptions` | items, title, bordered, column, layout | ✅ |
| Empty | `empty` | description, image | ✅ |
| Image | `image` | src, width, preview, fallback | ✅ (on_error) |
| List / Item / Item.Meta | `list_view` / `list_item` / `list_item_meta` | data_source, bordered, pagination, grid | ✅ |
| Popover | `popover` | content, title, placement, trigger | ✅ (on_open_change) |
| Tooltip | `tooltip` | title, placement, trigger, color | ✅ (on_open_change) |
| QRCode | `qr_code` | value, size, color, error_level, status | ✅ (on_refresh) |
| Segmented | `segmented` | value, options, size, block, vertical | ✅ (on_change) |
| Statistic / Countdown | `statistic` / `statistic_countdown` | title, value, precision, prefix, suffix | ✅ |
| Table | `table` | columns, data_source, pagination, row_selection, scroll | ✅ (on_change) |
| Tag / Tag.CheckableTag | `tag` / `checkable_tag` | color, closable, checked | ✅ (on_close/on_change) |
| Timeline | `timeline` | items, mode, pending, reverse | ✅ |
| Tour | `tour` | open, steps, current, mask | ✅ (on_close, on_change, on_finish) |
| Tree | `tree` | tree_data, checkable, draggable, expanded_keys | ✅ (on_select, on_check, on_expand) |

### Feedback (`feedback.py`)

| antd | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- |
| Alert | `alert` | message, description, type, show_icon, closable, banner | on_close | ✅ |
| Drawer | `drawer` | open, title, placement, width, mask_closable | on_close | ✅ |
| Modal | `modal` | open, title, width, centered, confirm_loading, footer | on_ok, on_cancel | ✅ |
| Popconfirm | `popconfirm` | title, description, ok_text, placement | on_confirm, on_cancel | ✅ |
| Progress | `progress` | percent, type, status, steps, stroke_color | — | ✅ |
| Result | `result` | status, title, sub_title, icon, extra | — | ✅ |
| Skeleton / Button / Image | `skeleton` / `skeleton_button` / `skeleton_image` | active, loading, avatar, paragraph | — | ✅ |
| Spin | `spin` | spinning, size, tip, delay, fullscreen | — | ✅ |
| Watermark | `watermark` | content, rotate, gap, image, font | — | ✅ |
| message (imperative) | — | — | — | ⏳ Phase 6 |
| notification (imperative) | — | — | — | ⏳ Phase 6 |
| Modal.confirm (imperative) | — | — | — | ⏳ Phase 6 |

### Config (`base.py`)

| antd | Factory | Key props | Status |
| --- | --- | --- | --- |
| ConfigProvider | `config_provider` | theme, component_size, direction, locale | ✅ |
| App | `app` | component | ✅ |

### Out of scope (⛔)

`@ant-design/pro-components`, `@ant-design/charts`, `@ant-design/x` (AI), and
server-rendered locale bundles. Custom antd props not yet typed remain reachable
through `custom_attrs`.
