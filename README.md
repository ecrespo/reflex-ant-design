# reflex-ant-design

[Ant Design](https://ant.design) (`antd`) wrapped as [Reflex](https://reflex.dev)
components — build enterprise-grade UIs in pure Python.

This is a Reflex **custom component** package. It exposes the Ant Design React
components (Button, Table, Form, DatePicker, Modal, and ~90 more) as Reflex
components you can drive entirely from Python state, with theming through
`ConfigProvider`.

> Status: **0.1.0 — alpha.** The API surface is broad and may still change.

## Installation

With **uv** (recommended):

```bash
uv add reflex-ant-design
```

With pip:

```bash
pip install reflex-ant-design
```

The `antd` npm package is installed automatically by Reflex the first time you
run your app.

## Quickstart

```python
import reflex as rx
from reflex_ant_design import antd, icon


class State(rx.State):
    name: str = ""

    @rx.event
    def set_name(self, value: str):
        self.name = value


def index() -> rx.Component:
    return antd.config_provider(
        antd.card(
            antd.space(
                antd.input(
                    value=State.name,
                    on_change=State.set_name,
                    placeholder="Your name",
                    prefix=icon("UserOutlined"),
                ),
                antd.button("Greet", type="primary", icon=icon("SmileOutlined")),
                antd.text(f"Hello!", strong=True),
                direction="vertical",
            ),
            title="reflex-ant-design",
        ),
        theme={"token": {"colorPrimary": "#722ed1", "borderRadius": 8}},
    )


app = rx.App()
app.add_page(index)
```

## Two ways to import

```python
# 1) Namespace (mirrors rx.*)
from reflex_ant_design import antd
antd.button("Save", type="primary")

# 2) Flat factories
from reflex_ant_design import button, table, date_picker
button("Save", type="primary")
```

## Examples

### Data table from state

```python
COLUMNS = [
    {"title": "Name", "dataIndex": "name", "key": "name"},
    {"title": "Role", "dataIndex": "role", "key": "role"},
]
DATA = [
    {"key": "1", "name": "Ada", "role": "Engineer"},
    {"key": "2", "name": "Alan", "role": "Researcher"},
]

antd.table(columns=COLUMNS, data_source=DATA, pagination={"pageSize": 5})
```

### Select bound to state

```python
antd.select(
    value=State.country,
    on_change=State.set_country,
    options=[{"label": "Spain", "value": "es"}, {"label": "Japan", "value": "jp"}],
    show_search=True,
    allow_clear=True,
)
```

### Modal driven by a boolean

```python
antd.button("Open", on_click=State.open_modal)
antd.modal(
    antd.text("Are you sure?"),
    open=State.modal_open,
    title="Confirm",
    on_ok=State.close_modal,
    on_cancel=State.close_modal,
)
```

### Theming

Wrap your app (or any subtree) in `config_provider` and pass design tokens:

```python
antd.config_provider(
    your_app(),
    theme={"token": {"colorPrimary": "#13c2c2", "borderRadius": 6}},
    component_size="large",
)
```

## Component catalog

| Category | Components |
| --- | --- |
| **General** | Button, FloatButton (+ Group, BackTop), Typography (Title/Text/Paragraph/Link), `icon()` |
| **Layout** | Divider, Flex, Row/Col, Layout (Header/Sider/Content/Footer), Space (+ Compact), Splitter |
| **Navigation** | Anchor, Breadcrumb, Dropdown (+ Button), Menu, Pagination, Steps, Tabs |
| **Data Entry** | Input (+ TextArea/Search/Password/OTP), InputNumber, Checkbox, Radio, Select, Switch, Slider, Rate, DatePicker, RangePicker, TimePicker, AutoComplete, Cascader, TreeSelect, Mentions, ColorPicker, Transfer, Upload, Form |
| **Data Display** | Avatar, Badge, Card, Carousel, Collapse, Descriptions, Empty, Image, List, Popover, Tooltip, QRCode, Segmented, Statistic, Table, Tag, Timeline, Tour, Tree |
| **Feedback** | Alert, Drawer, Modal, Popconfirm, Progress, Result, Skeleton, Spin, Watermark |
| **Config** | ConfigProvider, App |

See [`docs/guides/usage.md`](docs/guides/usage.md) for per-category notes and
the gotchas (date values, imperative `message`/`notification`, form binding).

## Try the demo

```bash
git clone https://github.com/ecrespo/reflex-ant-design
cd reflex-ant-design
make install
cd reflex_ant_design_demo && uv run reflex run
```

## Documentation

- [`docs/sdd`](docs/sdd) — the Spec-Driven Design docs (PRD, requirements,
  architecture, component catalog, roadmap, implementation plan).
- [`docs/guides/usage.md`](docs/guides/usage.md) — usage patterns and tips.
- [`docs/guides/compatibility.md`](docs/guides/compatibility.md) — antd / React
  / Reflex version matrix.

## Compatibility

- Reflex `>= 0.7`
- `antd@^6` (works with React 19 shipped by Reflex 0.7+). Pin `antd@^5` for apps
  on React 18 — see the compatibility guide.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © Ernesto Crespo
