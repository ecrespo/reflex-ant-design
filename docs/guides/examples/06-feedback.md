# Feedback components

Usage examples for the **Feedback** components of `reflex-ant-design` (Ant Design
wrapped for Reflex). Overlays (`modal`, `drawer`) are **declarative**: drive their
`open` prop from a bool in state and toggle it with `@rx.event` setters or inline
bound args like `S.set_open(True)`. All examples assume:

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

## Contents

- [alert](#alert)
- [modal](#modal)
- [drawer](#drawer)
- [popconfirm](#popconfirm)
- [progress](#progress)
- [result](#result)
- [skeleton](#skeleton) (+ skeleton_button, skeleton_image)
- [spin](#spin)
- [watermark](#watermark)
- [Imperative feedback (message / notification)](#imperative-feedback-message--notification)

## alert

A static, inline status banner. Set `type` to pick the color/semantics, `show_icon`
for the leading glyph, `closable` to let users dismiss it, and `banner` for the
full-width page-top style.

```python
def alert_types() -> rx.Component:
    return rx.vstack(
        antd.alert(message="Success! Your changes were saved.", type="success", show_icon=True),
        antd.alert(message="Heads up, this is informational.", type="info", show_icon=True),
        antd.alert(message="Warning: quota almost reached.", type="warning", show_icon=True),
        antd.alert(message="Error: could not connect.", type="error", show_icon=True),
        spacing="3",
    )
```

A closable alert with a description and an action button. `on_close` receives no
args:

```python
def alert_with_action() -> rx.Component:
    return antd.alert(
        message="Subscription expiring",
        description="Your plan renews in 3 days. Update your payment method to avoid interruption.",
        type="warning",
        show_icon=True,
        closable=True,                       # or a dict, e.g. {"closeIcon": icon("CloseOutlined")}
        action=antd.button("Renew now", type="primary", size="small"),
        # on_close -> no args; fires after the user dismisses the alert
        on_close=lambda: rx.console_log("alert closed"),
    )
```

The `banner` variant renders edge-to-edge at the top of a page:

```python
antd.alert(
    message="Scheduled maintenance tonight 02:00–03:00 UTC.",
    type="info",
    banner=True,
)
```

`message` and `description` also accept `rx.Component` values, and you can supply a
custom `icon=icon("BellOutlined")` when `show_icon=True`.

## modal

A centered dialog overlay. It is declarative: bind `open` to a state bool and toggle
it from a button. `on_ok` and `on_cancel` receive no args.

```python
class ModalState(rx.State):
    open: bool = False

    @rx.event
    def confirm(self):
        # on_ok -> no args; do the work, then close
        self.open = False

    @rx.event
    def cancel(self):
        # on_cancel -> no args; also fires on mask click / Esc
        self.open = False


def basic_modal() -> rx.Component:
    return rx.fragment(
        antd.button("Open modal", type="primary", on_click=ModalState.set_open(True)),
        antd.modal(
            rx.text("Are you sure you want to publish this draft?"),  # children = modal body
            open=ModalState.open,
            title="Publish draft",
            centered=True,
            width=520,
            ok_text="Publish",
            cancel_text="Keep editing",
            ok_type="primary",
            mask_closable=True,
            keyboard=True,                   # Esc closes
            destroy_on_hidden=True,
            on_ok=ModalState.confirm,
            on_cancel=ModalState.cancel,
        ),
    )
```

Use `confirm_loading=True` while an async ok-handler runs, or pass `footer=False`
(or a custom `rx.Component`) to replace the default OK/Cancel buttons.

## drawer

A panel that slides in from an edge of the screen. Like `modal`, it is declarative;
`on_close` receives no args and fires on the close icon, the mask, or Esc.

```python
class DrawerState(rx.State):
    open: bool = False

    @rx.event
    def close(self):
        # on_close -> no args
        self.open = False


def settings_drawer() -> rx.Component:
    return rx.fragment(
        antd.button("Open settings", on_click=DrawerState.set_open(True)),
        antd.drawer(
            rx.vstack(                       # children = drawer body
                rx.text("Notification preferences"),
                antd.switch(default_checked=True),
                spacing="3",
            ),
            open=DrawerState.open,
            title="Settings",
            placement="right",               # top | left | right | bottom
            width=420,
            size="default",                  # default | large
            closable=True,
            mask=True,
            mask_closable=True,
            keyboard=True,
            destroy_on_hidden=True,
            extra=antd.button("Save", type="primary", size="small"),
            footer=rx.text("Changes apply immediately."),
            on_close=DrawerState.close,
        ),
    )
```

Use `placement="bottom"` with `height=300` for a bottom sheet, and `loading=True` to
show a skeleton while the body content is fetched.

## popconfirm

A small confirmation bubble anchored to its trigger element — ideal for guarding a
destructive action. The child is the trigger (e.g. a button); `on_confirm` and
`on_cancel` receive no args.

```python
class RowState(rx.State):
    @rx.event
    def delete_item(self):
        # on_confirm -> no args
        return rx.toast("Item deleted")


def delete_with_confirm() -> rx.Component:
    return antd.popconfirm(
        antd.button("Delete", danger=True, icon=icon("DeleteOutlined")),  # the trigger
        title="Delete this item?",
        description="This action cannot be undone.",
        ok_text="Yes, delete",
        cancel_text="Cancel",
        ok_type="primary",
        icon=icon("QuestionCircleOutlined"),
        placement="topRight",
        on_confirm=RowState.delete_item,
        on_cancel=lambda: rx.console_log("cancelled"),
        # on_open_change -> bool (whether the bubble is open)
        on_open_change=lambda is_open: rx.console_log(is_open),
    )
```

Set `disabled=True` to fall through to the trigger's own `on_click` without showing
the bubble, or drive `open` from state for a fully controlled popover.

## progress

A progress indicator. Switch the look with `type` (`line` / `circle` / `dashboard`).

```python
def progress_examples() -> rx.Component:
    return rx.vstack(
        # line (default)
        antd.progress(percent=60, status="active", stroke_color="#1677ff"),
        antd.progress(percent=100, status="success"),
        antd.progress(percent=70, status="exception"),
        # circle
        antd.progress(percent=75, type="circle", size=120),
        # dashboard with a gradient stroke
        antd.progress(
            percent=90,
            type="dashboard",
            gap_degree=90,
            stroke_color={"0%": "#108ee9", "100%": "#87d068"},
        ),
        # stepped progress bar
        antd.progress(percent=80, steps=5, size="small", stroke_color="#52c41a"),
        spacing="4",
    )
```

Bind `percent` to a state var to animate it, hide the label with `show_info=False`,
and use `success={"percent": 30}` to render a secondary "success" segment.

## result

A full-page status block for the outcome of an operation. `status` sets the icon and
tone; pass `extra` for follow-up actions.

```python
def success_result() -> rx.Component:
    return antd.result(
        status="success",
        title="Order placed successfully!",
        sub_title="Order #2017182818828182881 — confirmation sent to your email.",
        extra=antd.space(
            antd.button("Go to console", type="primary"),
            antd.button("Buy again"),
        ),
    )


def not_found_result() -> rx.Component:
    return antd.result(
        status="404",                        # success | error | info | warning | 404 | 403 | 500
        title="404",
        sub_title="Sorry, the page you visited does not exist.",
        extra=antd.button("Back home", type="primary"),
    )
```

Supply a custom `icon=icon("SmileOutlined")` to override the default glyph, and pass
children for extra detail content below the result.

## skeleton

A placeholder shown while content loads. Drive a `loading` flag from state and pass
the real content as children — `skeleton` renders the placeholder when `loading=True`
and the children otherwise.

```python
class LoadState(rx.State):
    loading: bool = True

    @rx.event
    def toggle(self):
        self.loading = not self.loading


def loading_card() -> rx.Component:
    return rx.vstack(
        antd.button("Toggle loading", on_click=LoadState.toggle),
        antd.skeleton(
            rx.vstack(                       # shown when loading is False
                rx.heading("Ada Lovelace"),
                rx.text("Author, analyst and the first computer programmer."),
            ),
            loading=LoadState.loading,
            active=True,                     # shimmer animation
            avatar=True,                     # or a dict, e.g. {"size": "large", "shape": "circle"}
            title=True,
            paragraph={"rows": 3},
            round=True,
        ),
        spacing="4",
    )
```

### skeleton_button

A placeholder for a button (`Skeleton.Button`).

```python
antd.skeleton_button(active=True, size="large", shape="round", block=False)
```

### skeleton_image

A placeholder for an image (`Skeleton.Image`).

```python
antd.skeleton_image(active=True)
```

## spin

A loading spinner that can overlay arbitrary content. Wrap the content as children
and toggle `spinning`.

```python
class SpinState(rx.State):
    spinning: bool = True

    @rx.event
    def stop(self):
        self.spinning = False


def loading_panel() -> rx.Component:
    return antd.spin(
        rx.box(                              # children = content under the overlay
            rx.text("Dashboard content loads here."),
            height="160px",
        ),
        spinning=SpinState.spinning,
        size="large",                        # small | middle | large
        tip="Loading…",
        delay=200,                           # ms before the spinner appears
    )
```

For a page-blocking spinner with a progress ring, use `fullscreen=True` with
`percent="auto"`; pass a custom `indicator=icon("LoadingOutlined")` to swap the glyph.

## watermark

Overlays a repeating, tamper-resistant watermark over its children — handy for
sensitive previews.

```python
def watermarked_card() -> rx.Component:
    return antd.watermark(
        rx.box(                              # children = the protected content
            rx.heading("Confidential report"),
            rx.text("Internal use only. Do not distribute."),
            padding="2rem",
            height="240px",
        ),
        content=["Confidential", "ecrespo@gmail.com"],
        rotate=-22,
        gap=[120, 120],
        offset=[60, 60],
        z_index=11,
        font={"color": "rgba(0,0,0,0.12)", "fontSize": 16},
    )
```

Pass a single string for `content`, or set `image="/stamp.png"` (with `width`/`height`)
to watermark with an image instead of text.

## Imperative feedback (message / notification)

Ant Design's `message.*`, `notification.*`, and `Modal.confirm` are **imperative hook
APIs** (you call them from JS like `message.success("Saved")`), not components. They
are **not wrapped in 0.1.0** — they are on the roadmap for **Phase 6**.

Until then you have two options:

- Wrap the relevant subtree in `antd.app(...)` (the Ant Design `App` provider, which
  hosts the static `message`/`notification`/`modal` instances) and trigger the call
  through a small custom JS helper passed via `custom_attrs={...}` or an
  `rx.call_script(...)` event.
- Or use Reflex's own toast, which needs no extra wiring:

```python
class SaveState(rx.State):
    @rx.event
    def save(self):
        # ... persist ...
        return rx.toast.success("Saved successfully")
```

See also: [usage guide](../usage.md) and the
[component catalog](../../sdd/06-component-catalog.md).
