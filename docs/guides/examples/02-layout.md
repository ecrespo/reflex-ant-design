# Layout components

Structural building blocks from Ant Design wrapped for Reflex: dividers, flexbox
helpers, the 24-column grid, the page shell (`layout`/`header`/`sider`/...),
spacing utilities, and resizable splitters. Every example uses
`antd.<factory>(*children, **props)` with snake_case props and Reflex event
handlers.

## Contents

- [divider](#divider)
- [flex](#flex)
- [row / col (24-column grid)](#row--col-24-column-grid)
- [layout, header, content, footer](#layout-header-content-footer)
- [sider](#sider)
- [space](#space)
- [space_compact](#space_compact)
- [splitter / splitter_panel](#splitter--splitter_panel)
- [Full page scaffold](#full-page-scaffold)

## Setup

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

## divider

A separator line between sections of content. Pass optional inline text as the
child to render a titled divider.

```python
rx.fragment(
    rx.text("Section one"),
    antd.divider(),                                  # plain horizontal rule
    antd.divider("Details", orientation="left"),     # titled, title aligned left
    antd.divider(dashed=True, variant="dashed"),     # dashed line
    antd.divider("Plain", plain=True, size="small"),
    rx.text("Section two"),
)
```

Use `type="vertical"` to separate inline items (e.g. inside a row of links):

```python
rx.hstack(
    rx.link("Edit"),
    antd.divider(type="vertical"),
    rx.link("Delete"),
    antd.divider(type="vertical", variant="dotted"),
    rx.link("Share"),
)
```

## flex

A thin wrapper over CSS flexbox. Control direction with `vertical`, line-wrapping
with `wrap`, and main/cross-axis alignment with `justify` / `align`.

```python
antd.flex(
    antd.button("A"),
    antd.button("B"),
    antd.button("C"),
    justify="space-between",   # CSS justify-content
    align="center",            # CSS align-items
    gap="middle",              # small | middle | large | int (px)
    wrap="wrap",               # nowrap | wrap | wrap-reverse | bool
)
```

A vertical stack rendered as a `<section>` element via `component`:

```python
antd.flex(
    rx.heading("Title"),
    rx.text("Body copy"),
    vertical=True,
    gap=16,            # gap accepts a pixel int too
    flex="1",          # CSS flex shorthand on this container
    component="section",
)
```

## row / col (24-column grid)

`row` and `col` form Ant Design's responsive 24-column grid. `span` is out of 24;
`gutter` adds spacing between columns (`int`, `[horizontal, vertical]`, or a
responsive dict). `col` accepts per-breakpoint props (`xs`...`xxl`) for responsive
spans.

Basic three-up grid with a horizontal + vertical gutter:

```python
antd.row(
    antd.col(rx.box("1", bg="#e6f4ff", padding="16px"), span=8),
    antd.col(rx.box("2", bg="#e6f4ff", padding="16px"), span=8),
    antd.col(rx.box("3", bg="#e6f4ff", padding="16px"), span=8),
    gutter=[16, 16],          # [horizontal_px, vertical_px]
    justify="center",         # start|end|center|space-around|space-between|space-evenly
    align="middle",           # top|middle|bottom|stretch
)
```

Responsive layout: full width on phones, halves on tablets, thirds on desktops.
`offset` shifts a column right by N grid units. `gutter` can be a responsive dict.

```python
antd.row(
    antd.col(
        rx.box("Main", padding="24px", bg="#f0f5ff"),
        xs=24, sm=24, md=16, lg=18,    # breakpoint spans
    ),
    antd.col(
        rx.box("Aside", padding="24px", bg="#fff7e6"),
        xs=24, sm=24, md=8, lg=6,
    ),
    gutter={"xs": 8, "sm": 16, "md": 24, "lg": 32},
    wrap=True,
)
```

`order`, `push`, `pull`, and `flex` give finer control over a single column:

```python
antd.row(
    antd.col(rx.box("Renders second"), order=2, flex="auto"),
    antd.col(rx.box("Renders first"), order=1, flex="200px"),
)
```

## layout, header, content, footer

`layout` is the outer page shell. Its direct children are the structural slots:
`header`, `content`, `footer`, and `sider`. `header`/`content`/`footer` take no
special props and simply wrap their children.

```python
antd.layout(
    antd.header(rx.heading("My App", color="white")),
    antd.content(rx.text("Main page content goes here.")),
    antd.footer(rx.text("© 2026 Acme Inc."), text_align="center"),
)
```

Set `has_sider` so the layout arranges a sider beside the content horizontally
(useful when the sider is rendered via a computed/conditional child):

```python
antd.layout(
    antd.sider(rx.text("Nav")),
    antd.layout(
        antd.header(rx.heading("Dashboard")),
        antd.content(rx.text("Body")),
    ),
    has_sider=True,
)
```

## sider

A collapsible side panel for navigation. It can be controlled (`collapsed`),
uncontrolled (`default_collapsed`), and can auto-collapse at a responsive
`breakpoint`. `on_collapse` fires with the new collapsed state and the trigger
type; `on_breakpoint` fires when the breakpoint is crossed.

```python
class LayoutState(rx.State):
    collapsed: bool = False

    @rx.event
    def on_collapse(self, collapsed: bool, kind: str):
        # collapsed -> bool, kind -> "clickTrigger" | "responsive"
        self.collapsed = collapsed

    @rx.event
    def on_breakpoint(self, broken: bool):
        # broken -> True when below the configured breakpoint
        ...


antd.sider(
    rx.vstack(
        rx.link("Home"),
        rx.link("Reports"),
        rx.link("Settings"),
    ),
    collapsed=LayoutState.collapsed,
    collapsible=True,
    width=240,
    collapsed_width=64,
    breakpoint="lg",
    collapse_type="responsive",   # clickTrigger | responsive
    reverse_arrow=False,
    theme="dark",                 # light | dark
    on_collapse=LayoutState.on_collapse,
    on_breakpoint=LayoutState.on_breakpoint,
)
```

## space

Even spacing between a set of inline or stacked elements, with an optional
`split` component drawn between each child. Prefer `space` for spacing arbitrary
elements; prefer `flex` when you need full flexbox control (justify/align/wrap).

```python
antd.space(
    antd.button("Save"),
    antd.button("Cancel"),
    antd.button("Reset"),
    size="middle",          # small | middle | large | int | [int, int]
    align="center",         # start | end | center | baseline
)
```

Vertical direction with a divider drawn between items via `split`:

```python
antd.space(
    rx.text("Line one"),
    rx.text("Line two"),
    rx.text("Line three"),
    direction="vertical",
    size=12,
    split=antd.divider(type="vertical"),
    wrap=True,
)
```

### Flex vs Space

```python
# Space: simple uniform gaps, optional split between items.
antd.space(antd.button("A"), antd.button("B"), size="large")

# Flex: full control over distribution and cross-axis alignment.
antd.flex(
    antd.button("A"),
    antd.button("B"),
    justify="space-between",
    align="center",
    gap="large",
)
```

## space_compact

Merges adjacent form controls into a single connected group (shared borders, no
gaps) — ideal for an input paired with a button or select.

```python
antd.space_compact(
    antd.input(placeholder="Search…"),
    antd.button("Go", type="primary"),
    block=True,             # stretch to full width
)
```

Vertical, sized group of inputs:

```python
antd.space_compact(
    antd.input(placeholder="Street"),
    antd.input(placeholder="City"),
    direction="vertical",
    size="middle",          # small | middle | large
)
```

## splitter / splitter_panel

`splitter` lays out resizable panes; each pane is a `splitter_panel`. Resize
events (`on_resize`, `on_resize_start`, `on_resize_end`) receive the list of
panel sizes. Per-panel constraints come from `min` / `max` / `default_size` and
flags like `resizable` and `collapsible`.

```python
class SplitState(rx.State):
    sizes: list = []

    @rx.event
    def on_resize(self, sizes: list):
        # sizes -> list of current panel sizes (px or %), one per panel
        self.sizes = sizes


antd.splitter(
    antd.splitter_panel(
        rx.box("Left pane", padding="16px"),
        default_size="30%",
        min="20%",
        max="70%",
        collapsible=True,
    ),
    antd.splitter_panel(
        rx.box("Right pane", padding="16px"),
        resizable=True,
    ),
    layout="horizontal",       # horizontal | vertical
    on_resize=SplitState.on_resize,
    on_resize_end=SplitState.on_resize,
    height="320px",
)
```

A vertical splitter with a fixed-size, non-resizable top panel:

```python
antd.splitter(
    antd.splitter_panel(rx.text("Top"), size=120, resizable=False),
    antd.splitter_panel(rx.text("Bottom")),
    layout="vertical",
    height="400px",
)
```

## Full page scaffold

A complete shell combining `layout`, `header`, `sider`, `content`, and `footer`
with a collapsible navigation sider.

```python
class AppState(rx.State):
    collapsed: bool = False

    @rx.event
    def toggle(self, collapsed: bool, kind: str):
        # collapsed -> bool, kind -> "clickTrigger" | "responsive"
        self.collapsed = collapsed


def page() -> rx.Component:
    return antd.layout(
        antd.sider(
            rx.vstack(
                rx.link("Dashboard", color="white"),
                rx.link("Orders", color="white"),
                rx.link("Settings", color="white"),
                spacing="3",
                padding="16px",
            ),
            collapsible=True,
            collapsed=AppState.collapsed,
            breakpoint="lg",
            width=220,
            collapsed_width=64,
            theme="dark",
            on_collapse=AppState.toggle,
        ),
        antd.layout(
            antd.header(
                antd.flex(
                    rx.heading("Acme Admin", color="white"),
                    antd.button(icon("setting"), type="text"),
                    justify="space-between",
                    align="center",
                ),
                background="#001529",
            ),
            antd.content(
                antd.row(
                    antd.col(rx.box("Widget A", padding="24px"), xs=24, md=12),
                    antd.col(rx.box("Widget B", padding="24px"), xs=24, md=12),
                    gutter=[16, 16],
                ),
                padding="24px",
            ),
            antd.footer(
                rx.text("© 2026 Acme Inc."),
                text_align="center",
            ),
        ),
        has_sider=True,
        min_height="100vh",
    )
```

---

See also: [Usage guide](../usage.md) ·
[Component catalog](../../sdd/06-component-catalog.md)
