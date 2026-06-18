# 02 — API Spec (the public contract)

This is the contract a Reflex developer programs against. It must be complete
enough that an app developer can build a UI without reading the wrapper source.

## 1. Imports

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

## 2. Calling convention

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

## 3. Props contract

| Python form | antd form | Notes |
| --- | --- | --- |
| `type="primary"` | `type="primary"` | scalar passthrough |
| `allow_clear=True` | `allowClear={true}` | snake_case → camelCase |
| `options=[{"label","value"}]` | `options={[...]}` | list of dicts |
| `theme={"token": {...}}` | `theme={{token:{...}}}` | nested dict |
| `icon=icon("UserOutlined")` | `icon={<UserOutlined/>}` | component prop |
| `style={"width": "200px"}` | `style={{width:"200px"}}` | inline style dict |
| `custom_attrs={...}` | arbitrary attrs | escape hatch for unlisted props |

## 4. Event contract

Handlers receive a **serializable payload**, defined per component:

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
| Form | `on_finish` | `dict` (collected values) |
| Table | `on_change` | `(pagination, filters, sorter)` |

## 5. Theming & configuration

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

## 6. Compound components

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

## 7. The `icon()` factory

```python
icon(name: str, **props) -> rx.Component
```

`name` is any export of `@ant-design/icons` (`"SearchOutlined"`,
`"HeartFilled"`). Supports `spin`, `rotate`, `style`, `on_click`.

## 8. Stability

- Factory names and the documented props/events are the **stable surface**.
- Unlisted antd props are reachable via `custom_attrs` and are **not** part of
  the stability guarantee until promoted to a typed prop.
