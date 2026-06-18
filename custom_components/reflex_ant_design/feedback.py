"""Feedback components: alerts, dialogs, drawers and progress indicators.

Covers Alert, Drawer, Modal, Popconfirm, Progress, Result, Skeleton, Spin and
Watermark.

Ant Design also exposes imperative feedback APIs (``message``, ``notification``,
``Modal.confirm``) that are driven by React hooks. Those are best invoked from
custom JS; the component-style wrappers below cover the declarative cases that
map cleanly onto Reflex state. See ``docs/guides/usage.md``.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

from .base import AntdComponent, Placement, Size


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------
class Alert(AntdComponent):
    """``Alert`` -- a contextual feedback banner."""

    tag = "Alert"

    message: Var[str | rx.Component]
    description: Var[str | rx.Component]
    type: Var[Literal["success", "info", "warning", "error"]]
    show_icon: Var[bool]
    icon: Var[rx.Component]
    closable: Var[bool | dict]
    banner: Var[bool]
    action: Var[rx.Component]

    on_close: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Drawer
# ---------------------------------------------------------------------------
class Drawer(AntdComponent):
    """``Drawer`` -- a panel that slides in from a screen edge."""

    tag = "Drawer"

    open: Var[bool]
    title: Var[str | rx.Component]
    placement: Var[Placement]
    width: Var[int | str]
    height: Var[int | str]
    size: Var[Literal["default", "large"]]
    closable: Var[bool | dict]
    mask: Var[bool]
    mask_closable: Var[bool]
    keyboard: Var[bool]
    footer: Var[rx.Component]
    extra: Var[rx.Component]
    loading: Var[bool]
    destroy_on_hidden: Var[bool]

    on_close: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Modal
# ---------------------------------------------------------------------------
class Modal(AntdComponent):
    """``Modal`` -- a dialog overlay for focused tasks or confirmations."""

    tag = "Modal"

    open: Var[bool]
    title: Var[str | rx.Component]
    width: Var[int | str]
    centered: Var[bool]
    closable: Var[bool | dict]
    mask: Var[bool]
    mask_closable: Var[bool]
    keyboard: Var[bool]
    confirm_loading: Var[bool]
    ok_text: Var[str]
    cancel_text: Var[str]
    ok_type: Var[Literal["primary", "dashed", "link", "text", "default"]]
    footer: Var[rx.Component | bool]
    destroy_on_hidden: Var[bool]

    on_ok: rx.EventHandler[rx.event.no_args_event_spec]
    on_cancel: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Popconfirm
# ---------------------------------------------------------------------------
class Popconfirm(AntdComponent):
    """``Popconfirm`` -- an inline confirmation bubble before an action."""

    tag = "Popconfirm"

    title: Var[str | rx.Component]
    description: Var[str | rx.Component]
    ok_text: Var[str]
    cancel_text: Var[str]
    ok_type: Var[Literal["primary", "dashed", "link", "text", "default"]]
    icon: Var[rx.Component]
    placement: Var[str]
    disabled: Var[bool]
    open: Var[bool]

    on_confirm: rx.EventHandler[rx.event.no_args_event_spec]
    on_cancel: rx.EventHandler[rx.event.no_args_event_spec]
    on_open_change: rx.EventHandler[lambda open: [open]]


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------
class Progress(AntdComponent):
    """``Progress`` -- a line, circle or dashboard progress indicator."""

    tag = "Progress"

    percent: Var[int | float]
    type: Var[Literal["line", "circle", "dashboard"]]
    status: Var[Literal["success", "exception", "normal", "active"]]
    size: Var[Size | int | list[int]]
    show_info: Var[bool]
    steps: Var[int | dict]
    stroke_color: Var[str | dict | list]
    trail_color: Var[str]
    stroke_linecap: Var[Literal["round", "butt", "square"]]
    gap_degree: Var[int]
    success: Var[dict]


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------
class Result(AntdComponent):
    """``Result`` -- a full-page feedback state (success, error, 404 ...)."""

    tag = "Result"

    status: Var[
        Literal["success", "error", "info", "warning", "404", "403", "500"]
    ]
    title: Var[str | rx.Component]
    sub_title: Var[str | rx.Component]
    icon: Var[rx.Component]
    extra: Var[rx.Component]


# ---------------------------------------------------------------------------
# Skeleton
# ---------------------------------------------------------------------------
class Skeleton(AntdComponent):
    """``Skeleton`` -- a placeholder shown while content loads."""

    tag = "Skeleton"

    active: Var[bool]
    loading: Var[bool]
    avatar: Var[bool | dict]
    title: Var[bool | dict]
    paragraph: Var[bool | dict]
    round: Var[bool]


class SkeletonButton(AntdComponent):
    """``Skeleton.Button`` -- a button-shaped skeleton."""

    tag = "Skeleton.Button"

    active: Var[bool]
    size: Var[Size]
    shape: Var[Literal["circle", "round", "default", "square"]]
    block: Var[bool]


class SkeletonImage(AntdComponent):
    """``Skeleton.Image`` -- an image-shaped skeleton."""

    tag = "Skeleton.Image"

    active: Var[bool]


# ---------------------------------------------------------------------------
# Spin
# ---------------------------------------------------------------------------
class Spin(AntdComponent):
    """``Spin`` -- a loading spinner, optionally wrapping content."""

    tag = "Spin"

    spinning: Var[bool]
    size: Var[Size]
    tip: Var[str]
    delay: Var[int]
    percent: Var[int | Literal["auto"]]
    fullscreen: Var[bool]
    indicator: Var[rx.Component]


# ---------------------------------------------------------------------------
# Watermark
# ---------------------------------------------------------------------------
class Watermark(AntdComponent):
    """``Watermark`` -- overlay repeated text/image marks on content."""

    tag = "Watermark"

    content: Var[str | list[str]]
    width: Var[int]
    height: Var[int]
    rotate: Var[int]
    gap: Var[list[int]]
    offset: Var[list[int]]
    z_index: Var[int]
    image: Var[str]
    font: Var[dict]


alert = Alert.create
drawer = Drawer.create
modal = Modal.create
popconfirm = Popconfirm.create
progress = Progress.create
result = Result.create
skeleton = Skeleton.create
skeleton_button = SkeletonButton.create
skeleton_image = SkeletonImage.create
spin = Spin.create
watermark = Watermark.create
