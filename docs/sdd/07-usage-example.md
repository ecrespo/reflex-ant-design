# 07 — Usage Example (worked end-to-end)

A complete, runnable example: a small **user dashboard** that uses components
from every category, bound to Reflex state, and themed with `ConfigProvider`.
This is the canonical "how do I use this library" reference. The shipped demo
app (`reflex_ant_design_demo/`) is a larger version of the same idea.

## The app

```python
# dashboard.py
import reflex as rx
from reflex_ant_design import antd, icon


class DashboardState(rx.State):
    # form fields
    name: str = ""
    role: str = "engineer"
    active: bool = True
    # overlay flags
    drawer_open: bool = False
    # theme
    primary: str = "#1677ff"

    @rx.event
    def set_name(self, v: str):
        self.name = v

    @rx.event
    def set_role(self, v: str):
        self.role = v

    @rx.event
    def set_active(self, v: bool):
        self.active = v

    @rx.event
    def set_drawer(self, v: bool):
        self.drawer_open = v

    @rx.event
    def set_primary(self, v: str):
        self.primary = v

    @rx.var
    def theme(self) -> dict:
        return {"token": {"colorPrimary": self.primary, "borderRadius": 8}}


ROLE_OPTIONS = [
    {"label": "Engineer", "value": "engineer"},
    {"label": "Designer", "value": "designer"},
    {"label": "Manager", "value": "manager"},
]

COLUMNS = [
    {"title": "Name", "dataIndex": "name", "key": "name"},
    {"title": "Role", "dataIndex": "role", "key": "role"},
    {"title": "Status", "dataIndex": "status", "key": "status"},
]

ROWS = [
    {"key": "1", "name": "Ada Lovelace", "role": "Engineer", "status": "Active"},
    {"key": "2", "name": "Grace Hopper", "role": "Manager", "status": "Away"},
]


def stats_row() -> rx.Component:
    return antd.row(
        antd.col(antd.statistic(title="Users", value=1128, prefix=icon("TeamOutlined")), span=8),
        antd.col(antd.statistic(title="Active", value=87, suffix="%"), span=8),
        antd.col(antd.statistic(title="Revenue", value=9280, prefix="$"), span=8),
        gutter=16,
    )


def profile_form() -> rx.Component:
    return antd.card(
        antd.space(
            antd.input(
                value=DashboardState.name,
                on_change=DashboardState.set_name,
                placeholder="Full name",
                prefix=icon("UserOutlined"),
                allow_clear=True,
            ),
            antd.select(
                value=DashboardState.role,
                on_change=DashboardState.set_role,
                options=ROLE_OPTIONS,
                style={"width": "100%"},
            ),
            antd.space(
                antd.text("Active"),
                antd.switch(checked=DashboardState.active, on_change=DashboardState.set_active),
            ),
            antd.button(
                "View details",
                type="primary",
                icon=icon("EyeOutlined"),
                on_click=DashboardState.set_drawer(True),
            ),
            direction="vertical",
            style={"width": "100%"},
        ),
        title="Profile",
    )


def team_table() -> rx.Component:
    return antd.card(
        antd.table(columns=COLUMNS, data_source=ROWS, pagination=False),
        title="Team",
    )


def index() -> rx.Component:
    return antd.config_provider(
        antd.app(
            rx.box(
                antd.title("Dashboard", level=2),
                antd.space(
                    antd.text("Primary color:"),
                    antd.color_picker(
                        value=DashboardState.primary,
                        on_change=DashboardState.set_primary,
                        show_text=True,
                    ),
                ),
                stats_row(),
                antd.row(
                    antd.col(profile_form(), span=10),
                    antd.col(team_table(), span=14),
                    gutter=16,
                    style={"marginTop": "16px"},
                ),
                antd.drawer(
                    antd.descriptions(
                        items=[
                            {"label": "Name", "children": DashboardState.name},
                            {"label": "Role", "children": DashboardState.role},
                        ],
                        bordered=True,
                        column=1,
                    ),
                    open=DashboardState.drawer_open,
                    title="User details",
                    on_close=DashboardState.set_drawer(False),
                ),
                style={"maxWidth": "1000px", "margin": "0 auto", "padding": "32px"},
            ),
        ),
        theme=DashboardState.theme,
    )


app = rx.App()
app.add_page(index)
```

## Run it

```bash
reflex init        # if starting a new app
reflex run
```

## What this demonstrates

| Concept | Where |
| --- | --- |
| Theming the whole tree | `config_provider(theme=DashboardState.theme)` |
| Computed theme from state | `@rx.var def theme` + live `color_picker` |
| Two-way input binding | `input(value=..., on_change=...)` |
| Value-first events | `select`, `switch` `on_change` |
| Event with a bound argument | `on_click=DashboardState.set_drawer(True)` |
| Data-driven components | `table(columns=..., data_source=...)`, `descriptions(items=...)` |
| Layout grid | `row`/`col` with `gutter` and `span` |
| Composition | `statistic` inside `col` inside `row` |
| Overlay driven by a bool | `drawer(open=DashboardState.drawer_open)` |
| Icons | `icon("UserOutlined")` as a prop and as button content |

## Patterns to copy

1. **Bind, don't poll.** Give every control a `value` from state and an
   `on_change` that writes back.
2. **Compute props with `rx.var`.** The theme dict is derived from state so the
   UI re-themes reactively.
3. **Pass bound event args** (`set_drawer(True)`) instead of writing a separate
   handler for each constant.
4. **Keep data in Python.** `columns`, `options`, `items` are plain lists of
   dicts you can build, filter and sort in your state.
