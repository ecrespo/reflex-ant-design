"""Data display components: how Ant Design presents information.

Avatar, Badge, Calendar, Card, Carousel, Collapse, Descriptions, Empty, Image,
List, Popover, QRCode, Segmented, Statistic, Table, Tag, Timeline, Tooltip,
Tour and Tree.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

from .base import AntdComponent, Placement, Size


# ---------------------------------------------------------------------------
# Avatar
# ---------------------------------------------------------------------------
class Avatar(AntdComponent):
    """``Avatar`` -- represent a user or thing with an image, icon or letters."""

    tag = "Avatar"

    src: Var[str]
    alt: Var[str]
    icon: Var[rx.Component]
    shape: Var[Literal["circle", "square"]]
    size: Var[Size | int | dict]
    gap: Var[int]
    src_set: Var[str]
    draggable: Var[bool]

    on_error: rx.EventHandler[rx.event.no_args_event_spec]


class AvatarGroup(AntdComponent):
    """``Avatar.Group`` -- overlap several avatars with a ``+N`` overflow."""

    tag = "Avatar.Group"

    max_count: Var[int]
    max_popover_placement: Var[Literal["top", "bottom"]]
    max_popover_trigger: Var[Literal["hover", "focus", "click"]]
    size: Var[Size | int]
    shape: Var[Literal["circle", "square"]]


# ---------------------------------------------------------------------------
# Badge
# ---------------------------------------------------------------------------
class Badge(AntdComponent):
    """``Badge`` -- a small count or status dot on the corner of an element."""

    tag = "Badge"

    count: Var[int | str | rx.Component]
    show_zero: Var[bool]
    overflow_count: Var[int]
    dot: Var[bool]
    status: Var[Literal["success", "processing", "default", "error", "warning"]]
    color: Var[str]
    text: Var[str]
    size: Var[Literal["default", "small"]]
    offset: Var[list[int]]
    title: Var[str]


class BadgeRibbon(AntdComponent):
    """``Badge.Ribbon`` -- a corner ribbon wrapped around content."""

    tag = "Badge.Ribbon"

    text: Var[str]
    color: Var[str]
    placement: Var[Literal["start", "end"]]


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------
class Card(AntdComponent):
    """``Card`` -- a flexible content container with header, body and actions."""

    tag = "Card"

    title: Var[str | rx.Component]
    extra: Var[str | rx.Component]
    size: Var[Literal["default", "small"]]
    bordered: Var[bool]
    hoverable: Var[bool]
    loading: Var[bool]
    cover: Var[rx.Component]
    type: Var[str]
    variant: Var[Literal["outlined", "borderless"]]

    on_tab_change: rx.EventHandler[lambda key: [key]]


class CardMeta(AntdComponent):
    """``Card.Meta`` -- a title/description/avatar block inside a Card."""

    tag = "Card.Meta"

    title: Var[str | rx.Component]
    description: Var[str | rx.Component]
    avatar: Var[rx.Component]


class CardGrid(AntdComponent):
    """``Card.Grid`` -- a grid cell inside a Card."""

    tag = "Card.Grid"

    hoverable: Var[bool]


# ---------------------------------------------------------------------------
# Carousel
# ---------------------------------------------------------------------------
class Carousel(AntdComponent):
    """``Carousel`` -- a rotating slideshow of content."""

    tag = "Carousel"

    autoplay: Var[bool | dict]
    dots: Var[bool | dict]
    dot_position: Var[Placement]
    effect: Var[Literal["scrollx", "fade"]]
    infinite: Var[bool]
    speed: Var[int]
    arrows: Var[bool]
    adaptive_height: Var[bool]
    draggable: Var[bool]

    after_change: rx.EventHandler[lambda current: [current]]
    before_change: rx.EventHandler[lambda from_, to: [from_, to]]


# ---------------------------------------------------------------------------
# Collapse
# ---------------------------------------------------------------------------
class Collapse(AntdComponent):
    """``Collapse`` -- show/hide regions of content (accordion optional)."""

    tag = "Collapse"

    # [{"key", "label", "children", "extra", "showArrow", "collapsible"}].
    items: Var[list[dict]]
    active_key: Var[str | list[str]]
    default_active_key: Var[str | list[str]]
    accordion: Var[bool]
    bordered: Var[bool]
    ghost: Var[bool]
    size: Var[Size]
    expand_icon_position: Var[Literal["start", "end"]]
    destroy_on_hidden: Var[bool]

    on_change: rx.EventHandler[lambda key: [key]]


# ---------------------------------------------------------------------------
# Descriptions
# ---------------------------------------------------------------------------
class Descriptions(AntdComponent):
    """``Descriptions`` -- display read-only field/value groups."""

    tag = "Descriptions"

    # [{"label", "children", "span"}].
    items: Var[list[dict]]
    title: Var[str | rx.Component]
    extra: Var[str | rx.Component]
    bordered: Var[bool]
    column: Var[int | dict]
    size: Var[Literal["default", "middle", "small"]]
    layout: Var[Literal["horizontal", "vertical"]]
    colon: Var[bool]


# ---------------------------------------------------------------------------
# Empty
# ---------------------------------------------------------------------------
class Empty(AntdComponent):
    """``Empty`` -- a placeholder for "no data"."""

    tag = "Empty"

    description: Var[str | rx.Component]
    image: Var[str]
    image_style: Var[dict]


# ---------------------------------------------------------------------------
# Image
# ---------------------------------------------------------------------------
class Image(AntdComponent):
    """``Image`` -- a previewable image with fallback and placeholder."""

    tag = "Image"

    src: Var[str]
    alt: Var[str]
    width: Var[int | str]
    height: Var[int | str]
    placeholder: Var[bool | rx.Component]
    fallback: Var[str]
    preview: Var[bool | dict]

    on_error: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------
class List(AntdComponent):
    """``List`` -- a versatile list with header, footer and pagination."""

    tag = "List"

    data_source: Var[list]
    bordered: Var[bool]
    size: Var[Literal["default", "large", "small"]]
    item_layout: Var[Literal["horizontal", "vertical"]]
    split: Var[bool]
    loading: Var[bool | dict]
    pagination: Var[bool | dict]
    grid: Var[dict]
    header: Var[rx.Component]
    footer: Var[rx.Component]


class ListItem(AntdComponent):
    """``List.Item`` -- a single row of a :class:`List`."""

    tag = "List.Item"

    actions: Var[list]
    extra: Var[rx.Component]


class ListItemMeta(AntdComponent):
    """``List.Item.Meta`` -- avatar/title/description block in a list row."""

    tag = "List.Item.Meta"

    title: Var[str | rx.Component]
    description: Var[str | rx.Component]
    avatar: Var[rx.Component]


# ---------------------------------------------------------------------------
# Popover / Tooltip
# ---------------------------------------------------------------------------
class Tooltip(AntdComponent):
    """``Tooltip`` -- a simple text tip shown on hover/focus."""

    tag = "Tooltip"

    title: Var[str | rx.Component]
    placement: Var[
        Literal[
            "top",
            "left",
            "right",
            "bottom",
            "topLeft",
            "topRight",
            "bottomLeft",
            "bottomRight",
            "leftTop",
            "leftBottom",
            "rightTop",
            "rightBottom",
        ]
    ]
    trigger: Var[str | list[str]]
    color: Var[str]
    open: Var[bool]
    arrow: Var[bool | dict]
    mouse_enter_delay: Var[float]
    mouse_leave_delay: Var[float]

    on_open_change: rx.EventHandler[lambda open: [open]]


class Popover(Tooltip):
    """``Popover`` -- a rich floating card triggered like a tooltip."""

    tag = "Popover"

    content: Var[str | rx.Component]


# ---------------------------------------------------------------------------
# QRCode
# ---------------------------------------------------------------------------
class QRCode(AntdComponent):
    """``QRCode`` -- render a QR code for a value."""

    tag = "QRCode"

    value: Var[str]
    type: Var[Literal["canvas", "svg"]]
    icon: Var[str]
    size: Var[int]
    color: Var[str]
    bg_color: Var[str]
    bordered: Var[bool]
    error_level: Var[Literal["L", "M", "Q", "H"]]
    status: Var[Literal["active", "expired", "loading", "scanned"]]

    on_refresh: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Segmented
# ---------------------------------------------------------------------------
class Segmented(AntdComponent):
    """``Segmented`` -- a segmented control (single-select button row)."""

    tag = "Segmented"

    value: Var[str | int]
    default_value: Var[str | int]
    options: Var[list[str] | list[dict]]
    size: Var[Size]
    block: Var[bool]
    disabled: Var[bool]
    vertical: Var[bool]

    on_change: rx.EventHandler[lambda value: [value]]


# ---------------------------------------------------------------------------
# Statistic
# ---------------------------------------------------------------------------
class Statistic(AntdComponent):
    """``Statistic`` -- display a single highlighted number."""

    tag = "Statistic"

    title: Var[str | rx.Component]
    value: Var[str | int | float]
    precision: Var[int]
    prefix: Var[str | rx.Component]
    suffix: Var[str | rx.Component]
    loading: Var[bool]
    value_style: Var[dict]
    group_separator: Var[str]


class StatisticCountdown(Statistic):
    """``Statistic.Countdown`` -- a live countdown to a target time."""

    tag = "Statistic.Countdown"

    format: Var[str]

    on_finish: rx.EventHandler[rx.event.no_args_event_spec]
    on_change: rx.EventHandler[lambda value: [value]]


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------
class Table(AntdComponent):
    """``Table`` -- the flagship data grid: sort, filter, paginate, select.

    ``columns`` and ``data_source`` are plain lists of dicts, so the whole
    table can be driven from Reflex state. Each column dict uses the antd keys
    (``title``, ``dataIndex``, ``key``, ``sorter``, ``filters``, ``fixed`` ...).
    """

    tag = "Table"

    columns: Var[list[dict]]
    data_source: Var[list[dict]]
    row_key: Var[str]
    bordered: Var[bool]
    loading: Var[bool | dict]
    size: Var[Literal["large", "middle", "small"]]
    pagination: Var[bool | dict]
    scroll: Var[dict]
    sticky: Var[bool | dict]
    show_header: Var[bool]
    table_layout: Var[Literal["auto", "fixed"]]
    row_selection: Var[dict]
    expandable: Var[dict]

    on_change: rx.EventHandler[
        lambda pagination, filters, sorter, extra: [pagination, filters, sorter]
    ]


# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------
class Tag(AntdComponent):
    """``Tag`` -- a small categorizing/labelling chip."""

    tag = "Tag"

    color: Var[str]
    closable: Var[bool]
    bordered: Var[bool]
    icon: Var[rx.Component]

    on_close: rx.EventHandler[rx.event.no_args_event_spec]


class CheckableTag(AntdComponent):
    """``Tag.CheckableTag`` -- a tag that behaves like a checkbox."""

    tag = "Tag.CheckableTag"

    checked: Var[bool]

    on_change: rx.EventHandler[lambda checked: [checked]]


# ---------------------------------------------------------------------------
# Timeline / Tour / Tree
# ---------------------------------------------------------------------------
class Timeline(AntdComponent):
    """``Timeline`` -- a vertical list of chronological events."""

    tag = "Timeline"

    # [{"children", "color", "dot", "label", "position"}].
    items: Var[list[dict]]
    mode: Var[Literal["left", "alternate", "right"]]
    pending: Var[bool | str | rx.Component]
    reverse: Var[bool]


class Tour(AntdComponent):
    """``Tour`` -- a guided, step-by-step product tour."""

    tag = "Tour"

    open: Var[bool]
    # [{"title", "description", "target", "placement"}].
    steps: Var[list[dict]]
    current: Var[int]
    type: Var[Literal["default", "primary"]]
    arrow: Var[bool | dict]
    mask: Var[bool | dict]

    on_close: rx.EventHandler[lambda current: [current]]
    on_change: rx.EventHandler[lambda current: [current]]
    on_finish: rx.EventHandler[rx.event.no_args_event_spec]


class Tree(AntdComponent):
    """``Tree`` -- a hierarchical tree with checkboxes, selection and drag."""

    tag = "Tree"

    tree_data: Var[list[dict]]
    checkable: Var[bool]
    selectable: Var[bool]
    multiple: Var[bool]
    draggable: Var[bool]
    show_line: Var[bool | dict]
    show_icon: Var[bool]
    block_node: Var[bool]
    default_expand_all: Var[bool]
    checked_keys: Var[list[str]]
    expanded_keys: Var[list[str]]
    selected_keys: Var[list[str]]

    on_select: rx.EventHandler[lambda selected_keys, info: [selected_keys]]
    on_check: rx.EventHandler[lambda checked_keys, info: [checked_keys]]
    on_expand: rx.EventHandler[lambda expanded_keys, info: [expanded_keys]]


avatar = Avatar.create
avatar_group = AvatarGroup.create
badge = Badge.create
badge_ribbon = BadgeRibbon.create
card = Card.create
card_meta = CardMeta.create
card_grid = CardGrid.create
carousel = Carousel.create
collapse = Collapse.create
descriptions = Descriptions.create
empty = Empty.create
image = Image.create
list_view = List.create
list_item = ListItem.create
list_item_meta = ListItemMeta.create
tooltip = Tooltip.create
popover = Popover.create
qr_code = QRCode.create
segmented = Segmented.create
statistic = Statistic.create
statistic_countdown = StatisticCountdown.create
table = Table.create
tag = Tag.create
checkable_tag = CheckableTag.create
timeline = Timeline.create
tour = Tour.create
tree = Tree.create
