# General components

Buttons, floating action buttons, typography, and icons — the foundational
primitives from Ant Design's *General* category, wrapped for Reflex.

- [`button`](#button)
- [`float_button`](#float_button)
- [`float_button_group`](#float_button_group)
- [`back_top`](#back_top)
- [`typography`](#typography)
- [`title`](#title)
- [`text`](#text)
- [`paragraph`](#paragraph)
- [`link`](#link)
- [`icon`](#icon)

## button

The primary action trigger. `type`, `size`, and `shape` control appearance;
`danger`, `ghost`, `block`, `loading`, and `disabled` toggle states. Children are
the label text; `on_click` takes no arguments.

```python
import reflex as rx
from reflex_ant_design import antd, icon

antd.space(
    antd.button("Primary", type="primary"),
    antd.button("Dashed", type="dashed"),
    antd.button("Link", type="link"),
    antd.button("Text", type="text"),
    antd.button("Default"),            # type defaults to "default"
)
```

Sizes, shapes, and the danger flag:

```python
antd.space(
    antd.button("Small", size="small"),
    antd.button("Middle", size="middle"),
    antd.button("Large", size="large"),
    antd.button("Round", shape="round"),
    antd.button(icon=icon("SearchOutlined"), shape="circle"),  # icon-only circle
    antd.button("Delete", type="primary", danger=True),
    antd.button("Block", type="primary", block=True),          # full-width
)
```

An icon button with positioning. `icon` takes any `rx.Component` (use the `icon`
factory) and `icon_position` places it at `"start"` or `"end"`:

```python
antd.button(
    "Search",
    type="primary",
    icon=icon("SearchOutlined"),
    icon_position="start",
    on_click=rx.toast("Searching..."),
)
```

Wire `loading`/`disabled` to state to reflect an in-flight action:

```python
class S(rx.State):
    busy: bool = False

    @rx.event
    def submit(self):           # on_click passes no args
        self.busy = True
        yield
        # ...do work...
        self.busy = False

antd.button("Submit", type="primary", loading=S.busy, on_click=S.submit)
```

As a link, set `href`/`target`; as a form control, set `html_type`:

```python
antd.space(
    antd.button("Docs", type="link", href="https://ant.design", target="_blank"),
    antd.button("Save", type="primary", html_type="submit"),
    antd.button("Reset", html_type="reset"),
)
```

`auto_insert_space` controls the automatic space inserted between two CJK
characters in a label (defaults to enabled): `antd.button("登录", auto_insert_space=False)`.

## float_button

A fixed floating action button anchored to the viewport corner. Use `icon`,
`description`, and `tooltip` for content, `type`/`shape` for style, and `badge`
(a dict) for a count or dot indicator.

```python
antd.float_button(
    icon=icon("QuestionCircleOutlined"),
    type="primary",
    tooltip="Help",
    badge={"count": 5},
    on_click=rx.toast("Opened help"),
)
```

A square button with a description, or a link button:

```python
antd.float_button(
    icon=icon("CommentOutlined"),
    description="FAQ",
    shape="square",
    badge={"dot": True},
)
antd.float_button(icon=icon("FileTextOutlined"), href="/docs", target="_blank")
```

## float_button_group

Groups several `float_button` children into one expandable menu. `trigger`
chooses how it opens (`"click"` or `"hover"`); `open` plus `on_open_change`
make it controlled.

```python
class S(rx.State):
    fab_open: bool = False

    @rx.event
    def set_fab(self, is_open: bool):   # on_open_change passes the new open bool
        self.fab_open = is_open

antd.float_button_group(
    antd.float_button(icon=icon("EditOutlined"), tooltip="Edit"),
    antd.float_button(icon=icon("ShareAltOutlined"), tooltip="Share"),
    antd.float_button(icon=icon("DeleteOutlined"), tooltip="Delete"),
    trigger="click",
    icon=icon("PlusOutlined"),
    open=S.fab_open,
    on_open_change=S.set_fab,
)
```

## back_top

A scroll-to-top floating button (Ant Design's `FloatButton.BackTop`). It appears
once the page is scrolled past `visibility_height` pixels.

```python
antd.back_top(visibility_height=400, on_click=rx.toast("Back to top"))
```

Anchor scrolling to a specific scrollable element by CSS selector via `target`:

```python
antd.back_top(target="#scroll-container", visibility_height=200)
```

Combine it inside a group with other actions:

```python
antd.float_button_group(
    antd.float_button(icon=icon("CustomerServiceOutlined"), tooltip="Support"),
    antd.back_top(visibility_height=300),
    shape="circle",
)
```

## typography

A semantic container that wraps `title`, `text`, `paragraph`, and `link`
children. It carries no special props of its own — it groups and styles the
typographic elements inside it.

```python
antd.typography(
    antd.title("Release notes", level=2),
    antd.paragraph("Everything that changed in this version."),
    antd.text("Last updated June 2026", type="secondary"),
)
```

## title

A heading element. `level` (1–5) picks the heading size; the formatting flags
(`type`, `mark`, `code`, `strong`, `italic`, `underline`, `delete`, `keyboard`,
`disabled`) style the text. `ellipsis` truncates and `copyable` adds a copy button.

```python
antd.typography(
    antd.title("H1 heading", level=1),
    antd.title("Success heading", level=3, type="success"),
    antd.title("Copy me", level=4, copyable=True),
)
```

## text

Inline text with the same formatting flags as `title` (minus `level`). Combine
flags freely.

```python
antd.typography(
    antd.text("Default"),
    antd.text("Secondary", type="secondary"),
    antd.text("Warning", type="warning"),
    antd.text("Strong", strong=True),
    antd.text("Italic", italic=True),
    antd.text("Marked", mark=True),
    antd.text("code()", code=True),
    antd.text("Ctrl", keyboard=True),
    antd.text("Deleted", delete=True),
)
```

`copyable` and `ellipsis` also accept a dict for fine control:

```python
antd.space(
    antd.text("npm i reflex-ant-design", copyable={"tooltips": ["Copy", "Copied!"]}),
    antd.text("A very long single line of text...", ellipsis={"tooltip": True}),
    direction="vertical",
)
```

## paragraph

A block of body text. Shares the formatting flags of `text`, and its `ellipsis`
dict can clamp to multiple rows with an expand link.

```python
antd.typography(
    antd.paragraph("Standard paragraph copy goes here."),
    antd.paragraph(
        "A long multi-line paragraph that should clamp after two rows and offer "
        "an expand control to reveal the rest of the content.",
        ellipsis={"rows": 2, "expandable": True, "symbol": "more"},
    ),
)
```

## link

A typographic anchor. Adds `href` and `target` on top of the shared formatting
flags.

```python
antd.typography(
    antd.link("Ant Design", href="https://ant.design", target="_blank"),
    antd.link("Disabled link", href="https://ant.design", disabled=True),
    antd.link("Strong link", href="#", strong=True),
)
```

## icon

The `icon` factory renders any export from `@ant-design/icons`. Pass the icon's
export **name** as the first positional argument; `spin`, `rotate`, `style`, and
`on_click` are supported props.

```python
antd.space(
    icon("HomeOutlined"),
    icon("HeartFilled", style={"color": "red"}),
    icon("LoadingOutlined", spin=True),
    icon("UpOutlined", rotate=180),                 # rotated 180°
    icon("SettingOutlined", on_click=rx.toast("Settings")),
)
```

Icons double as the `icon=` prop of other components (button, float_button, etc.):

```python
antd.button("Add", type="primary", icon=icon("PlusOutlined"))
antd.float_button(icon=icon("CustomerServiceOutlined"), tooltip="Chat")
```

> Need a prop that isn't listed above? Pass it through the `custom_attrs={...}`
> escape hatch, e.g. `antd.button("X", custom_attrs={"data-testid": "save"})`.

---

See also: [`../usage.md`](../usage.md) and
[`../../sdd/06-component-catalog.md`](../../sdd/06-component-catalog.md).
