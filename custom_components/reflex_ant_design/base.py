"""Base classes and shared types for the reflex-ant-design library.

Every wrapped Ant Design component inherits from :class:`AntdComponent`, which
declares the single npm dependency (``antd``) and injects the Ant Design reset
stylesheet exactly once into the compiled app.

Ant Design ships a large, well documented React component set. The wrappers in
this package follow a few consistent rules so the whole surface behaves
predictably from Python:

* ``library`` is pinned once here and inherited everywhere, so the npm version
  only changes when you change it on purpose.
* Compound components (``Input.TextArea``, ``Typography.Title``,
  ``Layout.Header`` ...) use a dot-qualified ``tag``. Reflex imports the
  left-most name (``Input``) and renders the member access (``Input.TextArea``).
* Event handlers are declared with :class:`reflex.EventHandler` and an explicit
  spec so the payload that reaches the Python backend is JSON-serializable.

See ``docs/sdd`` for the full specification and ``docs/guides`` for usage and
compatibility notes.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

# ---------------------------------------------------------------------------
# Pinned npm dependency. Keep in sync with docs/sdd and the README.
# ---------------------------------------------------------------------------
# antd v6 requires React >= 18 and works with the React 19 runtime shipped by
# Reflex >= 0.7. Apps still on React 18 can pin ``antd@^5.0.0`` instead -- the
# component API used by these wrappers is compatible across v5 and v6.
# See docs/guides/compatibility.md.
ANTD_VERSION = "antd@^6.0.0"

# Companion icon package, used by :mod:`reflex_ant_design.general` (Icon).
ANTD_ICONS_VERSION = "@ant-design/icons@^6.0.0"

# ---------------------------------------------------------------------------
# Shared literal types reused across many components.
# ---------------------------------------------------------------------------
Size = Literal["small", "middle", "large"]
Status = Literal["success", "processing", "default", "error", "warning"]
Placement = Literal["top", "left", "right", "bottom"]
Variant = Literal["outlined", "borderless", "filled", "underlined"]


class AntdComponent(rx.Component):
    """Base class for every Ant Design component wrapper.

    Declares the shared ``antd`` npm dependency and imports the reset
    stylesheet that Ant Design recommends including once at the app root.
    """

    # The npm package every wrapped component is imported from.
    library = ANTD_VERSION

    # Ant Design v5/v6 are CSS-in-JS, but still ship a small reset stylesheet
    # that normalizes the base element styles. Importing it here means it is
    # bundled exactly once regardless of how many antd components are used.
    def _get_custom_code(self) -> str:
        return 'import "antd/dist/reset.css";'


class AntdProvider(AntdComponent):
    """Base for context providers (``ConfigProvider``, ``App``).

    Identical to :class:`AntdComponent`; kept as a distinct type so providers
    can be detected and documented separately from leaf components.
    """


class ConfigProvider(AntdProvider):
    """``ConfigProvider`` -- global configuration and theming for antd.

    Wrap your app (or a subtree) to set the design tokens (primary color,
    border radius, ...), the component size, the text direction, and the
    locale. The ``theme`` prop accepts a dict with ``token``, ``components``
    and ``algorithm`` keys, mirroring the antd theming API.

    Example:
        config_provider(
            app_body(),
            theme={"token": {"colorPrimary": "#722ed1", "borderRadius": 8}},
        )
    """

    tag = "ConfigProvider"

    # Design tokens / component tokens / algorithm. e.g.
    # {"token": {"colorPrimary": "#1677ff"}, "algorithm": "darkAlgorithm"}.
    theme: Var[dict]

    # Default size applied to every nested component.
    component_size: Var[Size]

    # Layout direction.
    direction: Var[Literal["ltr", "rtl"]]

    # Global prefix for component class names.
    prefix_cls: Var[str]

    # Locale object (advanced: import from ``antd/locale/*``).
    locale: Var[dict]


class App(AntdProvider):
    """``App`` -- context wrapper for the static message/notification/modal helpers.

    Place it just inside :class:`ConfigProvider` so feedback components inherit
    the configured theme and the global reset styles apply to nested content.
    """

    tag = "App"

    # Apply the global reset styles to the wrapped DOM subtree.
    component: Var[str]


config_provider = ConfigProvider.create
app = App.create
