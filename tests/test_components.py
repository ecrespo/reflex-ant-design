"""Component-level tests: tags, dotted imports, props and event specs."""

from __future__ import annotations

import reflex as rx
from reflex_ant_design import antd
from reflex_ant_design.base import AntdComponent
from reflex_ant_design.data_entry import TextArea
from reflex_ant_design.general import Button


class _S(rx.State):
    value: str = ""

    @rx.event
    def set_value(self, v: str):
        self.value = v


def test_base_imports_antd_and_reset_css():
    button = antd.button("hi")
    imports = button._get_all_imports()
    assert any("antd" in key for key in imports)
    assert "antd/dist/reset.css" in button._get_custom_code()


def test_button_is_antd_component_with_tag():
    assert issubclass(Button, AntdComponent)
    assert Button.create().tag == "Button"


def test_dotted_tag_imports_left_most_name():
    # Input.TextArea must import `Input` (not a non-existent `TextArea`).
    textarea = TextArea.create()
    assert textarea.tag == "Input.TextArea"
    import_keys = textarea._get_all_imports()
    antd_key = next(k for k in import_keys if "antd" in k and "reset" not in k)
    imported_names = {var.tag for var in import_keys[antd_key]}
    assert "Input" in imported_names


def test_input_value_event_binding_renders():
    component = antd.input(value=_S.value, on_change=_S.set_value)
    assert component.render()


def test_select_options_prop():
    component = antd.select(options=[{"label": "A", "value": "a"}])
    assert component.render()


def test_table_columns_and_data():
    component = antd.table(
        columns=[{"title": "N", "dataIndex": "n"}],
        data_source=[{"n": 1}],
    )
    assert component.render()


def test_config_provider_theme_dict():
    component = antd.config_provider(
        antd.button("x"),
        theme={"token": {"colorPrimary": "#722ed1"}},
    )
    assert component.render()


def test_calendar_serializable_events_render():
    # antd Calendar emits dayjs objects; the wrapper must deliver serializable
    # payloads. All three event specs must compile and render.
    assert antd.calendar(on_change=_S.set_value).render()
    assert antd.calendar(on_select=_S.set_value).render()
    assert antd.calendar(on_panel_change=_S.set_value).render()
    from reflex_ant_design.data_display import Calendar

    assert Calendar.create().tag == "Calendar"


def test_affix_pins_child_and_emits_bool():
    component = antd.affix(antd.button("top"), offset_top=10, on_change=_S.set_value)
    assert component.render()
    from reflex_ant_design.navigation import Affix

    assert Affix.create().tag == "Affix"
