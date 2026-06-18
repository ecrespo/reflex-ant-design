"""reflex-ant-design demo app.

A single-page gallery that exercises a broad slice of the wrapped Ant Design
component set: general, layout, navigation, data entry, data display and
feedback. Everything is wrapped in a :func:`antd.config_provider` so the live
primary-color control re-themes the whole page.

Run it with::

    cd reflex_ant_design_demo
    reflex run
"""

from __future__ import annotations

import reflex as rx
from reflex_ant_design import antd, icon

from .state import DemoState

# ---------------------------------------------------------------------------
# Static data used by the data-display examples
# ---------------------------------------------------------------------------
COUNTRY_OPTIONS = [
    {"label": "United States", "value": "us"},
    {"label": "Spain", "value": "es"},
    {"label": "Venezuela", "value": "ve"},
    {"label": "Japan", "value": "jp"},
]

TABLE_COLUMNS = [
    {"title": "Name", "dataIndex": "name", "key": "name"},
    {"title": "Role", "dataIndex": "role", "key": "role"},
    {"title": "Status", "dataIndex": "status", "key": "status"},
]

TABLE_DATA = [
    {"key": "1", "name": "Ada Lovelace", "role": "Engineer", "status": "Active"},
    {"key": "2", "name": "Alan Turing", "role": "Researcher", "status": "Active"},
    {"key": "3", "name": "Grace Hopper", "role": "Admiral", "status": "Away"},
]

MENU_ITEMS = [
    {"key": "overview", "label": "Overview"},
    {"key": "team", "label": "Team"},
    {"key": "settings", "label": "Settings"},
]

STEP_ITEMS = [
    {"title": "Login", "description": "Authenticate"},
    {"title": "Verification", "description": "Confirm email"},
    {"title": "Done", "description": "All set"},
]

TIMELINE_ITEMS = [
    {"children": "Account created", "color": "green"},
    {"children": "First project added"},
    {"children": "Upgraded to Pro", "color": "blue"},
]


def section(title: str, *children: rx.Component) -> rx.Component:
    """A titled card wrapping one demo section."""
    return antd.card(
        antd.space(*children, direction="vertical", size="middle", style={"width": "100%"}),
        title=title,
        style={"marginBottom": "20px", "width": "100%"},
    )


def general_section() -> rx.Component:
    """Buttons, icons and typography."""
    return section(
        "General — Button, Icon, Typography",
        antd.space(
            antd.button("Primary", type="primary", icon=icon("CheckOutlined")),
            antd.button("Default"),
            antd.button("Dashed", type="dashed"),
            antd.button("Danger", danger=True),
            antd.button("Loading", loading=True),
            antd.button(icon=icon("SettingOutlined"), shape="circle"),
            wrap=True,
        ),
        antd.title("A heading", level=4),
        antd.text(
            "Some ",
            antd.text("strong", strong=True),
            " and ",
            antd.text("danger", type="danger"),
            " text.",
        ),
    )


def data_entry_section() -> rx.Component:
    """A small interactive form bound to state."""
    return section(
        "Data Entry — Input, Select, Switch, Slider, Rate, ColorPicker, DatePicker",
        antd.input(
            value=DemoState.name,
            on_change=DemoState.set_name,
            placeholder="Your name",
            prefix=icon("UserOutlined"),
            allow_clear=True,
        ),
        antd.text(DemoState.greeting, type="secondary"),
        antd.text_area(
            value=DemoState.bio,
            on_change=DemoState.set_bio,
            placeholder="Short bio",
            rows=2,
            show_count=True,
            max_length=120,
        ),
        antd.select(
            value=DemoState.country,
            on_change=DemoState.set_country,
            options=COUNTRY_OPTIONS,
            style={"width": "240px"},
        ),
        antd.space(
            antd.text("Newsletter"),
            antd.switch(checked=DemoState.newsletter, on_change=DemoState.toggle_newsletter),
        ),
        antd.slider(value=DemoState.volume, on_change=DemoState.set_volume, min=0, max=100),
        antd.rate(value=DemoState.rating, on_change=DemoState.set_rating, allow_half=True),
        antd.space(
            antd.color_picker(value=DemoState.color, on_change=DemoState.set_color, show_text=True),
            antd.date_picker(on_change=DemoState.set_birthday),
        ),
    )


def navigation_section() -> rx.Component:
    """Affix, Menu, tabs, steps, pagination, breadcrumb, dropdown."""
    return section(
        "Navigation — Affix, Menu, Tabs, Steps, Pagination, Dropdown",
        antd.affix(
            antd.button("Affixed (offset 8px)", type="dashed"),
            offset_top=8,
            on_change=DemoState.set_affixed,
        ),
        antd.breadcrumb(
            items=[{"title": "Home"}, {"title": "Library"}, {"title": "Ant Design"}],
        ),
        antd.menu(
            items=MENU_ITEMS,
            mode="horizontal",
            selected_keys=[DemoState.active_tab],
            on_select=lambda info: DemoState.set_active_tab(info["key"]),
        ),
        antd.tabs(
            items=[
                {"key": "overview", "label": "Overview", "children": "Overview content"},
                {"key": "team", "label": "Team", "children": "Team content"},
                {"key": "settings", "label": "Settings", "children": "Settings content"},
            ],
            active_key=DemoState.active_tab,
            on_change=DemoState.set_active_tab,
        ),
        antd.steps(items=STEP_ITEMS, current=DemoState.current_step),
        antd.space(
            antd.button("Prev", on_click=DemoState.set_step((DemoState.current_step - 1) % 3)),
            antd.button("Next", on_click=DemoState.set_step((DemoState.current_step + 1) % 3)),
        ),
        antd.dropdown(
            antd.button("Actions ", icon("DownOutlined")),
            menu={"items": [{"key": "1", "label": "Edit"}, {"key": "2", "label": "Delete"}]},
        ),
        antd.pagination(default_current=1, total=200),
    )


def data_display_section() -> rx.Component:
    """Table, statistic, tags, badges, avatar, timeline, calendar, progress."""
    return section(
        "Data Display — Table, Statistic, Tag, Badge, Avatar, Timeline, Calendar",
        antd.space(
            antd.statistic(title="Active Users", value=1128, prefix=icon("TeamOutlined")),
            antd.statistic(title="Revenue", value=93, suffix="%", precision=0),
            size="large",
        ),
        antd.space(
            antd.tag("default"),
            antd.tag("success", color="success"),
            antd.tag("processing", color="processing"),
            antd.tag("error", color="error"),
            antd.badge(antd.avatar(icon=icon("UserOutlined")), count=5),
            antd.avatar_group(
                antd.avatar(icon=icon("UserOutlined")),
                antd.avatar("AB"),
                antd.avatar(icon=icon("UserOutlined"), style={"backgroundColor": "#87d068"}),
            ),
            wrap=True,
        ),
        antd.table(columns=TABLE_COLUMNS, data_source=TABLE_DATA, pagination=False),
        antd.timeline(items=TIMELINE_ITEMS),
        antd.calendar(fullscreen=False, on_select=DemoState.set_selected_date),
        antd.progress(percent=DemoState.volume),
    )


def feedback_section() -> rx.Component:
    """Alert, modal, drawer, popconfirm, spin, result."""
    return section(
        "Feedback — Alert, Modal, Drawer, Popconfirm, Spin",
        antd.alert(
            message="Heads up",
            description="This is an informational alert with an icon.",
            type="info",
            show_icon=True,
        ),
        antd.space(
            antd.button("Open Modal", type="primary", on_click=DemoState.open_modal),
            antd.button("Open Drawer", on_click=DemoState.set_drawer(True)),
            antd.popconfirm(
                antd.button("Delete", danger=True),
                title="Delete this item?",
                description="This action cannot be undone.",
                ok_text="Yes",
                cancel_text="No",
            ),
        ),
        antd.spin(antd.text("  Loading content…"), spinning=True),
        antd.modal(
            antd.text("Modal body content goes here."),
            open=DemoState.modal_open,
            title="Confirm",
            on_ok=DemoState.close_modal,
            on_cancel=DemoState.close_modal,
        ),
        antd.drawer(
            antd.text("Drawer content slides in from the right."),
            open=DemoState.drawer_open,
            title="Details",
            on_close=DemoState.set_drawer(False),
        ),
    )


def theme_controls() -> rx.Component:
    """Live theming controls feeding the ConfigProvider."""
    return antd.card(
        antd.space(
            antd.text("Primary color:", strong=True),
            antd.color_picker(
                value=DemoState.primary_color,
                on_change=DemoState.set_primary_color,
                show_text=True,
            ),
            wrap=True,
        ),
        style={"marginBottom": "20px", "width": "100%"},
    )


def index() -> rx.Component:
    """The demo page, wrapped in a themed ConfigProvider + App."""
    return antd.config_provider(
        antd.app(
            rx.box(
                antd.title("reflex-ant-design", level=2),
                antd.paragraph(
                    "A gallery of Ant Design components wrapped for Reflex. "
                    "Change the primary color to re-theme everything below.",
                    type="secondary",
                ),
                theme_controls(),
                general_section(),
                data_entry_section(),
                navigation_section(),
                data_display_section(),
                feedback_section(),
                style={"maxWidth": "900px", "margin": "0 auto", "padding": "32px 16px"},
            ),
        ),
        theme=DemoState.theme_config,
    )


app = rx.App()
app.add_page(index, title="reflex-ant-design demo")
