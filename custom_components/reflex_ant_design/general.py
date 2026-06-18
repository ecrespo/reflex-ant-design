"""General components: Button, FloatButton, Typography, Icon.

These are the building blocks of any Ant Design UI -- actions and text.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

from .base import ANTD_ICONS_VERSION, AntdComponent, Size

ButtonType = Literal["primary", "dashed", "link", "text", "default"]
ButtonShape = Literal["default", "circle", "round"]
ButtonHTMLType = Literal["submit", "reset", "button"]


# ---------------------------------------------------------------------------
# Button
# ---------------------------------------------------------------------------
class Button(AntdComponent):
    """``Button`` -- to trigger an operation.

    Ant Design defines five button types and three sizes/shapes, plus danger,
    ghost, block, loading and icon variants.
    """

    tag = "Button"

    # Visual style of the button.
    type: Var[ButtonType]

    # ``small`` | ``middle`` | ``large``.
    size: Var[Size]

    # ``default`` | ``circle`` | ``round``.
    shape: Var[ButtonShape]

    # Set the danger (destructive) color.
    danger: Var[bool]

    # Make the background transparent (for colored backgrounds).
    ghost: Var[bool]

    # Span the full width of its container.
    block: Var[bool]

    # Show a loading spinner (and disable interaction).
    loading: Var[bool]

    # Disable the button.
    disabled: Var[bool]

    # Render as an ``<a>`` with this href.
    href: Var[str]

    # Anchor target when ``href`` is set.
    target: Var[str]

    # Native button type when used inside a form.
    html_type: Var[ButtonHTMLType]

    # An icon component rendered before the children.
    icon: Var[rx.Component]

    # Position of the icon relative to the text.
    icon_position: Var[Literal["start", "end"]]

    # Auto-insert a space between two Chinese characters.
    auto_insert_space: Var[bool]

    on_click: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# FloatButton
# ---------------------------------------------------------------------------
class FloatButton(AntdComponent):
    """``FloatButton`` -- a floating action button pinned to the viewport."""

    tag = "FloatButton"

    # ``default`` | ``primary``.
    type: Var[Literal["default", "primary"]]

    # ``circle`` | ``square``.
    shape: Var[Literal["circle", "square"]]

    # Text shown inside a ``square`` float button.
    description: Var[str]

    # Tooltip content shown on hover.
    tooltip: Var[str]

    # An icon component.
    icon: Var[rx.Component]

    # Render as a link.
    href: Var[str]
    target: Var[str]

    # Attach a badge (dict, e.g. {"count": 5, "dot": True}).
    badge: Var[dict]

    on_click: rx.EventHandler[rx.event.no_args_event_spec]


class FloatButtonGroup(FloatButton):
    """``FloatButton.Group`` -- group several float buttons, optionally as a menu."""

    tag = "FloatButton.Group"

    # Expand the group on click/hover instead of always showing children.
    trigger: Var[Literal["click", "hover"]]

    # Controlled open state when ``trigger`` is set.
    open: Var[bool]

    on_open_change: rx.EventHandler[lambda open: [open]]


class BackTop(AntdComponent):
    """``FloatButton.BackTop`` -- scroll back to the top of the page."""

    tag = "FloatButton.BackTop"

    # Pixels scrolled before the button appears.
    visibility_height: Var[int]

    # Scroll target selector.
    target: Var[str]

    on_click: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
class _Typography(AntdComponent):
    """Shared props for the Typography family."""

    # Semantic color of the text.
    type: Var[Literal["secondary", "success", "warning", "danger"]]

    disabled: Var[bool]
    mark: Var[bool]
    code: Var[bool]
    keyboard: Var[bool]
    underline: Var[bool]
    delete: Var[bool]
    strong: Var[bool]
    italic: Var[bool]

    # Truncate with an ellipsis (bool or config dict).
    ellipsis: Var[bool | dict]

    # Make the text copyable (bool or config dict {"text": ..., "tooltips": ...}).
    copyable: Var[bool | dict]


class Typography(AntdComponent):
    """``Typography`` -- the wrapping article container for text blocks."""

    tag = "Typography"


class Title(_Typography):
    """``Typography.Title`` -- headings, level 1 through 5."""

    tag = "Typography.Title"

    # Heading level (h1..h5).
    level: Var[Literal[1, 2, 3, 4, 5]]


class Text(_Typography):
    """``Typography.Text`` -- inline text with rich formatting flags."""

    tag = "Typography.Text"


class Paragraph(_Typography):
    """``Typography.Paragraph`` -- a block of body text."""

    tag = "Typography.Paragraph"


class TypographyLink(_Typography):
    """``Typography.Link`` -- an anchor styled as antd text."""

    tag = "Typography.Link"

    href: Var[str]
    target: Var[str]


# ---------------------------------------------------------------------------
# Icon -- factory over @ant-design/icons
# ---------------------------------------------------------------------------
class _AntdIcon(AntdComponent):
    """Base for icons imported from ``@ant-design/icons``."""

    library = ANTD_ICONS_VERSION

    # Spin the icon continuously (useful for loading states).
    spin: Var[bool]

    # Rotate the icon by N degrees.
    rotate: Var[int]

    # The icons package has no stylesheet of its own.
    def _get_custom_code(self) -> str:
        return ""


# Cache generated icon classes so the same icon name reuses one class.
_ICON_CLASSES: dict[str, type[_AntdIcon]] = {}


def icon(name: str, **props) -> rx.Component:
    """Create an Ant Design icon by its export name.

    ``@ant-design/icons`` exports hundreds of icon components (``HomeOutlined``,
    ``SearchOutlined``, ``SettingFilled`` ...). This factory builds the wrapper
    for any of them on demand::

        icon("SearchOutlined")
        icon("HeartFilled", style={"color": "red", "fontSize": "20px"})

    Args:
        name: The exact export name from ``@ant-design/icons``.
        **props: Props forwarded to the icon (``style``, ``spin``, ``rotate``,
            ``on_click`` ...).

    Returns:
        A Reflex component rendering the requested icon.
    """
    cls = _ICON_CLASSES.get(name)
    if cls is None:
        cls = type(
            name,
            (_AntdIcon,),
            {"__module__": __name__, "__qualname__": name, "tag": name},
        )
        _ICON_CLASSES[name] = cls
    return cls.create(**props)


button = Button.create
float_button = FloatButton.create
float_button_group = FloatButtonGroup.create
back_top = BackTop.create
typography = Typography.create
title = Title.create
text = Text.create
paragraph = Paragraph.create
link = TypographyLink.create
