# Usage guide

Practical patterns and gotchas for building with `reflex-ant-design`.

## Importing

```python
from reflex_ant_design import antd          # namespace (recommended)
from reflex_ant_design import button, table  # flat factories
from reflex_ant_design import icon           # icon factory
```

## Theming

Wrap your app once in `config_provider`:

```python
antd.config_provider(
    page(),
    theme={"token": {"colorPrimary": "#722ed1", "borderRadius": 8}},
    component_size="middle",
)
```

`theme` is a plain dict of antd design tokens. Make it a computed var to re-theme
from state:

```python
class S(rx.State):
    primary: str = "#1677ff"
    @rx.var
    def theme(self) -> dict:
        return {"token": {"colorPrimary": self.primary}}

antd.config_provider(page(), theme=S.theme)
```

### Dark mode (advanced)

The light/dark **algorithm** is an antd *function* (`theme.darkAlgorithm`), not
a string, so it can't be passed through a JSON dict. Provide it with custom code:

```python
class ThemedProvider(antd.config_provider.__self__.__class__):  # ConfigProvider subclass
    def add_imports(self):
        return {"antd": ["theme as antdTheme"]}
    # then inject `algorithm: antdTheme.darkAlgorithm` via add_custom_code / a JS helper
```

For most apps, setting `colorPrimary` and other tokens is enough; full dark-mode
algorithm switching is tracked in roadmap Phase 7.

## Binding inputs to state

Every interactive control follows the same shape:

```python
class S(rx.State):
    text: str = ""
    @rx.event
    def set_text(self, v: str): self.text = v

antd.input(value=S.text, on_change=S.set_text)
antd.text_area(value=S.text, on_change=S.set_text, rows=4)
antd.select(value=S.text, on_change=S.set_text, options=[...])
```

What the handler receives is documented per component in
[`docs/sdd/04-data-model.md`](../sdd/04-data-model.md). In short: text inputs →
`str`, value controls → the value, checkbox/radio → `bool`, pickers → date
string.

## Events with constant arguments

Bind arguments inline instead of writing one handler per value:

```python
antd.button("Open", on_click=S.set_open(True))
antd.button("Close", on_click=S.set_open(False))
antd.steps(items=STEPS, current=S.step)
antd.button("Next", on_click=S.set_step((S.step + 1) % len(STEPS)))
```

## Data-driven components

Tables, menus, selects, trees and timelines take lists of dicts you build in
Python:

```python
COLUMNS = [{"title": "Name", "dataIndex": "name", "key": "name"}]
antd.table(columns=COLUMNS, data_source=S.rows, pagination={"pageSize": 10})

antd.menu(items=[{"key": "home", "label": "Home"}], mode="inline",
          on_select=lambda info: S.select(info["key"]))
```

## Icons

```python
icon("SearchOutlined")
icon("HeartFilled", style={"color": "red", "fontSize": "20px"})
antd.button("Save", icon=icon("CheckOutlined"), type="primary")
```

Any export name from [`@ant-design/icons`](https://ant.design/components/icon)
works.

## Date & time pickers

Antd stores values as `dayjs` objects. The wrappers' `on_change` gives you the
**formatted string** (controlled by `format`):

```python
antd.date_picker(format="YYYY-MM-DD", on_change=S.set_date)   # -> "2026-06-17"
antd.range_picker(on_change=S.set_range)                       # -> ["...", "..."]
```

To set an initial value, pass a string matching `format` via `default_value`
plus `value_format` patterns (or drive it through custom code). Native
`date`/`datetime` conversion is roadmap Phase 7.

## Overlays (Modal, Drawer)

These are declarative — drive `open` from a bool in state:

```python
antd.button("Open", on_click=S.open_modal)
antd.modal(
    antd.text("Body"),
    open=S.modal_open, title="Confirm",
    on_ok=S.close_modal, on_cancel=S.close_modal,
)
```

## Imperative feedback (message / notification)

`message.success(...)`, `notification.open(...)` and `Modal.confirm(...)` are
imperative hook APIs and are **not** wrapped in 0.1.0 (roadmap Phase 6). Until
then, wrap the subtree in `antd.app(...)` and trigger them with a small custom
JS helper, or use Reflex's own `rx.toast`.

## Forms

`antd.form` manages its own field store; `on_finish` returns the collected
values dict:

```python
antd.form(
    antd.form_item(antd.input(), name="email", label="Email",
                   rules=[{"required": True, "message": "Required"}]),
    antd.form_item(antd.button("Submit", type="primary", html_type="submit")),
    on_finish=S.submit,   # receives {"email": "..."}
    layout="vertical",
)
```

For tight per-field two-way binding to Reflex state, `rx.form` with bound
`antd.input` controls can be simpler than antd's field store.

## Escape hatch for unlisted props

Any antd prop not yet typed is still reachable:

```python
antd.button("X", custom_attrs={"data-testid": "save", "rootClassName": "x"})
```
