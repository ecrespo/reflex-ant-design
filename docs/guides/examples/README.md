# reflex-ant-design — examples by category

A runnable, copy-paste example for **every** Ant Design component wrapped by
`reflex-ant-design` (102 factories), grouped by the Ant Design category menu.
Each guide uses the `antd.*` namespace, real props/events only, and shows state
binding where it matters.

```python
import reflex as rx
from reflex_ant_design import antd, icon
```

## The guides

| # | Guide | Components |
| --- | --- | --- |
| 01 | [General](01-general.md) | button, float_button, float_button_group, back_top, typography, title, text, paragraph, link, icon |
| 02 | [Layout](02-layout.md) | divider, flex, row, col, layout, header, content, footer, sider, space, space_compact, splitter, splitter_panel |
| 03 | [Navigation](03-navigation.md) | affix, anchor, breadcrumb, dropdown, dropdown_button, menu, pagination, steps, tabs |
| 04 | [Data Entry](04-data-entry.md) | input (+ text_area, search, password, otp), input_number, checkbox(_group), radio(_group/_button), select, switch, slider, rate, date/time/range pickers, auto_complete, cascader, tree_select, mentions, color_picker, transfer, upload(_dragger), form(_item/_list) |
| 05 | [Data Display](05-data-display.md) | avatar(_group), badge(_ribbon), calendar, card(_meta/_grid), carousel, collapse, descriptions, empty, image, list_view(_item/_meta), tooltip, popover, qr_code, segmented, statistic(_countdown), table, tag(checkable_tag), timeline, tour, tree |
| 06 | [Feedback](06-feedback.md) | alert, drawer, modal, popconfirm, progress, result, skeleton(_button/_image), spin, watermark |
| 07 | [Config & Theming](07-config-theming.md) | config_provider, app, dark mode, per-component tokens |

## How to read these

- **Namespace style.** Examples call `antd.<factory>(*children, **props)`. The
  same factories are also importable flat: `from reflex_ant_design import button`.
  (One rename: `antd.list` ↔ flat `list_view`, to avoid shadowing `list`.)
- **Snake_case props** compile to antd camelCase (`allow_clear` → `allowClear`).
- **Serializable events.** Each handler receives a JSON-serializable payload
  (string, number, bool, list, or dict) — never a raw DOM event or `dayjs`
  object. The payload is annotated in comments and tabulated in
  [`../../sdd/04-data-model.md`](../../sdd/04-data-model.md).
- **Escape hatch.** Any antd prop not yet typed is reachable via
  `custom_attrs={...}`.

## See also

- [Usage guide](../usage.md) — theming, state binding, pickers, forms, gotchas.
- [Compatibility guide](../compatibility.md) — antd v5/v6 and React versions.
- [Component catalog](../../sdd/06-component-catalog.md) — the full antd → wrapper map.
- [Spec (canonical)](../../../specs/reflex-ant-design/README.md) — requirements, design, tasks.
