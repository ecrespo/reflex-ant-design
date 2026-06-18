# 06 — Component Catalog (antd → wrapper)

Complete mapping of Ant Design components to their `reflex-ant-design` wrappers.
Legend: ✅ wrapped in 0.1.0 · ⏳ planned · ⛔ out of scope.

## General (`general.py`)

| antd | Class | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- | --- |
| Button | `Button` | `button` | type, size, shape, danger, ghost, block, loading, icon, href | on_click | ✅ |
| FloatButton | `FloatButton` | `float_button` | type, shape, description, tooltip, icon, badge | on_click | ✅ |
| FloatButton.Group | `FloatButtonGroup` | `float_button_group` | trigger, open | on_open_change | ✅ |
| FloatButton.BackTop | `BackTop` | `back_top` | visibility_height, target | on_click | ✅ |
| Typography | `Typography` | `typography` | — | — | ✅ |
| Typography.Title | `Title` | `title` | level, type, ellipsis, copyable | — | ✅ |
| Typography.Text | `Text` | `text` | strong, italic, code, mark, type, copyable | — | ✅ |
| Typography.Paragraph | `Paragraph` | `paragraph` | ellipsis, copyable | — | ✅ |
| Typography.Link | `TypographyLink` | `link` | href, target | — | ✅ |
| Icon (`@ant-design/icons`) | `_AntdIcon` | `icon(name)` | spin, rotate, style | on_click | ✅ |

## Layout (`layout.py`)

| antd | Factory | Key props | Status |
| --- | --- | --- | --- |
| Divider | `divider` | type, orientation, dashed, variant, plain | ✅ |
| Flex | `flex` | vertical, wrap, justify, align, gap | ✅ |
| Row | `row` | justify, align, gutter, wrap | ✅ |
| Col | `col` | span, offset, order, push, pull, xs–xxl | ✅ |
| Layout | `layout` | has_sider | ✅ |
| Layout.Header / Content / Footer | `header` / `content` / `footer` | — | ✅ |
| Layout.Sider | `sider` | collapsed, collapsible, width, breakpoint, theme | ✅ (on_collapse) |
| Space | `space` | direction, size, align, wrap, split | ✅ |
| Space.Compact | `space_compact` | direction, size, block | ✅ |
| Splitter | `splitter` | layout | ✅ (on_resize*) |
| Splitter.Panel | `splitter_panel` | default_size, min, max, collapsible | ✅ |

## Navigation (`navigation.py`)

| antd | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- |
| Anchor | `anchor` | items, direction, affix, offset_top | on_change, on_click | ✅ |
| Breadcrumb | `breadcrumb` | items, separator | — | ✅ |
| Dropdown | `dropdown` | menu, trigger, placement, arrow, open | on_open_change | ✅ |
| Dropdown.Button | `dropdown_button` | type, size, loading | on_click | ✅ |
| Menu | `menu` | items, mode, theme, selected_keys, open_keys | on_select, on_open_change, on_click | ✅ |
| Pagination | `pagination` | current, total, page_size, show_size_changer | on_change, on_show_size_change | ✅ |
| Steps | `steps` | items, current, direction, status, type | on_change | ✅ |
| Tabs | `tabs` | items, active_key, type, tab_position | on_change, on_tab_click, on_edit | ✅ |

## Data Entry (`data_entry.py`)

| antd | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- |
| Input | `input` | value, placeholder, size, variant, allow_clear, prefix | on_change, on_press_enter | ✅ |
| Input.TextArea | `text_area` | rows, auto_size, show_count, max_length | on_change | ✅ |
| Input.Search | `search_input` | enter_button, loading | on_search | ✅ |
| Input.Password | `password_input` | visibility_toggle | on_change | ✅ |
| Input.OTP | `input_otp` | length, mask, formatter | on_change | ✅ |
| InputNumber | `input_number` | min, max, step, precision, controls | on_change | ✅ |
| Checkbox | `checkbox` | checked, indeterminate, disabled | on_change | ✅ |
| Checkbox.Group | `checkbox_group` | value, options | on_change | ✅ |
| Radio / Radio.Button | `radio` / `radio_button` | value, checked | on_change | ✅ |
| Radio.Group | `radio_group` | value, options, option_type, button_style | on_change | ✅ |
| Select | `select` | value, options, mode, show_search, allow_clear | on_change, on_search, on_select | ✅ |
| Switch | `switch` | checked, loading, size, checked_children | on_change | ✅ |
| Slider | `slider` | value, min, max, step, range, marks | on_change, on_change_complete | ✅ |
| Rate | `rate` | value, count, allow_half, character | on_change | ✅ |
| DatePicker | `date_picker` | format, picker, show_time, allow_clear | on_change, on_ok | ✅ |
| DatePicker.RangePicker | `range_picker` | format, show_time | on_change | ✅ |
| TimePicker | `time_picker` | format, use12_hours, hour_step | on_change | ✅ |
| AutoComplete | `auto_complete` | options, backfill, filter_option | on_change, on_select, on_search | ✅ |
| Cascader | `cascader` | options, multiple, change_on_select | on_change | ✅ |
| TreeSelect | `tree_select` | tree_data, tree_checkable, multiple | on_change, on_select | ✅ |
| Mentions | `mentions` | options, prefix, split | on_change, on_select, on_search | ✅ |
| ColorPicker | `color_picker` | format, presets, show_text, allow_clear | on_change, on_change_complete | ✅ |
| Transfer | `transfer` | data_source, target_keys, show_search | on_change, on_select_change | ✅ |
| Upload | `upload` | action, accept, list_type, multiple, max_count | on_change, on_remove, on_preview | ✅ |
| Upload.Dragger | `upload_dragger` | (inherits Upload) | on_drop | ✅ |
| Form | `form` | layout, initial_values, label_col, size | on_finish, on_finish_failed, on_values_change | ✅ |
| Form.Item | `form_item` | name, label, rules, required, tooltip | — | ✅ |
| Form.List | `form_list` | name | — | ✅ |

## Data Display (`data_display.py`)

| antd | Factory | Key props | Status |
| --- | --- | --- | --- |
| Avatar / Avatar.Group | `avatar` / `avatar_group` | src, icon, shape, size, max_count | ✅ |
| Badge / Badge.Ribbon | `badge` / `badge_ribbon` | count, dot, status, color, text | ✅ |
| Card / Card.Meta / Card.Grid | `card` / `card_meta` / `card_grid` | title, extra, hoverable, loading, cover | ✅ |
| Carousel | `carousel` | autoplay, dots, effect, infinite | ✅ (after/before_change) |
| Collapse | `collapse` | items, accordion, bordered, ghost | ✅ (on_change) |
| Descriptions | `descriptions` | items, title, bordered, column, layout | ✅ |
| Empty | `empty` | description, image | ✅ |
| Image | `image` | src, width, preview, fallback | ✅ (on_error) |
| List / Item / Item.Meta | `list_view` / `list_item` / `list_item_meta` | data_source, bordered, pagination, grid | ✅ |
| Popover | `popover` | content, title, placement, trigger | ✅ (on_open_change) |
| Tooltip | `tooltip` | title, placement, trigger, color | ✅ (on_open_change) |
| QRCode | `qr_code` | value, size, color, error_level, status | ✅ (on_refresh) |
| Segmented | `segmented` | value, options, size, block, vertical | ✅ (on_change) |
| Statistic / Countdown | `statistic` / `statistic_countdown` | title, value, precision, prefix, suffix | ✅ |
| Table | `table` | columns, data_source, pagination, row_selection, scroll | ✅ (on_change) |
| Tag / Tag.CheckableTag | `tag` / `checkable_tag` | color, closable, checked | ✅ (on_close/on_change) |
| Timeline | `timeline` | items, mode, pending, reverse | ✅ |
| Tour | `tour` | open, steps, current, mask | ✅ (on_close, on_change, on_finish) |
| Tree | `tree` | tree_data, checkable, draggable, expanded_keys | ✅ (on_select, on_check, on_expand) |

## Feedback (`feedback.py`)

| antd | Factory | Key props | Events | Status |
| --- | --- | --- | --- | --- |
| Alert | `alert` | message, description, type, show_icon, closable, banner | on_close | ✅ |
| Drawer | `drawer` | open, title, placement, width, mask_closable | on_close | ✅ |
| Modal | `modal` | open, title, width, centered, confirm_loading, footer | on_ok, on_cancel | ✅ |
| Popconfirm | `popconfirm` | title, description, ok_text, placement | on_confirm, on_cancel | ✅ |
| Progress | `progress` | percent, type, status, steps, stroke_color | — | ✅ |
| Result | `result` | status, title, sub_title, icon, extra | — | ✅ |
| Skeleton / Button / Image | `skeleton` / `skeleton_button` / `skeleton_image` | active, loading, avatar, paragraph | — | ✅ |
| Spin | `spin` | spinning, size, tip, delay, fullscreen | — | ✅ |
| Watermark | `watermark` | content, rotate, gap, image, font | — | ✅ |
| message (imperative) | — | — | — | ⏳ Phase 6 |
| notification (imperative) | — | — | — | ⏳ Phase 6 |
| Modal.confirm (imperative) | — | — | — | ⏳ Phase 6 |

## Config (`base.py`)

| antd | Factory | Key props | Status |
| --- | --- | --- | --- |
| ConfigProvider | `config_provider` | theme, component_size, direction, locale | ✅ |
| App | `app` | component | ✅ |

## Out of scope (⛔)

`@ant-design/pro-components`, `@ant-design/charts`, `@ant-design/x` (AI), and
server-rendered locale bundles. Custom antd props not yet typed remain reachable
through `custom_attrs`.
