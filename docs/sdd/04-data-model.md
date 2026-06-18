# 04 — Data Model (type & serialization mapping)

For a component library, the "data model" is the **mapping between Python types
and the JS props/events** that cross the Reflex compile and runtime boundary.

## 1. Prop type mapping

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

## 2. Shared literal types (`base.py`)

```python
Size      = Literal["small", "middle", "large"]
Status    = Literal["success", "processing", "default", "error", "warning"]
Placement = Literal["top", "left", "right", "bottom"]
Variant   = Literal["outlined", "borderless", "filled", "underlined"]
```

These are reused across modules to keep enums consistent and self-documenting.

## 3. Event payload model

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

### Non-serializable values are filtered out

The `dayjs` object (DatePicker), the DOM event (`Input`), and the antd `Color`
object (ColorPicker) are **never** sent to the backend; the spec selects the
string/primitive instead. This is the core reason each event has an explicit
spec rather than forwarding the raw argument.

## 4. Structured prop shapes (reference)

These are the dict shapes used by data-driven props (validated by antd at
runtime, documented here for app developers):

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

## 5. State-binding pattern

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
