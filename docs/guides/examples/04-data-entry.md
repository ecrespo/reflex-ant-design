# Data Entry components

Usage examples for the **Data Entry** components of `reflex-ant-design` (Ant Design
wrapped for Reflex). These are interactive controls, so every example binds to a
small `rx.State` and uses Reflex event handlers. A comment on each handler notes
the payload type that reaches Python. All examples assume:

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

> Only the props/events listed in the component catalog are wrapped. Anything not
> shown here can usually be passed through with `custom_attrs={...}`.

## Contents

- **Text inputs:** [input](#input) · [text_area](#text_area) · [search_input](#search_input) · [password_input](#password_input) · [input_otp](#input_otp)
- **Number & toggles:** [input_number](#input_number) · [checkbox](#checkbox) · [checkbox_group](#checkbox_group) · [radio](#radio) · [radio_group](#radio_group) · [switch](#switch) · [slider](#slider) · [rate](#rate)
- **Selection:** [select](#select) · [segmented (see note)](#select) · [auto_complete](#auto_complete) · [cascader](#cascader) · [tree_select](#tree_select) · [mentions](#mentions)
- **Pickers:** [date_picker](#date_picker) · [range_picker](#range_picker) · [time_picker](#time_picker) · [color_picker](#color_picker)
- **Advanced:** [transfer](#transfer) · [upload](#upload) · [upload_dragger](#upload_dragger)
- **Form:** [form](#form) · [form_item](#form_item) · [form_list](#form_list)

---

## input

A single-line text box. Bind `value`/`on_change` for a controlled input; `on_change`
delivers the current string to Python.

```python
class S(rx.State):
    name: str = ""

    @rx.event
    def set_name(self, value: str):  # value: str
        self.name = value


def name_field() -> rx.Component:
    return antd.input(
        value=S.name,
        on_change=S.set_name,
        placeholder="Your name",
        size="middle",                 # small | middle | large
        allow_clear=True,
        max_length=40,
        show_count=True,
        prefix=icon("user"),           # rx.Component slots
        on_press_enter=S.set_name,     # on_press_enter -> str
    )
```

Add affixes inside or outside the box:

```python
antd.input(
    value=S.name,
    on_change=S.set_name,
    add_on_before="https://",          # rx.Component or str
    add_on_after=".com",
    suffix=icon("search"),
    variant="filled",                  # outlined | borderless | filled | underlined
    status="warning",                  # error | warning
)
```

## text_area

Multi-line input. Inherits all `input` props and adds `rows` and `auto_size`.

```python
class S(rx.State):
    bio: str = ""

    @rx.event
    def set_bio(self, value: str):  # value: str
        self.bio = value


def bio_field() -> rx.Component:
    return antd.text_area(
        value=S.bio,
        on_change=S.set_bio,
        placeholder="Tell us about yourself",
        rows=4,
        auto_size={"minRows": 2, "maxRows": 6},  # or auto_size=True
        show_count=True,
        max_length=200,
    )
```

## search_input

An input with an attached search button. `on_search` fires on enter / button click.

```python
class S(rx.State):
    query: str = ""
    loading: bool = False

    @rx.event
    def run_search(self, value: str):  # value: str
        self.query = value
        # ... trigger a backend lookup here


def search_box() -> rx.Component:
    return antd.search_input(
        placeholder="Search products",
        enter_button="Search",          # True for an icon-only button, or a label
        loading=S.loading,
        on_search=S.run_search,         # on_search -> str
        on_change=S.set_query,          # on_change -> str
        allow_clear=True,
    )
```

## password_input

A masked input with a visibility toggle. `on_change` yields the plain string.

```python
class S(rx.State):
    pwd: str = ""

    @rx.event
    def set_pwd(self, value: str):  # value: str
        self.pwd = value


def password_field() -> rx.Component:
    return antd.password_input(
        value=S.pwd,
        on_change=S.set_pwd,
        placeholder="Password",
        visibility_toggle=True,         # or {"visible": S.show, "onVisibleChange": ...}
    )
```

## input_otp

A grouped set of one-character boxes for one-time codes. `on_change` fires with the
full string once every cell is filled.

```python
class S(rx.State):
    code: str = ""

    @rx.event
    def set_code(self, value: str):  # value: str (full OTP)
        self.code = value


def otp_field() -> rx.Component:
    return antd.input_otp(
        length=6,
        on_change=S.set_code,
        mask=True,                      # or a custom mask char, e.g. "*"
        formatter="upper",              # transform each typed char
        size="large",
    )
```

## input_number

A numeric stepper. `on_change` delivers a number (or `None` when cleared).

```python
class S(rx.State):
    qty: int = 1

    @rx.event
    def set_qty(self, value: int | float | None):  # value: number | None
        self.qty = int(value or 0)


def quantity_field() -> rx.Component:
    return antd.input_number(
        value=S.qty,
        on_change=S.set_qty,
        min=0,
        max=100,
        step=1,
        precision=0,
        controls=True,                  # show the +/- buttons
        keyboard=True,
        prefix="$",
        on_press_enter=S.set_qty,       # on_press_enter -> str
    )
```

## checkbox

A single boolean checkbox. `on_change` yields the checked `bool`.

```python
class S(rx.State):
    agreed: bool = False

    @rx.event
    def set_agreed(self, checked: bool):  # checked: bool
        self.agreed = checked


def terms_checkbox() -> rx.Component:
    return antd.checkbox(
        "I accept the terms",
        checked=S.agreed,
        on_change=S.set_agreed,
    )
```

## checkbox_group

A set of checkboxes driven by `options`. `on_change` yields a `list` of the checked
values.

```python
class S(rx.State):
    toppings: list[str] = ["cheese"]

    @rx.event
    def set_toppings(self, values: list):  # values: list
        self.toppings = values


def toppings_group() -> rx.Component:
    return antd.checkbox_group(
        value=S.toppings,
        on_change=S.set_toppings,
        options=[
            {"label": "Cheese", "value": "cheese"},
            {"label": "Mushroom", "value": "mushroom"},
            {"label": "Onion", "value": "onion", "disabled": True},
        ],
        # options can also be a plain list of strings: ["cheese", "mushroom"]
    )
```

## radio

A single radio button, usually used standalone or as children of a group.

```python
antd.radio("Express shipping", value="express", checked=S.fast, on_change=S.set_fast)
# on_change -> bool (checked)
```

## radio_group

Mutually exclusive options. `on_change` yields the selected value (a `str`).

```python
class S(rx.State):
    plan: str = "free"

    @rx.event
    def set_plan(self, value: str):  # value: str (selected option)
        self.plan = value


def plan_group() -> rx.Component:
    return antd.radio_group(
        value=S.plan,
        on_change=S.set_plan,
        option_type="button",           # default | button
        button_style="solid",           # outline | solid
        options=[
            {"label": "Free", "value": "free"},
            {"label": "Pro", "value": "pro"},
            {"label": "Team", "value": "team", "disabled": True},
        ],
    )
```

You can also compose `radio_button` children instead of `options`:

```python
antd.radio_group(
    antd.radio_button("Left", value="left"),
    antd.radio_button("Right", value="right"),
    value=S.align,
    on_change=S.set_align,
)
```

## switch

An on/off toggle. `on_change` yields the new `bool`.

```python
class S(rx.State):
    notify: bool = True

    @rx.event
    def set_notify(self, checked: bool):  # checked: bool
        self.notify = checked


def notify_switch() -> rx.Component:
    return antd.switch(
        checked=S.notify,
        on_change=S.set_notify,
        checked_children="ON",          # str or rx.Component
        un_checked_children="OFF",
        size="default",                 # default | small
    )
```

## slider

A draggable value selector. `on_change` fires continuously; `on_change_complete`
fires on release. Both yield the value (a number, or a `list[int]` in range mode).

```python
class S(rx.State):
    volume: int = 30
    band: list[int] = [20, 80]

    @rx.event
    def set_volume(self, value: int):  # value: number
        self.volume = value

    @rx.event
    def set_band(self, value: list[int]):  # value: list[int] (range mode)
        self.band = value


def sliders() -> rx.Component:
    return rx.vstack(
        antd.slider(
            value=S.volume,
            on_change=S.set_volume,
            min=0,
            max=100,
            step=5,
            marks={0: "0%", 50: "50%", 100: "100%"},
            tooltip={"open": True},
        ),
        antd.slider(
            value=S.band,
            on_change=S.set_band,
            on_change_complete=S.set_band,
            range=True,
            min=0,
            max=100,
        ),
    )
```

## rate

A star rating. `on_change` yields the chosen number.

```python
class S(rx.State):
    stars: float = 3.0

    @rx.event
    def set_stars(self, value: float):  # value: number
        self.stars = value


def rating() -> rx.Component:
    return antd.rate(
        value=S.stars,
        on_change=S.set_stars,
        count=5,
        allow_half=True,
        tooltips=["Bad", "Poor", "OK", "Good", "Great"],
        # character="A" or character=icon("heart") for custom symbols
    )
```

## select

A dropdown selector. Use `mode="multiple"` or `mode="tags"` for multi-value. In
multi mode `on_change` yields a `list`; otherwise the single selected value.

```python
class S(rx.State):
    tags: list[str] = []

    @rx.event
    def set_tags(self, values: list):  # values: list (multiple/tags mode)
        self.tags = values


def tag_select() -> rx.Component:
    return antd.select(
        value=S.tags,
        on_change=S.set_tags,
        mode="tags",                    # multiple | tags
        placeholder="Add tags",
        allow_clear=True,
        show_search=True,
        max_tag_count="responsive",     # int or "responsive"
        options=[
            {"label": "Python", "value": "py"},
            {"label": "Rust", "value": "rs"},
            {"label": "Go", "value": "go", "disabled": True},
        ],
        on_search=lambda text: rx.console_log(text),
        on_clear=S.clear_tags,
    )
```

> **segmented** is a single-select toggle bar with the same payload contract as
> `select` (`on_change` -> the new value). Bind `value`/`on_change` the same way.

## auto_complete

A text input with completion suggestions. `on_change` and `on_search` yield the
typed string; `on_select` yields the picked value.

```python
class S(rx.State):
    email: str = ""
    options: list[dict] = []

    @rx.event
    def suggest(self, text: str):  # text: str
        self.options = [{"value": f"{text}@{d}"} for d in ("gmail.com", "outlook.com")]

    @rx.event
    def set_email(self, value: str):  # value: str
        self.email = value


def email_complete() -> rx.Component:
    return antd.auto_complete(
        value=S.email,
        on_change=S.set_email,
        on_search=S.suggest,
        on_select=S.set_email,
        options=S.options,
        placeholder="email",
        allow_clear=True,
        backfill=True,
    )
```

## cascader

A multi-level dropdown for hierarchical data. `on_change` yields the selected path
as a `list`.

```python
class S(rx.State):
    region: list = []

    @rx.event
    def set_region(self, value: list):  # value: list (path of values)
        self.region = value


def region_cascader() -> rx.Component:
    return antd.cascader(
        value=S.region,
        on_change=S.set_region,
        placeholder="Select region",
        change_on_select=True,
        expand_trigger="hover",         # click | hover
        options=[
            {
                "value": "us",
                "label": "USA",
                "children": [
                    {"value": "ca", "label": "California"},
                    {"value": "ny", "label": "New York"},
                ],
            },
            {"value": "mx", "label": "Mexico", "children": [
                {"value": "cdmx", "label": "Mexico City"},
            ]},
        ],
    )
```

## tree_select

A dropdown backed by a tree. `on_change` yields the selected value(s); enable
`tree_checkable` for multi-select with checkboxes.

```python
class S(rx.State):
    node: str = ""

    @rx.event
    def set_node(self, value):  # value: str | list (multiple mode)
        self.node = value


def org_tree() -> rx.Component:
    return antd.tree_select(
        value=S.node,
        on_change=S.set_node,
        placeholder="Pick a team",
        tree_default_expand_all=True,
        show_search=True,
        allow_clear=True,
        tree_data=[
            {"title": "Engineering", "value": "eng", "children": [
                {"title": "Backend", "value": "be"},
                {"title": "Frontend", "value": "fe"},
            ]},
            {"title": "Design", "value": "design"},
        ],
    )
```

## mentions

A textarea that suggests entries after a trigger prefix. `on_change` yields the full
text; `on_search` yields the fragment after the prefix.

```python
class S(rx.State):
    note: str = ""

    @rx.event
    def set_note(self, value: str):  # value: str (full text)
        self.note = value


def mentions_box() -> rx.Component:
    return antd.mentions(
        value=S.note,
        on_change=S.set_note,
        placeholder="Type @ to mention",
        prefix="@",                     # str or list[str], e.g. ["@", "#"]
        rows=3,
        options=[
            {"value": "alice", "label": "Alice"},
            {"value": "bob", "label": "Bob"},
        ],
    )
```

## date_picker

A calendar picker. antd works in `dayjs` internally, but the wrapper hands Python a
**formatted string** controlled by `format`.

```python
class S(rx.State):
    day: str = ""

    @rx.event
    def set_day(self, value: str):  # value: str, formatted per `format`
        self.day = value


def date_field() -> rx.Component:
    return antd.date_picker(
        on_change=S.set_day,
        format="YYYY-MM-DD",
        picker="date",                  # date | week | month | quarter | year
        placeholder="Pick a date",
        allow_clear=True,
        show_time=True,                 # or {"format": "HH:mm"}
    )
```

## range_picker

A start/end date picker. Inherits `date_picker`; `on_change` yields a
`list[str]` of two formatted dates.

```python
class S(rx.State):
    span: list[str] = []

    @rx.event
    def set_span(self, values: list):  # values: list[str] (start, end)
        self.span = values


def range_field() -> rx.Component:
    return antd.range_picker(
        on_change=S.set_span,
        format="YYYY-MM-DD",
        allow_clear=True,
    )
```

## time_picker

A clock picker. `on_change` yields the formatted time string.

```python
class S(rx.State):
    at: str = ""

    @rx.event
    def set_at(self, value: str):  # value: str, formatted per `format`
        self.at = value


def time_field() -> rx.Component:
    return antd.time_picker(
        on_change=S.set_at,
        format="HH:mm",
        use12_hours=False,
        minute_step=5,
        allow_clear=True,
    )
```

## color_picker

A color selector. `on_change` yields a hex string (the `format` controls the picker
UI, not necessarily the payload shape here).

```python
class S(rx.State):
    color: str = "#1677ff"

    @rx.event
    def set_color(self, value: str):  # value: str (hex)
        self.color = value


def color_field() -> rx.Component:
    return antd.color_picker(
        value=S.color,
        on_change=S.set_color,
        on_change_complete=S.set_color,
        format="hex",                   # rgb | hex | hsb
        show_text=True,
        allow_clear=True,
        presets=[{"label": "Brand", "colors": ["#1677ff", "#52c41a", "#faad14"]}],
    )
```

## transfer

Two side-by-side lists for moving items between a source and a target. `on_change`
fires with the new target keys plus the direction and moved keys.

```python
class S(rx.State):
    target: list[str] = ["b"]

    @rx.event
    def move(self, target_keys: list, direction: str, move_keys: list):
        # target_keys: list[str], direction: "left"|"right", move_keys: list[str]
        self.target = target_keys


def transfer_box() -> rx.Component:
    return antd.transfer(
        data_source=[
            {"key": "a", "title": "Apples"},
            {"key": "b", "title": "Bananas"},
            {"key": "c", "title": "Cherries"},
        ],
        target_keys=S.target,
        on_change=S.move,
        titles=["Available", "Selected"],
        show_search=True,
    )
```

## upload

A file uploader. Children are the trigger (e.g. a button). `on_change` fires with an
`info` object describing the file list and status.

```python
class S(rx.State):
    @rx.event
    def on_upload(self, info: dict):  # info: dict {"file": {...}, "fileList": [...]}
        ...


def upload_box() -> rx.Component:
    return antd.upload(
        antd.button(icon("upload"), " Click to upload"),
        action="/api/upload",            # server URL antd POSTs to
        accept=".png,.jpg",
        list_type="text",               # text | picture | picture-card | picture-circle
        multiple=True,
        max_count=5,
        on_change=S.on_upload,
        on_remove=lambda file: rx.console_log(file),
    )
```

> In a pure-Reflex app you may prefer Reflex's own upload primitives
> (`rx.upload`, `rx.upload_files()`) instead of antd's `action` URL.

## upload_dragger

A large drag-and-drop area. Inherits all `upload` props; children describe the drop
zone.

```python
def dragger_box() -> rx.Component:
    return antd.upload_dragger(
        rx.vstack(
            icon("inbox", font_size="3em"),
            rx.text("Click or drag files to this area to upload"),
            align="center",
        ),
        action="/api/upload",
        multiple=True,
        on_change=S.on_upload,          # info: dict
        on_drop=lambda e: rx.console_log("dropped"),
    )
```

## form

A validated form. Children are `form_item`s. `on_finish` fires with a `dict` of all
collected values when validation passes.

```python
class S(rx.State):
    submitted: dict = {}

    @rx.event
    def handle_finish(self, values: dict):  # values: dict of field name -> value
        self.submitted = values

    @rx.event
    def handle_failed(self, error_info: dict):  # error_info: dict
        ...


def signup_form() -> rx.Component:
    return antd.form(
        antd.form_item(
            antd.input(placeholder="Username"),
            name="username",
            label="Username",
            rules=[{"required": True, "message": "Username is required"}],
        ),
        antd.form_item(
            antd.password_input(placeholder="Password"),
            name="password",
            label="Password",
            rules=[
                {"required": True, "message": "Password is required"},
                {"min": 8, "message": "At least 8 characters"},
            ],
            has_feedback=True,
        ),
        antd.form_item(
            antd.checkbox("Subscribe to newsletter"),
            name="subscribe",
            valid_status="success",
        ),
        antd.form_item(
            antd.button("Sign up", type="primary", html_type="submit"),
        ),
        name="signup",
        layout="vertical",              # horizontal | vertical | inline
        initial_values={"subscribe": True},
        on_finish=S.handle_finish,      # values: dict
        on_finish_failed=S.handle_failed,
        scroll_to_first_error=True,
    )
```

## form_item

Wraps a single control inside a `form`, providing the label, validation `rules`, and
feedback. `name` links the control's value into the `on_finish` dict.

```python
antd.form_item(
    antd.select(options=[{"label": "EN", "value": "en"}, {"label": "ES", "value": "es"}]),
    name="lang",
    label="Language",
    rules=[{"required": True, "message": "Choose a language"}],
    tooltip="Used for the UI",
    extra="You can change this later.",
)
```

## form_list

Renders a dynamic, repeatable group of fields under a single `name`. Collected values
arrive in `on_finish` as a list under that key.

```python
def contacts_form() -> rx.Component:
    return antd.form(
        antd.form_list(
            antd.form_item(
                antd.input(placeholder="Email"),
                name="email",
                rules=[{"required": True, "message": "Email required"}],
            ),
            name="contacts",
        ),
        name="contacts_form",
        on_finish=S.handle_finish,      # values["contacts"] -> list[dict]
    )
```

---

**See also:** [usage guide](../usage.md) ·
[component catalog](../../sdd/06-component-catalog.md)
