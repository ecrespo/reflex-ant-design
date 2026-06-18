# Navigation components

Usage examples for the **Navigation** components of `reflex-ant-design` (Ant Design
wrapped for Reflex). These components are mostly **data-driven**: you pass `items`
as plain Python lists of dicts and wire selection/state through Reflex event
handlers. All examples assume:

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

## Contents

- [affix](#affix)
- [anchor](#anchor)
- [breadcrumb](#breadcrumb)
- [dropdown](#dropdown)
- [dropdown_button](#dropdown_button)
- [menu](#menu)
- [pagination](#pagination)
- [steps](#steps)
- [tabs](#tabs)

## affix

Pins its child element to the viewport as the page scrolls. (Ant Design lists
*Affix* under "Other", but it's grouped here.) The child is the element to pin.

```python
def affixed_button() -> rx.Component:
    return antd.affix(
        antd.button("Pinned to top", type="primary"),
        offset_top=24,                  # px from the top once pinned
        # on_change fires with a bool: True when the element becomes affixed
        on_change=lambda affixed: rx.console_log(affixed),
    )
```

You can also pin to the bottom with `offset_bottom`:

```python
antd.affix(
    antd.button("Stays at bottom"),
    offset_bottom=16,
)
```

## anchor

A floating set of in-page links that highlights the section currently in view.
Pass a nested `items` list; each item needs a `key`, an `href` (the anchor target)
and a `title`, and may nest `children`.

```python
def page_anchor() -> rx.Component:
    return antd.anchor(
        items=[
            {"key": "intro", "href": "#intro", "title": "Introduction"},
            {
                "key": "api",
                "href": "#api",
                "title": "API",
                "children": [
                    {"key": "props", "href": "#props", "title": "Props"},
                    {"key": "events", "href": "#events", "title": "Events"},
                ],
            },
            {"key": "faq", "href": "#faq", "title": "FAQ"},
        ],
        affix=True,             # stick to the viewport while scrolling
        offset_top=80,
        bounds=5,
        target_offset=80,
        show_ink_in_fixed=True,
        # on_change -> the currently active link (str), e.g. "#api"
        on_change=lambda link: rx.console_log(link),
        # on_click -> the clicked link
        on_click=lambda link: rx.console_log(link),
    )
```

Use `direction="horizontal"` for a top-bar style anchor.

## breadcrumb

Shows the path to the current page. Pass `items` as a list of dicts with a `title`
and optional `href`; an item may include a `menu` dict to render a dropdown.

```python
def crumbs() -> rx.Component:
    return antd.breadcrumb(
        items=[
            {"title": "Home", "href": "/"},
            {"title": "Catalog", "href": "/catalog"},
            {
                "title": "Phones",
                "menu": {  # dropdown attached to this crumb
                    "items": [
                        {"key": "ios", "label": "iOS"},
                        {"key": "android", "label": "Android"},
                    ]
                },
            },
            {"title": "Model X"},  # current page, no href
        ],
        separator=">",
    )
```

## dropdown

Wraps a trigger element (e.g. a button) and shows a floating menu. The menu is a
plain dict (`{"items": [...]}`); the child is the trigger.

```python
def actions_dropdown() -> rx.Component:
    return antd.dropdown(
        antd.button("Actions ", icon("DownOutlined")),  # the trigger element
        menu={
            "items": [
                {"key": "edit", "label": "Edit"},
                {"key": "duplicate", "label": "Duplicate"},
                {"type": "divider"},
                {"key": "delete", "label": "Delete", "danger": True},
            ]
        },
        trigger=["click"],          # click | hover | contextMenu
        placement="bottomLeft",
        arrow=True,
        # on_open_change -> bool (open state)
        on_open_change=lambda is_open: rx.console_log(is_open),
    )
```

Controlled open state from a Reflex var:

```python
class DropdownState(rx.State):
    is_open: bool = False

    @rx.event
    def set_open(self, value: bool):
        self.is_open = value


antd.dropdown(
    antd.button("Menu"),
    menu={"items": [{"key": "a", "label": "Item A"}]},
    open=DropdownState.is_open,
    on_open_change=DropdownState.set_open,
)
```

## dropdown_button

Like `dropdown`, but renders a split button: a main action button plus a dropdown
arrow. It accepts every `dropdown` prop and adds `type`, `size`, `loading`, and an
`on_click` for the main button.

```python
def save_split_button() -> rx.Component:
    return antd.dropdown_button(
        "Save",                      # main button label
        menu={
            "items": [
                {"key": "draft", "label": "Save as draft"},
                {"key": "template", "label": "Save as template"},
            ]
        },
        type="primary",
        size="middle",
        loading=False,
        placement="bottomRight",
        # on_click -> the main (left) button press
        on_click=lambda: rx.console_log("primary save clicked"),
    )
```

## menu

A vertical, horizontal, or inline menu driven by `items`. Each item carries a
`key`, a `label`, an optional `icon`, and may nest `children` (submenus) or use
`"type": "group"` / `"type": "divider"`. Handlers receive an **info dict**; read
the chosen key via `info["key"]`.

```python
class MenuState(rx.State):
    selected: list[str] = ["dashboard"]
    open_keys: list[str] = ["reports"]

    @rx.event
    def on_select(self, info: dict):
        # info -> {"key": ..., "keyPath": [...], "selectedKeys": [...], ...}
        self.selected = [info["key"]]

    @rx.event
    def on_open_change(self, open_keys: list[str]):
        self.open_keys = open_keys


def side_menu() -> rx.Component:
    return antd.menu(
        items=[
            {"key": "dashboard", "label": "Dashboard", "icon": icon("DashboardOutlined")},
            {
                "key": "reports",
                "label": "Reports",
                "icon": icon("BarChartOutlined"),
                "children": [
                    {"key": "daily", "label": "Daily"},
                    {"key": "weekly", "label": "Weekly"},
                ],
            },
            {"type": "divider"},
            {
                "type": "group",
                "label": "Account",
                "children": [
                    {"key": "profile", "label": "Profile"},
                    {"key": "logout", "label": "Logout"},
                ],
            },
        ],
        mode="inline",
        theme="light",
        inline_indent=24,
        # bind selection + open submenus to state
        selected_keys=MenuState.selected,
        open_keys=MenuState.open_keys,
        on_select=MenuState.on_select,
        on_open_change=MenuState.on_open_change,
        # on_click also fires with an info dict on every item click
        on_click=lambda info: rx.console_log(info),
    )
```

A horizontal top navbar that collapses when there's no room:

```python
antd.menu(
    items=[
        {"key": "home", "label": "Home"},
        {"key": "products", "label": "Products"},
        {"key": "about", "label": "About"},
    ],
    mode="horizontal",
    default_selected_keys=["home"],
)
```

Set `multiple=True` to allow multi-select, `selectable=False` for a pure action
menu, and `inline_collapsed=True` to show only icons.

## pagination

Page navigation for lists and tables. Bind `current` to state and update it from
`on_change`.

```python
class PageState(rx.State):
    page: int = 1
    page_size: int = 10

    @rx.event
    def on_change(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

    @rx.event
    def on_size_change(self, current: int, size: int):
        self.page_size = size


def list_pagination() -> rx.Component:
    return antd.pagination(
        current=PageState.page,
        page_size=PageState.page_size,
        total=485,
        page_size_options=[10, 20, 50, 100],
        size="default",
        show_size_changer=True,
        show_quick_jumper=True,
        show_total=True,
        responsive=True,
        # on_change -> (page, page_size)
        on_change=PageState.on_change,
        # on_show_size_change -> (current, size)
        on_show_size_change=PageState.on_size_change,
    )
```

A compact, simple pager:

```python
antd.pagination(
    default_current=1,
    total=50,
    simple=True,
    size="small",
    hide_on_single_page=True,
)
```

## steps

A progress indicator for multi-step flows. Drive `current` from state and combine
it with prev/next buttons for a wizard.

```python
class WizardState(rx.State):
    current: int = 0

    @rx.event
    def next_step(self):
        self.current += 1

    @rx.event
    def prev_step(self):
        self.current -= 1

    @rx.event
    def go_to(self, step: int):
        # on_change -> the clicked step index
        self.current = step


def checkout_wizard() -> rx.Component:
    return rx.vstack(
        antd.steps(
            items=[
                {"title": "Cart", "description": "Review items"},
                {"title": "Shipping", "description": "Address & method"},
                {"title": "Payment", "description": "Card details"},
                {"title": "Done", "description": "Confirmation"},
            ],
            current=WizardState.current,
            direction="horizontal",
            label_placement="vertical",
            size="default",
            on_change=WizardState.go_to,
        ),
        antd.space(
            antd.button(
                "Previous",
                on_click=WizardState.prev_step,
                disabled=WizardState.current <= 0,
            ),
            antd.button(
                "Next",
                type="primary",
                on_click=WizardState.next_step,
                disabled=WizardState.current >= 3,
            ),
        ),
        spacing="4",
    )
```

`steps` also supports `status`, `percent`, `progress_dot=True`, and
`type="navigation"` / `"inline"` variants. Per-item `status` (`wait` / `process` /
`finish` / `error`), `subTitle`, `icon`, and `disabled` are read from each dict.

## tabs

Tabbed content driven by `items`. Each item has a `key`, a `label`, and `children`
(its panel). Use `active_key` + `on_change` for a controlled component.

```python
class TabState(rx.State):
    active: str = "overview"

    @rx.event
    def set_active(self, key: str):
        self.active = key


def profile_tabs() -> rx.Component:
    return antd.tabs(
        items=[
            {"key": "overview", "label": "Overview", "children": rx.text("Overview panel")},
            {
                "key": "settings",
                "label": "Settings",
                "icon": icon("SettingOutlined"),
                "children": rx.text("Settings panel"),
            },
            {"key": "billing", "label": "Billing", "children": rx.text("Billing panel"), "disabled": True},
        ],
        active_key=TabState.active,
        type="line",
        size="middle",
        tab_position="top",
        centered=False,
        animated=True,
        tab_bar_gutter=24,
        # on_change -> the new active_key (str)
        on_change=TabState.set_active,
        # on_tab_click -> the clicked key (str)
        on_tab_click=lambda key: rx.console_log(key),
    )
```

Editable card tabs (add/close), where `on_edit` receives the affected key and the
action (`"add"` or `"remove"`):

```python
antd.tabs(
    items=[
        {"key": "1", "label": "Tab 1", "children": rx.text("One"), "closable": True},
        {"key": "2", "label": "Tab 2", "children": rx.text("Two"), "closable": True},
    ],
    type="editable-card",
    hide_add=False,
    default_active_key="1",
    destroy_on_hidden=True,
    # on_edit -> (target_key, action)
    on_edit=lambda target_key, action: rx.console_log([target_key, action]),
)
```

> Need a prop that isn't wrapped? Pass it through `custom_attrs={...}`.

See also: [usage guide](../usage.md) and the
[component catalog](../../sdd/06-component-catalog.md).
