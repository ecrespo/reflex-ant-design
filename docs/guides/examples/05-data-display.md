# Data Display components

Usage examples for the **Data Display** components of `reflex-ant-design` (Ant
Design wrapped for Reflex). Most are **data-driven**: you pass `items`,
`columns`, `data_source`, or `tree_data` as plain Python lists of dicts and wire
state through Reflex event handlers. All examples assume:

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

## Contents

- [avatar](#avatar)
- [avatar_group](#avatar_group)
- [badge](#badge)
- [badge_ribbon](#badge_ribbon)
- [calendar](#calendar)
- [card](#card)
- [card_meta](#card_meta)
- [card_grid](#card_grid)
- [carousel](#carousel)
- [collapse](#collapse)
- [descriptions](#descriptions)
- [empty](#empty)
- [image](#image)
- [list_view](#list_view)
- [list_item](#list_item)
- [list_item_meta](#list_item_meta)
- [tooltip](#tooltip)
- [popover](#popover)
- [qr_code](#qr_code)
- [segmented](#segmented)
- [statistic](#statistic)
- [statistic_countdown](#statistic_countdown)
- [table](#table)
- [tag](#tag)
- [checkable_tag](#checkable_tag)
- [timeline](#timeline)
- [tour](#tour)
- [tree](#tree)

## avatar

Represents a user or entity with an image, an icon, or text initials. Pass `src`
for an image, or an `icon` component / text child as fallback.

```python
def avatars() -> rx.Component:
    return antd.space(
        # image avatar
        antd.avatar(src="https://i.pravatar.cc/64?img=1", alt="Ada", size="large"),
        # icon avatar (square)
        antd.avatar(icon=icon("UserOutlined"), shape="square", size=48),
        # text avatar; gap shrinks long initials to fit
        antd.avatar("AC", gap=4, size="middle"),
        # on_error fires (and should return True to keep the fallback) if src fails
        antd.avatar(
            src="https://example.com/missing.png",
            on_error=lambda: rx.console_log("avatar image failed"),
        ),
    )
```

`size` accepts `"small" | "middle" | "large"`, an int (px), or a responsive dict
like `{"xs": 24, "lg": 40}`.

## avatar_group

Stacks several `avatar(...)` children and collapses overflow into a `+N` avatar
with a popover. Children must be `antd.avatar(...)`.

```python
def team() -> rx.Component:
    return antd.avatar_group(
        antd.avatar(src="https://i.pravatar.cc/64?img=1"),
        antd.avatar(src="https://i.pravatar.cc/64?img=2"),
        antd.avatar(src="https://i.pravatar.cc/64?img=3"),
        antd.avatar("ZY"),
        antd.avatar(icon=icon("UserOutlined")),
        max_count=3,                     # show 3, collapse the rest into "+N"
        max_popover_placement="bottom",
        max_popover_trigger="hover",     # hover | focus | click
        size="large",
        shape="circle",
    )
```

## badge

Decorates a child element with a small count or status dot. The badged element is
the child.

```python
def badges() -> rx.Component:
    return antd.space(
        # numeric count over an icon
        antd.badge(
            icon("BellOutlined"),
            count=12,
            overflow_count=99,           # renders "99+" beyond this
            offset=[2, -2],
        ),
        # standalone status dot + text (no child)
        antd.badge(status="processing", text="Running", color="blue"),
        # red dot, no number
        antd.badge(antd.avatar(icon=icon("UserOutlined")), dot=True),
        # explicit zero
        antd.badge(antd.button("Inbox"), count=0, show_zero=True, size="small"),
    )
```

`count` also accepts a string (e.g. `"new"`) or a component. `status` is one of
`success | processing | default | error | warning`.

## badge_ribbon

A corner ribbon wrapped around any content (Ant Design's `Badge.Ribbon`). The
wrapped content is the child.

```python
def ribbon() -> rx.Component:
    return antd.badge_ribbon(
        antd.card("Pro plan", title="Plan"),  # wrapped content
        text="Hot",
        color="volcano",
        placement="end",                # start | end
    )
```

## calendar

A full or compact month/year calendar. Ant Design stores dates as dayjs objects,
but the wrapped events deliver an **ISO date string** (e.g. `"2026-06-18"`).

```python
class CalState(rx.State):
    selected: str = "2026-06-18"

    @rx.event
    def on_select(self, date: str):
        # date -> ISO string, e.g. "2026-06-21"
        self.selected = date

    @rx.event
    def on_panel_change(self, date: str, mode: str):
        # mode -> "month" | "year"
        rx.console_log([date, mode])


def compact_calendar() -> rx.Component:
    return rx.vstack(
        antd.calendar(
            fullscreen=False,            # compact card-sized calendar
            show_week=True,
            mode="month",
            on_select=CalState.on_select,
            # on_change also delivers an ISO date string
            on_change=lambda date: rx.console_log(date),
            on_panel_change=CalState.on_panel_change,
        ),
        rx.text(f"Selected: {CalState.selected}"),
    )
```

## card

A bordered content container with an optional title, `extra` slot, `cover` image,
and a body (the children).

```python
def product_card() -> rx.Component:
    return antd.card(
        # --- body children ---
        antd.card_meta(
            title="Wireless Headset",
            description="Noise-cancelling, 30h battery",
            avatar=antd.avatar(icon=icon("AudioOutlined")),
        ),
        # --- card props ---
        title="Featured",
        extra=antd.button("More", type="link"),
        cover=antd.image(
            src="https://picsum.photos/seed/headset/600/280",
            preview=False,
        ),
        hoverable=True,
        bordered=True,
        size="default",
        variant="outlined",              # outlined | borderless
        loading=False,
    )
```

A card with tabbed sections fires `on_tab_change(key)`:

```python
antd.card(
    rx.text("Tab body"),
    title="Stats",
    custom_attrs={
        "tabList": [
            {"key": "day", "tab": "Day"},
            {"key": "week", "tab": "Week"},
        ]
    },
    on_tab_change=lambda key: rx.console_log(key),
)
```

## card_meta

The avatar/title/description block used inside a `card` (Ant Design's
`Card.Meta`). See the [card](#card) example above.

```python
antd.card_meta(
    title="Ada Lovelace",
    description="First programmer",
    avatar=antd.avatar(src="https://i.pravatar.cc/64?img=5"),
)
```

## card_grid

A grid cell rendered inside a `card` body (Ant Design's `Card.Grid`). Place
multiple `card_grid` children directly in a `card`.

```python
def grid_card() -> rx.Component:
    return antd.card(
        antd.card_grid("Feature A", hoverable=True),
        antd.card_grid("Feature B", hoverable=True),
        antd.card_grid("Feature C", hoverable=False),
        title="Modules",
    )
```

## carousel

A rotating slideshow. Each child is a slide (commonly an `rx.box(...)`).

```python
def banner() -> rx.Component:
    slide = lambda label, bg: rx.box(
        rx.center(rx.heading(label, color="white")),
        height="180px",
        background=bg,
    )
    return antd.carousel(
        slide("Slide 1", "#364d79"),
        slide("Slide 2", "#5b8c00"),
        slide("Slide 3", "#722ed1"),
        autoplay=True,
        dots=True,
        dot_position="bottom",           # top | left | right | bottom
        effect="scrollx",                # scrollx | fade
        infinite=True,
        speed=500,
        arrows=True,
        draggable=True,
        # before_change -> (from_index, to_index); after_change -> current_index
        before_change=lambda frm, to: rx.console_log([frm, to]),
        after_change=lambda current: rx.console_log(current),
    )
```

## collapse

Accordion-style expandable panels driven by `items`. Each item has a `key`, a
`label`, and `children` (the panel body).

```python
class CollapseState(rx.State):
    active: list[str] = ["1"]

    @rx.event
    def on_change(self, keys: list[str]):
        self.active = keys


def faq() -> rx.Component:
    return antd.collapse(
        items=[
            {
                "key": "1",
                "label": "What is Reflex?",
                "children": rx.text("A pure-Python full-stack web framework."),
            },
            {
                "key": "2",
                "label": "Is it free?",
                "children": rx.text("Yes, open source."),
                "extra": icon("InfoCircleOutlined"),
            },
            {
                "key": "3",
                "label": "Disabled panel",
                "children": rx.text("Locked"),
                "collapsible": "disabled",
            },
        ],
        accordion=True,                  # only one panel open at a time
        active_key=CollapseState.active,
        bordered=True,
        size="middle",
        expand_icon_position="start",    # start | end
        # on_change -> the active key(s)
        on_change=CollapseState.on_change,
    )
```

## descriptions

A read-only table of label/value pairs. Pass `items` with `label`, `children`
(the value), and an optional `span`.

```python
def order_summary() -> rx.Component:
    return antd.descriptions(
        items=[
            {"label": "Order", "children": "#10293"},
            {"label": "Status", "children": antd.tag("Shipped", color="green")},
            {"label": "Customer", "children": "Ada Lovelace"},
            {"label": "Address", "children": "12 Analytical Ave", "span": 2},
            {"label": "Notes", "children": "Leave at door", "span": 3},
        ],
        title="Order summary",
        extra=antd.button("Edit", type="link"),
        bordered=True,
        column=3,                        # int, or responsive dict {"xs": 1, "lg": 3}
        size="middle",
        layout="horizontal",             # horizontal | vertical
        colon=True,
    )
```

## empty

A placeholder for "no data" states. Customize the `description` and optionally the
`image`.

```python
def no_results() -> rx.Component:
    return antd.empty(
        description="No matching records",
        image="https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg",
        image_style={"height": 80},
    )
```

## image

An image with a built-in fullscreen preview, lazy `placeholder`, and a `fallback`
shown when the source fails.

```python
def thumb() -> rx.Component:
    return antd.image(
        src="https://picsum.photos/seed/cat/200/120",
        alt="A cat",
        width=200,
        height=120,
        placeholder=True,
        fallback="https://via.placeholder.com/200x120?text=Unavailable",
        preview=True,                    # set a dict for advanced preview options
        on_error=lambda: rx.console_log("image load failed"),
    )
```

## list_view

Ant Design's `List`. Via the namespace it is `antd.list`; the flat factory is
`list_view` (renamed to avoid shadowing Python's built-in `list`). Provide a
`data_source`, then render each row with a `list_item` child. Combine with
`list_item_meta` for an avatar/title/description layout.

```python
from reflex_ant_design import antd, list_view  # antd.list  ==  list_view
```

```python
class FeedState(rx.State):
    data: list[dict] = [
        {"id": 1, "name": "Ada Lovelace", "summary": "Wrote the first algorithm."},
        {"id": 2, "name": "Alan Turing", "summary": "Defined computability."},
        {"id": 3, "name": "Grace Hopper", "summary": "Built the first compiler."},
    ]


def feed() -> rx.Component:
    return list_view(   # or antd.list(...)
        # render one list_item per element via rx.foreach
        rx.foreach(
            FeedState.data,
            lambda person: antd.list_item(
                antd.list_item_meta(
                    title=person["name"],
                    description=person["summary"],
                    avatar=antd.avatar(icon=icon("UserOutlined")),
                ),
                actions=[antd.button("View", type="link")],
            ),
        ),
        data_source=FeedState.data,
        bordered=True,
        size="default",
        item_layout="horizontal",        # horizontal | vertical
        split=True,
        pagination={"pageSize": 5},      # bool or a dict of pagination options
        header=rx.heading("People", size="4"),
        footer=rx.text("End of list"),
    )
```

## list_item

A single row inside a `list_view`. Use `actions` for trailing links/buttons and
`extra` for an aside (e.g. a thumbnail). See the [list_view](#list_view) example.

```python
antd.list_item(
    antd.list_item_meta(title="Item title", description="Item description"),
    actions=[antd.button("Edit", type="link"), antd.button("Delete", type="link")],
    extra=antd.image(src="https://picsum.photos/seed/x/120/80", width=120),
)
```

## list_item_meta

The avatar/title/description block inside a `list_item` (Ant Design's
`List.Item.Meta`). See the [list_view](#list_view) example.

```python
antd.list_item_meta(
    title="Grace Hopper",
    description="Built the first compiler.",
    avatar=antd.avatar(src="https://i.pravatar.cc/64?img=8"),
)
```

## tooltip

A small text bubble shown on hover/focus over its child element.

```python
def hint() -> rx.Component:
    return antd.tooltip(
        antd.button("Hover me"),         # the hovered element (child)
        title="Saves your changes",
        placement="top",                 # top | left | right | bottom | topLeft | ...
        trigger="hover",                 # str or list, e.g. ["hover", "focus"]
        color="geekblue",
        arrow=True,
        mouse_enter_delay=0.1,
        mouse_leave_delay=0.1,
        # on_open_change -> bool (visible state)
        on_open_change=lambda is_open: rx.console_log(is_open),
    )
```

## popover

Like `tooltip`, but with richer `content` (any component) in addition to `title`.
Inherits every `tooltip` prop.

```python
def info_popover() -> rx.Component:
    return antd.popover(
        antd.button("Details"),          # the trigger (child)
        title="Account",
        content=rx.vstack(
            rx.text("Plan: Pro"),
            rx.text("Seats: 5"),
            antd.button("Manage", type="link"),
        ),
        trigger="click",
        placement="bottomLeft",
        arrow=True,
    )
```

## qr_code

Renders a QR code for a string value, with optional center `icon` and a `status`
overlay (e.g. expired) plus an `on_refresh` action.

```python
def qr() -> rx.Component:
    return antd.qr_code(
        value="https://reflex.dev",
        type="canvas",                   # canvas | svg
        size=160,
        color="#000000",
        bg_color="#ffffff",
        bordered=True,
        error_level="M",                 # L | M | Q | H
        status="active",                 # active | expired | loading | scanned
        on_refresh=lambda: rx.console_log("regenerate QR"),
    )
```

## segmented

A single-select control rendered as a connected button group. Bind `value` to
state and update from `on_change`.

```python
class ViewState(rx.State):
    mode: str = "list"

    @rx.event
    def on_change(self, value: str):
        # value -> the selected option value
        self.mode = value


def view_switch() -> rx.Component:
    return antd.segmented(
        options=[
            {"label": "List", "value": "list", "icon": icon("BarsOutlined")},
            {"label": "Grid", "value": "grid", "icon": icon("AppstoreOutlined")},
            {"label": "Kanban", "value": "kanban"},
        ],
        value=ViewState.mode,
        size="middle",
        block=True,
        on_change=ViewState.on_change,
    )
```

`options` may also be a plain list of strings, e.g. `["Daily", "Weekly",
"Monthly"]`.

## statistic

Displays a single highlighted number with an optional title, prefix/suffix, and
precision.

```python
def stats_row() -> rx.Component:
    return antd.space(
        antd.statistic(
            title="Active Users",
            value=11_280,
            group_separator=",",
            prefix=icon("UserOutlined"),
        ),
        antd.statistic(
            title="Conversion",
            value=87.65,
            precision=2,
            suffix="%",
            value_style={"color": "#3f8600"},
        ),
        antd.statistic(title="Loading", value=0, loading=True),
        size="large",
    )
```

## statistic_countdown

A live countdown to a target time (Ant Design's `Statistic.Countdown`). Inherits
`statistic` props and adds a `format` plus `on_finish` / `on_change`.

```python
class TimerState(rx.State):
    # an absolute timestamp in ms (e.g. now + 1 hour)
    deadline: int = 1_750_000_000_000

    @rx.event
    def on_finish(self):
        rx.console_log("countdown finished")


def sale_timer() -> rx.Component:
    return antd.statistic_countdown(
        title="Sale ends in",
        value=TimerState.deadline,       # target time, ms since epoch
        format="HH:mm:ss",
        on_finish=TimerState.on_finish,
        # on_change -> remaining time value
        on_change=lambda remaining: rx.console_log(remaining),
    )
```

## table

A data grid driven by `columns` and `data_source`. Each row in `data_source`
needs a unique `"key"` (or set `row_key`). Column dicts use `dataIndex` to map to
a row field.

```python
class TableState(rx.State):
    rows: list[dict] = [
        {"key": "1", "name": "Ada", "age": 36, "role": "Engineer"},
        {"key": "2", "name": "Alan", "age": 41, "role": "Researcher"},
        {"key": "3", "name": "Grace", "age": 52, "role": "Admiral"},
    ]

    @rx.event
    def on_change(self, pagination: dict, filters: dict, sorter: dict):
        # called on sort/filter/page change
        rx.console_log([pagination, filters, sorter])


def people_table() -> rx.Component:
    return antd.table(
        columns=[
            {
                "title": "Name",
                "dataIndex": "name",
                "key": "name",
                "sorter": True,
                "fixed": "left",
            },
            {"title": "Age", "dataIndex": "age", "key": "age", "sorter": True},
            {
                "title": "Role",
                "dataIndex": "role",
                "key": "role",
                "filters": [
                    {"text": "Engineer", "value": "Engineer"},
                    {"text": "Researcher", "value": "Researcher"},
                ],
            },
        ],
        data_source=TableState.rows,
        row_key="key",
        bordered=True,
        size="middle",
        pagination={"pageSize": 10, "showSizeChanger": True},
        scroll={"x": 600},
        sticky=True,
        show_header=True,
        table_layout="auto",
        # row_selection / expandable accept dict configs
        row_selection={"type": "checkbox"},
        # on_change -> (pagination, filters, sorter)
        on_change=TableState.on_change,
    )
```

## tag

A small colored label, optionally `closable` and with a leading `icon`. The label
is the child.

```python
def tags() -> rx.Component:
    return antd.space(
        antd.tag("Default"),
        antd.tag("Success", color="success", icon=icon("CheckCircleOutlined")),
        antd.tag("Error", color="error", bordered=True),
        antd.tag(
            "Closable",
            color="blue",
            closable=True,
            # on_close fires when the close "x" is clicked
            on_close=lambda: rx.console_log("tag closed"),
        ),
    )
```

## checkable_tag

A tag that behaves like a checkbox (Ant Design's `Tag.CheckableTag`). Bind
`checked` to state and toggle in `on_change`.

```python
class FilterState(rx.State):
    selected: list[str] = ["Python"]

    @rx.event
    def toggle(self, label: str, checked: bool):
        # checked -> the new checked state (bool)
        if checked:
            self.selected = self.selected + [label]
        else:
            self.selected = [t for t in self.selected if t != label]


def topic_filters() -> rx.Component:
    return antd.space(
        *[
            antd.checkable_tag(
                label,
                checked=FilterState.selected.contains(label),
                on_change=lambda checked, label=label: FilterState.toggle(label, checked),
            )
            for label in ["Python", "Reflex", "Ant Design"]
        ]
    )
```

## timeline

A vertical sequence of events driven by `items`. Each item has `children` (the
content) and optional `color`, `dot`, `label`, and `position`.

```python
def history() -> rx.Component:
    return antd.timeline(
        items=[
            {"children": "Account created", "color": "green", "label": "09:00"},
            {"children": "Email verified", "color": "blue", "label": "09:05"},
            {
                "children": "Payment failed",
                "color": "red",
                "dot": icon("CloseCircleOutlined"),
                "label": "09:12",
            },
            {"children": "Retry scheduled", "color": "gray"},
        ],
        mode="left",                     # left | alternate | right
        pending="Syncing...",            # bool, str, or component for a trailing node
        reverse=False,
    )
```

## tour

A guided walkthrough that highlights target elements step by step. Bind `open`
and `current` to state.

```python
class TourState(rx.State):
    open: bool = False
    step: int = 0

    @rx.event
    def start(self):
        self.open = True
        self.step = 0

    @rx.event
    def on_change(self, current: int):
        self.step = current

    @rx.event
    def on_close(self, current: int):
        self.open = False

    @rx.event
    def on_finish(self):
        self.open = False


def onboarding_tour() -> rx.Component:
    return antd.tour(
        open=TourState.open,
        current=TourState.step,
        steps=[
            {"title": "Welcome", "description": "Let's take a quick tour."},
            {"title": "Search", "description": "Find anything from here."},
            {"title": "Profile", "description": "Manage your account.", "placement": "bottom"},
        ],
        type="primary",                  # default | primary
        arrow=True,
        mask=True,
        on_change=TourState.on_change,
        # on_close / on_finish -> current step index
        on_close=TourState.on_close,
        on_finish=TourState.on_finish,
    )
```

## tree

A hierarchical, optionally checkable tree driven by `tree_data` (nested dicts with
`title`, `key`, and `children`). Bind selected/checked/expanded keys to state.

```python
class TreeState(rx.State):
    checked: list[str] = ["src-app"]
    expanded: list[str] = ["src"]
    selected: list[str] = []

    @rx.event
    def on_check(self, checked_keys: list[str]):
        self.checked = checked_keys

    @rx.event
    def on_expand(self, expanded_keys: list[str]):
        self.expanded = expanded_keys

    @rx.event
    def on_select(self, selected_keys: list[str]):
        self.selected = selected_keys


def file_tree() -> rx.Component:
    return antd.tree(
        tree_data=[
            {
                "title": "src",
                "key": "src",
                "children": [
                    {"title": "app.py", "key": "src-app"},
                    {"title": "state.py", "key": "src-state"},
                ],
            },
            {
                "title": "assets",
                "key": "assets",
                "children": [
                    {"title": "logo.svg", "key": "assets-logo"},
                ],
            },
        ],
        checkable=True,
        selectable=True,
        multiple=True,
        show_line=True,
        checked_keys=TreeState.checked,
        expanded_keys=TreeState.expanded,
        selected_keys=TreeState.selected,
        # each handler receives the updated key list
        on_check=TreeState.on_check,
        on_expand=TreeState.on_expand,
        on_select=TreeState.on_select,
    )
```

> Need a prop that isn't wrapped? Pass it through `custom_attrs={...}`.

See also: [usage guide](../usage.md) and the
[component catalog](../../sdd/06-component-catalog.md).
