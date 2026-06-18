# Configuration & theming

`ConfigProvider` and `App` are the global "Other" components from Ant Design.
Wrap your page once to set design tokens, default size, direction and locale.

- [config_provider](#config_provider) — global theme & defaults
- [app](#app) — static feedback context + reset styles
- [Computed theme from state](#computed-theme-from-state)
- [Per-component tokens](#per-component-tokens)
- [Dark mode](#dark-mode-advanced)

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

## config_provider

`antd.config_provider(*children, **props)` sets the theme and defaults for every
nested antd component.

Props: `theme` (dict of design tokens), `component_size` (`small`/`middle`/`large`),
`direction` (`ltr`/`rtl`), `prefix_cls` (str), `locale` (dict).

```python
antd.config_provider(
    antd.button("Primary", type="primary"),
    theme={
        "token": {"colorPrimary": "#722ed1", "borderRadius": 8},
    },
    component_size="large",   # default size for nested components
    direction="ltr",
)
```

`theme` is a plain dict of antd design tokens — it serializes cleanly and can be
a computed `rx.var` (see below). The most common token is `colorPrimary`.

## app

`antd.app(*children)` provides the context required by antd's static feedback
helpers and applies the reset styles to its subtree. Place it just **inside**
`config_provider`:

```python
def index() -> rx.Component:
    return antd.config_provider(
        antd.app(
            page_body(),
        ),
        theme={"token": {"colorPrimary": "#1677ff"}},
    )
```

## Computed theme from state

Derive the theme dict from state to re-theme reactively — e.g. a live color
picker that drives the whole app's primary color:

```python
class ThemeState(rx.State):
    primary: str = "#1677ff"

    @rx.event
    def set_primary(self, hex: str):    # color_picker on_change -> hex str
        self.primary = hex

    @rx.var
    def theme(self) -> dict:
        return {"token": {"colorPrimary": self.primary, "borderRadius": 8}}


def index() -> rx.Component:
    return antd.config_provider(
        antd.app(
            antd.space(
                antd.text("Primary color:"),
                antd.color_picker(
                    value=ThemeState.primary,
                    on_change=ThemeState.set_primary,
                    show_text=True,
                ),
                antd.button("Themed button", type="primary"),
            ),
        ),
        theme=ThemeState.theme,     # computed var -> live re-theme
    )
```

## Per-component tokens

Beyond global `token`, you can override tokens for individual components via the
`components` key:

```python
antd.config_provider(
    page(),
    theme={
        "token": {"colorPrimary": "#13c2c2"},
        "components": {
            "Button": {"controlHeight": 40},
            "Card": {"borderRadiusLG": 16},
        },
    },
)
```

## Dark mode (advanced)

The light/dark **algorithm** is an antd *function* (`theme.darkAlgorithm`), not a
string, so it cannot be passed through a JSON `theme` dict. For most apps,
setting `colorPrimary` and the other color tokens is enough. Full algorithm
switching needs a small custom-code step — see
[`../usage.md`](../usage.md#dark-mode-advanced). Native algorithm switching is
tracked in roadmap Phase 7.

## Escape hatch for unlisted props

Any antd prop not yet typed on these wrappers is still reachable:

```python
antd.config_provider(page(), custom_attrs={"componentDisabled": True})
```

---

See also: [`../usage.md`](../usage.md) ·
[`../../sdd/06-component-catalog.md`](../../sdd/06-component-catalog.md)
