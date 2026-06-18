"""Data entry components: inputs, selects, pickers, toggles, forms.

This is the largest Ant Design category. Each wrapper exposes the component's
``value``/``on_change`` pair (so it can be bound to Reflex state) plus the most
useful configuration props. Event specs extract the meaningful payload (the new
value / checked flag / date string) so what reaches the backend is serializable.
"""

from __future__ import annotations

from typing import Literal

import reflex as rx
from reflex.vars import Var

from .base import AntdComponent, Size, Variant

# ---------------------------------------------------------------------------
# Reusable event specs
# ---------------------------------------------------------------------------
# antd passes a DOM event for text inputs; the value lives on e.target.value.
_on_input = lambda e: [e.target.value]  # noqa: E731
# Checkbox / Radio pass a DOM event with e.target.checked.
_on_checked = lambda e: [e.target.checked]  # noqa: E731
# Most rich controls (Select, Slider, Switch, Rate...) pass the value directly.
_on_value = lambda value: [value]  # noqa: E731
# Date/Time pickers pass (dayjsValue, formattedString); we keep the string.
_on_date = lambda date, date_string: [date_string]  # noqa: E731


# ---------------------------------------------------------------------------
# Input family
# ---------------------------------------------------------------------------
class Input(AntdComponent):
    """``Input`` -- a basic single-line text field."""

    tag = "Input"

    value: Var[str]
    default_value: Var[str]
    placeholder: Var[str]
    type: Var[str]
    size: Var[Size]
    variant: Var[Variant]
    status: Var[Literal["error", "warning"]]
    disabled: Var[bool]
    allow_clear: Var[bool | dict]
    max_length: Var[int]
    show_count: Var[bool]
    bordered: Var[bool]
    prefix: Var[rx.Component]
    suffix: Var[rx.Component]
    add_on_before: Var[rx.Component]
    add_on_after: Var[rx.Component]

    on_change: rx.EventHandler[_on_input]
    on_press_enter: rx.EventHandler[_on_input]
    on_focus: rx.EventHandler[rx.event.no_args_event_spec]
    on_blur: rx.EventHandler[rx.event.no_args_event_spec]


class TextArea(Input):
    """``Input.TextArea`` -- a multi-line text field with optional auto-size."""

    tag = "Input.TextArea"

    rows: Var[int]
    # bool or {"minRows": int, "maxRows": int}.
    auto_size: Var[bool | dict]


class SearchInput(Input):
    """``Input.Search`` -- an input with an attached search button."""

    tag = "Input.Search"

    enter_button: Var[bool | str]
    loading: Var[bool]

    on_search: rx.EventHandler[_on_input]


class PasswordInput(Input):
    """``Input.Password`` -- a masked input with a visibility toggle."""

    tag = "Input.Password"

    visibility_toggle: Var[bool | dict]


class InputOTP(AntdComponent):
    """``Input.OTP`` -- a one-time-password / verification code input."""

    tag = "Input.OTP"

    length: Var[int]
    variant: Var[Variant]
    size: Var[Size]
    disabled: Var[bool]
    mask: Var[bool | str]
    formatter: Var[str]

    on_change: rx.EventHandler[_on_value]


class InputNumber(AntdComponent):
    """``InputNumber`` -- a numeric input with steppers and bounds."""

    tag = "InputNumber"

    value: Var[int | float]
    default_value: Var[int | float]
    placeholder: Var[str]
    min: Var[int | float]
    max: Var[int | float]
    step: Var[int | float]
    precision: Var[int]
    size: Var[Size]
    variant: Var[Variant]
    status: Var[Literal["error", "warning"]]
    disabled: Var[bool]
    keyboard: Var[bool]
    controls: Var[bool]
    prefix: Var[rx.Component]
    suffix: Var[rx.Component]
    string_mode: Var[bool]

    on_change: rx.EventHandler[_on_value]
    on_press_enter: rx.EventHandler[rx.event.no_args_event_spec]


# ---------------------------------------------------------------------------
# Checkbox / Radio
# ---------------------------------------------------------------------------
class Checkbox(AntdComponent):
    """``Checkbox`` -- a single on/off box."""

    tag = "Checkbox"

    checked: Var[bool]
    default_checked: Var[bool]
    indeterminate: Var[bool]
    disabled: Var[bool]
    auto_focus: Var[bool]

    on_change: rx.EventHandler[_on_checked]


class CheckboxGroup(AntdComponent):
    """``Checkbox.Group`` -- a group of checkboxes bound to a list value."""

    tag = "Checkbox.Group"

    value: Var[list[str]]
    default_value: Var[list[str]]
    # ["A", "B"] or [{"label", "value", "disabled"}].
    options: Var[list[str] | list[dict]]
    disabled: Var[bool]

    on_change: rx.EventHandler[_on_value]


class Radio(AntdComponent):
    """``Radio`` -- a single radio button."""

    tag = "Radio"

    value: Var[str | int | bool]
    checked: Var[bool]
    default_checked: Var[bool]
    disabled: Var[bool]

    on_change: rx.EventHandler[_on_checked]


class RadioGroup(AntdComponent):
    """``Radio.Group`` -- a group of mutually exclusive radio buttons."""

    tag = "Radio.Group"

    value: Var[str | int]
    default_value: Var[str | int]
    options: Var[list[str] | list[dict]]
    option_type: Var[Literal["default", "button"]]
    button_style: Var[Literal["outline", "solid"]]
    size: Var[Size]
    disabled: Var[bool]

    on_change: rx.EventHandler[_on_input]


class RadioButton(Radio):
    """``Radio.Button`` -- a radio styled as a segmented button."""

    tag = "Radio.Button"


# ---------------------------------------------------------------------------
# Select
# ---------------------------------------------------------------------------
class Select(AntdComponent):
    """``Select`` -- a dropdown selector, single or multiple."""

    tag = "Select"

    value: Var[str | int | list]
    default_value: Var[str | int | list]
    placeholder: Var[str]
    # [{"label", "value", "disabled"}] or grouped options.
    options: Var[list[dict]]
    mode: Var[Literal["multiple", "tags"]]
    size: Var[Size]
    variant: Var[Variant]
    status: Var[Literal["error", "warning"]]
    disabled: Var[bool]
    loading: Var[bool]
    allow_clear: Var[bool]
    show_search: Var[bool]
    filter_option: Var[bool]
    max_count: Var[int]
    max_tag_count: Var[int | Literal["responsive"]]
    open: Var[bool]
    popup_match_select_width: Var[bool]

    on_change: rx.EventHandler[_on_value]
    on_search: rx.EventHandler[_on_value]
    on_select: rx.EventHandler[_on_value]
    on_deselect: rx.EventHandler[_on_value]
    on_clear: rx.EventHandler[rx.event.no_args_event_spec]
    on_dropdown_visible_change: rx.EventHandler[lambda open: [open]]


# ---------------------------------------------------------------------------
# Switch / Slider / Rate
# ---------------------------------------------------------------------------
class Switch(AntdComponent):
    """``Switch`` -- a toggle between two states."""

    tag = "Switch"

    checked: Var[bool]
    default_checked: Var[bool]
    disabled: Var[bool]
    loading: Var[bool]
    size: Var[Literal["default", "small"]]
    checked_children: Var[rx.Component | str]
    un_checked_children: Var[rx.Component | str]

    on_change: rx.EventHandler[_on_value]


class Slider(AntdComponent):
    """``Slider`` -- pick a number (or range) by dragging a handle."""

    tag = "Slider"

    value: Var[int | list[int]]
    default_value: Var[int | list[int]]
    min: Var[int]
    max: Var[int]
    step: Var[int | float]
    range: Var[bool | dict]
    vertical: Var[bool]
    dots: Var[bool]
    included: Var[bool]
    disabled: Var[bool]
    # {value: label} marks on the track.
    marks: Var[dict]
    tooltip: Var[dict]
    keyboard: Var[bool]

    on_change: rx.EventHandler[_on_value]
    on_change_complete: rx.EventHandler[_on_value]


class Rate(AntdComponent):
    """``Rate`` -- a star rating control."""

    tag = "Rate"

    value: Var[int | float]
    default_value: Var[int | float]
    count: Var[int]
    allow_half: Var[bool]
    allow_clear: Var[bool]
    disabled: Var[bool]
    character: Var[rx.Component | str]
    tooltips: Var[list[str]]

    on_change: rx.EventHandler[_on_value]
    on_hover_change: rx.EventHandler[_on_value]


# ---------------------------------------------------------------------------
# Date / Time pickers
# ---------------------------------------------------------------------------
class DatePicker(AntdComponent):
    """``DatePicker`` -- pick a date/time.

    Note: antd stores values as ``dayjs`` objects. Bind to ``on_change`` (which
    yields the formatted *string*) and pass ``format`` for round-tripping; see
    ``docs/guides/usage.md``.
    """

    tag = "DatePicker"

    placeholder: Var[str]
    format: Var[str]
    picker: Var[Literal["date", "week", "month", "quarter", "year"]]
    size: Var[Size]
    variant: Var[Variant]
    status: Var[Literal["error", "warning"]]
    disabled: Var[bool]
    allow_clear: Var[bool]
    show_time: Var[bool | dict]
    show_today: Var[bool]
    multiple: Var[bool]

    on_change: rx.EventHandler[_on_date]
    on_ok: rx.EventHandler[rx.event.no_args_event_spec]


class RangePicker(DatePicker):
    """``DatePicker.RangePicker`` -- pick a start/end date range."""

    tag = "DatePicker.RangePicker"

    on_change: rx.EventHandler[lambda dates, date_strings: [date_strings]]


class TimePicker(AntdComponent):
    """``TimePicker`` -- pick a time of day."""

    tag = "TimePicker"

    placeholder: Var[str]
    format: Var[str]
    size: Var[Size]
    variant: Var[Variant]
    disabled: Var[bool]
    allow_clear: Var[bool]
    use12_hours: Var[bool]
    hour_step: Var[int]
    minute_step: Var[int]
    second_step: Var[int]

    on_change: rx.EventHandler[_on_date]


# ---------------------------------------------------------------------------
# AutoComplete / Cascader / TreeSelect / Mentions
# ---------------------------------------------------------------------------
class AutoComplete(AntdComponent):
    """``AutoComplete`` -- an input with autocomplete suggestions."""

    tag = "AutoComplete"

    value: Var[str]
    default_value: Var[str]
    placeholder: Var[str]
    options: Var[list[dict]]
    size: Var[Size]
    variant: Var[Variant]
    disabled: Var[bool]
    allow_clear: Var[bool]
    backfill: Var[bool]
    filter_option: Var[bool]

    on_change: rx.EventHandler[_on_value]
    on_select: rx.EventHandler[_on_value]
    on_search: rx.EventHandler[_on_value]


class Cascader(AntdComponent):
    """``Cascader`` -- select a value from a hierarchical (cascading) list."""

    tag = "Cascader"

    value: Var[list]
    default_value: Var[list]
    placeholder: Var[str]
    # Tree of {"value", "label", "children": [...]}.
    options: Var[list[dict]]
    multiple: Var[bool]
    size: Var[Size]
    variant: Var[Variant]
    disabled: Var[bool]
    allow_clear: Var[bool]
    show_search: Var[bool]
    change_on_select: Var[bool]
    expand_trigger: Var[Literal["click", "hover"]]

    on_change: rx.EventHandler[_on_value]


class TreeSelect(AntdComponent):
    """``TreeSelect`` -- a select whose options are a tree."""

    tag = "TreeSelect"

    value: Var[str | list]
    default_value: Var[str | list]
    placeholder: Var[str]
    tree_data: Var[list[dict]]
    multiple: Var[bool]
    tree_checkable: Var[bool]
    show_search: Var[bool]
    allow_clear: Var[bool]
    size: Var[Size]
    variant: Var[Variant]
    disabled: Var[bool]
    tree_default_expand_all: Var[bool]

    on_change: rx.EventHandler[_on_value]
    on_select: rx.EventHandler[_on_value]


class Mentions(AntdComponent):
    """``Mentions`` -- a textarea with ``@user`` style mention suggestions."""

    tag = "Mentions"

    value: Var[str]
    default_value: Var[str]
    placeholder: Var[str]
    options: Var[list[dict]]
    prefix: Var[str | list[str]]
    split: Var[str]
    rows: Var[int]
    auto_size: Var[bool | dict]
    variant: Var[Variant]
    status: Var[Literal["error", "warning"]]
    disabled: Var[bool]

    on_change: rx.EventHandler[_on_value]
    on_select: rx.EventHandler[lambda option, prefix: [option]]
    on_search: rx.EventHandler[lambda text, prefix: [text]]


# ---------------------------------------------------------------------------
# ColorPicker / Transfer
# ---------------------------------------------------------------------------
class ColorPicker(AntdComponent):
    """``ColorPicker`` -- pick a color, with presets and alpha."""

    tag = "ColorPicker"

    value: Var[str]
    default_value: Var[str]
    format: Var[Literal["rgb", "hex", "hsb"]]
    size: Var[Size]
    disabled: Var[bool]
    allow_clear: Var[bool]
    show_text: Var[bool]
    presets: Var[list[dict]]
    mode: Var[str | list[str]]

    on_change: rx.EventHandler[lambda value, hex: [hex]]
    on_change_complete: rx.EventHandler[_on_value]
    on_clear: rx.EventHandler[rx.event.no_args_event_spec]


class Transfer(AntdComponent):
    """``Transfer`` -- move items between a source and target list."""

    tag = "Transfer"

    data_source: Var[list[dict]]
    target_keys: Var[list[str]]
    selected_keys: Var[list[str]]
    titles: Var[list[str]]
    show_search: Var[bool]
    one_way: Var[bool]
    disabled: Var[bool]
    pagination: Var[bool | dict]

    on_change: rx.EventHandler[
        lambda target_keys, direction, move_keys: [target_keys, direction, move_keys]
    ]
    on_select_change: rx.EventHandler[
        lambda source_selected, target_selected: [source_selected, target_selected]
    ]
    on_search: rx.EventHandler[lambda direction, value: [direction, value]]


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------
class Upload(AntdComponent):
    """``Upload`` -- upload files by selecting or dragging them.

    For server-side handling you usually point ``action`` at an endpoint; in a
    Reflex app you can also drive uploads through Reflex's own upload events.
    """

    tag = "Upload"

    action: Var[str]
    accept: Var[str]
    list_type: Var[Literal["text", "picture", "picture-card", "picture-circle"]]
    multiple: Var[bool]
    directory: Var[bool]
    disabled: Var[bool]
    max_count: Var[int]
    file_list: Var[list[dict]]
    default_file_list: Var[list[dict]]
    show_upload_list: Var[bool | dict]
    name: Var[str]
    headers: Var[dict]
    data: Var[dict]
    with_credentials: Var[bool]

    on_change: rx.EventHandler[lambda info: [info]]
    on_remove: rx.EventHandler[lambda file: [file]]
    on_preview: rx.EventHandler[lambda file: [file]]
    on_drop: rx.EventHandler[rx.event.no_args_event_spec]


class UploadDragger(Upload):
    """``Upload.Dragger`` -- a large drag-and-drop upload area."""

    tag = "Upload.Dragger"


# ---------------------------------------------------------------------------
# Form
# ---------------------------------------------------------------------------
class Form(AntdComponent):
    """``Form`` -- high performance form with validation and layout.

    antd's ``Form`` manages its own field store. ``on_finish`` receives the
    collected values dict on a successful submit; ``on_values_change`` fires on
    every field change. For tight two-way binding to Reflex state, the native
    ``rx.form`` may be simpler -- see ``docs/guides/usage.md``.
    """

    tag = "Form"

    name: Var[str]
    layout: Var[Literal["horizontal", "vertical", "inline"]]
    label_align: Var[Literal["left", "right"]]
    label_col: Var[dict]
    wrapper_col: Var[dict]
    initial_values: Var[dict]
    size: Var[Size]
    variant: Var[Variant]
    disabled: Var[bool]
    colon: Var[bool]
    required_mark: Var[bool]
    scroll_to_first_error: Var[bool]

    on_finish: rx.EventHandler[lambda values: [values]]
    on_finish_failed: rx.EventHandler[lambda error_info: [error_info]]
    on_values_change: rx.EventHandler[lambda changed, all_values: [changed, all_values]]


class FormItem(AntdComponent):
    """``Form.Item`` -- a labelled field with validation rules."""

    tag = "Form.Item"

    name: Var[str]
    label: Var[str | rx.Component]
    rules: Var[list[dict]]
    required: Var[bool]
    help: Var[str | rx.Component]
    extra: Var[str | rx.Component]
    tooltip: Var[str | dict]
    valid_status: Var[Literal["success", "warning", "error", "validating"]]
    has_feedback: Var[bool]
    label_col: Var[dict]
    wrapper_col: Var[dict]
    no_style: Var[bool]
    colon: Var[bool]
    initial_value: Var[str | int | bool | list | dict]


class FormList(AntdComponent):
    """``Form.List`` -- a dynamic list of form fields."""

    tag = "Form.List"

    name: Var[str | list]


input = Input.create
text_area = TextArea.create
search_input = SearchInput.create
password_input = PasswordInput.create
input_otp = InputOTP.create
input_number = InputNumber.create
checkbox = Checkbox.create
checkbox_group = CheckboxGroup.create
radio = Radio.create
radio_group = RadioGroup.create
radio_button = RadioButton.create
select = Select.create
switch = Switch.create
slider = Slider.create
rate = Rate.create
date_picker = DatePicker.create
range_picker = RangePicker.create
time_picker = TimePicker.create
auto_complete = AutoComplete.create
cascader = Cascader.create
tree_select = TreeSelect.create
mentions = Mentions.create
color_picker = ColorPicker.create
transfer = Transfer.create
upload = Upload.create
upload_dragger = UploadDragger.create
form = Form.create
form_item = FormItem.create
form_list = FormList.create
