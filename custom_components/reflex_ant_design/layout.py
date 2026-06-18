"""Layout components: Divider, Flex, Grid (Row/Col), Layout, Space, Splitter.

These arrange other components in space. Ant Design's 24-column grid lives in
``Row`` / ``Col``; ``Layout`` provides the page-level header/sider/content
scaffold; ``Flex`` and ``Space`` cover the common flexbox/spacing needs.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

from .base import AntdComponent, Size


# ---------------------------------------------------------------------------
# Divider
# ---------------------------------------------------------------------------
class Divider(AntdComponent):
    """``Divider`` -- a separator line, horizontal or vertical, with optional text."""

    tag = "Divider"

    type: Var[Literal["horizontal", "vertical"]]

    # Position of the inline title text.
    orientation: Var[Literal["left", "right", "center"]]

    # Make the line dashed.
    dashed: Var[bool]

    # ``solid`` | ``dashed`` | ``dotted``.
    variant: Var[Literal["dashed", "dotted", "solid"]]

    # Render a thinner, lighter divider.
    plain: Var[bool]

    size: Var[Size]


# ---------------------------------------------------------------------------
# Flex
# ---------------------------------------------------------------------------
class Flex(AntdComponent):
    """``Flex`` -- a thin, token-aware wrapper around CSS flexbox."""

    tag = "Flex"

    vertical: Var[bool]
    wrap: Var[Literal["nowrap", "wrap", "wrap-reverse"] | bool]
    justify: Var[str]
    align: Var[str]

    # Spacing between items: a size token or a pixel number.
    gap: Var[Size | int]

    flex: Var[str]
    component: Var[str]


# ---------------------------------------------------------------------------
# Grid: Row / Col
# ---------------------------------------------------------------------------
class Row(AntdComponent):
    """``Row`` -- a row in the 24-column responsive grid."""

    tag = "Row"

    # Horizontal arrangement of columns.
    justify: Var[
        Literal["start", "end", "center", "space-around", "space-between", "space-evenly"]
    ]

    # Vertical alignment of columns.
    align: Var[Literal["top", "middle", "bottom", "stretch"]]

    # Gutter (px), or [horizontal, vertical], or a responsive dict.
    gutter: Var[int | list[int] | dict]

    wrap: Var[bool]


class Col(AntdComponent):
    """``Col`` -- a column; ``span`` is out of 24."""

    tag = "Col"

    # Number of grid cells to occupy (0-24, 0 hides the column).
    span: Var[int]

    # Cells to the left of the column.
    offset: Var[int]

    # Raster order.
    order: Var[int]

    # Push/pull the column.
    push: Var[int]
    pull: Var[int]

    # Flex layout style for the column.
    flex: Var[str | int]

    # Responsive breakpoints (int span or a config dict).
    xs: Var[int | dict]
    sm: Var[int | dict]
    md: Var[int | dict]
    lg: Var[int | dict]
    xl: Var[int | dict]
    xxl: Var[int | dict]


# ---------------------------------------------------------------------------
# Layout: Layout / Header / Sider / Content / Footer
# ---------------------------------------------------------------------------
class Layout(AntdComponent):
    """``Layout`` -- page scaffold container (use with Header/Sider/Content/Footer)."""

    tag = "Layout"

    # Place a Sider beside the content (auto-detected, can be forced).
    has_sider: Var[bool]


class LayoutHeader(AntdComponent):
    """``Layout.Header`` -- the top bar of a layout."""

    tag = "Layout.Header"


class LayoutContent(AntdComponent):
    """``Layout.Content`` -- the main content area of a layout."""

    tag = "Layout.Content"


class LayoutFooter(AntdComponent):
    """``Layout.Footer`` -- the bottom bar of a layout."""

    tag = "Layout.Footer"


class LayoutSider(AntdComponent):
    """``Layout.Sider`` -- a collapsible side navigation panel."""

    tag = "Layout.Sider"

    # Controlled collapsed state.
    collapsed: Var[bool]

    # Initial collapsed state (uncontrolled).
    default_collapsed: Var[bool]

    # Allow collapsing.
    collapsible: Var[bool]

    # Width when expanded / collapsed.
    width: Var[int | str]
    collapsed_width: Var[int]

    # Where the collapse trigger sits; ``None`` hides it.
    reverse_arrow: Var[bool]

    # Responsive breakpoint to auto-collapse at.
    breakpoint: Var[Literal["xs", "sm", "md", "lg", "xl", "xxl"]]

    # Collapse style.
    collapse_type: Var[Literal["clickTrigger", "responsive"]]

    # Background theme.
    theme: Var[Literal["light", "dark"]]

    on_collapse: rx.EventHandler[lambda collapsed, type_: [collapsed, type_]]
    on_breakpoint: rx.EventHandler[lambda broken: [broken]]


# ---------------------------------------------------------------------------
# Space
# ---------------------------------------------------------------------------
class Space(AntdComponent):
    """``Space`` -- set consistent spacing between inline children."""

    tag = "Space"

    direction: Var[Literal["vertical", "horizontal"]]
    size: Var[Size | int | list[int]]
    align: Var[Literal["start", "end", "center", "baseline"]]
    wrap: Var[bool]

    # Add a separator between every child.
    split: Var[rx.Component]


class SpaceCompact(AntdComponent):
    """``Space.Compact`` -- merge adjacent form controls into one seamless group."""

    tag = "Space.Compact"

    direction: Var[Literal["vertical", "horizontal"]]
    size: Var[Size]
    block: Var[bool]


# ---------------------------------------------------------------------------
# Splitter (antd 5.21+)
# ---------------------------------------------------------------------------
class Splitter(AntdComponent):
    """``Splitter`` -- a resizable split-pane container."""

    tag = "Splitter"

    layout: Var[Literal["horizontal", "vertical"]]

    on_resize: rx.EventHandler[lambda sizes: [sizes]]
    on_resize_start: rx.EventHandler[lambda sizes: [sizes]]
    on_resize_end: rx.EventHandler[lambda sizes: [sizes]]


class SplitterPanel(AntdComponent):
    """``Splitter.Panel`` -- one pane of a :class:`Splitter`."""

    tag = "Splitter.Panel"

    # Default / min / max size (px or percentage string).
    default_size: Var[int | str]
    min: Var[int | str]
    max: Var[int | str]
    size: Var[int | str]
    resizable: Var[bool]
    collapsible: Var[bool | dict]


divider = Divider.create
flex = Flex.create
row = Row.create
col = Col.create
layout = Layout.create
header = LayoutHeader.create
content = LayoutContent.create
footer = LayoutFooter.create
sider = LayoutSider.create
space = Space.create
space_compact = SpaceCompact.create
splitter = Splitter.create
splitter_panel = SplitterPanel.create
