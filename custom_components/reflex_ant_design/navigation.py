"""Navigation components: Anchor, Breadcrumb, Dropdown, Menu, Pagination, Steps, Tabs.

Ant Design v5+ favors a data-driven ``items`` prop (a list of dicts) over
nested child components for most of these. The wrappers expose both ``items``
and the relevant event handlers.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

from .base import AntdComponent, Size


# ---------------------------------------------------------------------------
# Anchor
# ---------------------------------------------------------------------------
class Anchor(AntdComponent):
    """``Anchor`` -- hyperlinks to scroll on a single page."""

    tag = "Anchor"

    # [{"key", "href", "title", "children": [...]}].
    items: Var[list[dict]]

    direction: Var[Literal["vertical", "horizontal"]]
    affix: Var[bool]
    offset_top: Var[int]
    bounds: Var[int]
    target_offset: Var[int]
    show_ink_in_fixed: Var[bool]

    on_change: rx.EventHandler[lambda current: [current]]
    on_click: rx.EventHandler[lambda e, link: [link]]


# ---------------------------------------------------------------------------
# Breadcrumb
# ---------------------------------------------------------------------------
class Breadcrumb(AntdComponent):
    """``Breadcrumb`` -- the current location within a hierarchy."""

    tag = "Breadcrumb"

    # [{"title", "href", "menu": {...}}].
    items: Var[list[dict]]

    separator: Var[str]


# ---------------------------------------------------------------------------
# Dropdown
# ---------------------------------------------------------------------------
class Dropdown(AntdComponent):
    """``Dropdown`` -- a floating menu triggered by a child element."""

    tag = "Dropdown"

    # Menu config: {"items": [...], "selectable": bool, ...}.
    menu: Var[dict]

    # ``hover`` | ``click`` | ``contextMenu`` (list allowed).
    trigger: Var[list[Literal["click", "hover", "contextMenu"]]]

    placement: Var[
        Literal[
            "bottom",
            "bottomLeft",
            "bottomRight",
            "top",
            "topLeft",
            "topRight",
        ]
    ]

    disabled: Var[bool]
    arrow: Var[bool | dict]
    open: Var[bool]

    on_open_change: rx.EventHandler[lambda open: [open]]


class DropdownButton(Dropdown):
    """``Dropdown.Button`` -- a button with an attached dropdown trigger."""

    tag = "Dropdown.Button"

    type: Var[Literal["primary", "dashed", "link", "text", "default"]]
    size: Var[Size]
    loading: Var[bool]

    on_click: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
class Menu(AntdComponent):
    """``Menu`` -- a versatile vertical/horizontal/inline navigation menu."""

    tag = "Menu"

    # [{"key", "label", "icon", "children": [...], "type": "group"|"divider"}].
    items: Var[list[dict]]

    mode: Var[Literal["vertical", "horizontal", "inline"]]
    theme: Var[Literal["light", "dark"]]

    # Controlled / default selection and expansion.
    selected_keys: Var[list[str]]
    default_selected_keys: Var[list[str]]
    open_keys: Var[list[str]]
    default_open_keys: Var[list[str]]

    multiple: Var[bool]
    selectable: Var[bool]
    inline_collapsed: Var[bool]
    inline_indent: Var[int]

    on_select: rx.EventHandler[lambda info: [info]]
    on_deselect: rx.EventHandler[lambda info: [info]]
    on_open_change: rx.EventHandler[lambda open_keys: [open_keys]]
    on_click: rx.EventHandler[lambda info: [info]]


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
class Pagination(AntdComponent):
    """``Pagination`` -- page through a long list of data."""

    tag = "Pagination"

    current: Var[int]
    default_current: Var[int]
    total: Var[int]
    page_size: Var[int]
    default_page_size: Var[int]
    page_size_options: Var[list[int]]

    size: Var[Literal["default", "small"]]
    simple: Var[bool]
    disabled: Var[bool]
    show_size_changer: Var[bool]
    show_quick_jumper: Var[bool | dict]
    show_total: Var[bool]
    hide_on_single_page: Var[bool]
    responsive: Var[bool]

    on_change: rx.EventHandler[lambda page, page_size: [page, page_size]]
    on_show_size_change: rx.EventHandler[lambda current, size: [current, size]]


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------
class Steps(AntdComponent):
    """``Steps`` -- guide a user through a sequence of tasks."""

    tag = "Steps"

    # [{"title", "description", "subTitle", "status", "icon", "disabled"}].
    items: Var[list[dict]]

    current: Var[int]
    initial: Var[int]
    direction: Var[Literal["horizontal", "vertical"]]
    label_placement: Var[Literal["horizontal", "vertical"]]
    size: Var[Literal["default", "small"]]
    status: Var[Literal["wait", "process", "finish", "error"]]
    percent: Var[int]
    progress_dot: Var[bool]
    type: Var[Literal["default", "navigation", "inline"]]
    responsive: Var[bool]

    on_change: rx.EventHandler[lambda current: [current]]


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
class Tabs(AntdComponent):
    """``Tabs`` -- switch between views in the same context."""

    tag = "Tabs"

    # [{"key", "label", "children", "disabled", "icon", "closable"}].
    items: Var[list[dict]]

    active_key: Var[str]
    default_active_key: Var[str]

    type: Var[Literal["line", "card", "editable-card"]]
    size: Var[Size]
    tab_position: Var[Literal["top", "right", "bottom", "left"]]
    centered: Var[bool]
    animated: Var[bool | dict]
    hide_add: Var[bool]
    tab_bar_gutter: Var[int]
    destroy_on_hidden: Var[bool]

    on_change: rx.EventHandler[lambda active_key: [active_key]]
    on_tab_click: rx.EventHandler[lambda key, event: [key]]
    on_edit: rx.EventHandler[lambda target_key, action: [target_key, action]]


anchor = Anchor.create
breadcrumb = Breadcrumb.create
dropdown = Dropdown.create
dropdown_button = DropdownButton.create
menu = Menu.create
pagination = Pagination.create
steps = Steps.create
tabs = Tabs.create
