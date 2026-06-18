# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-17

### Added

- Initial release wrapping the Ant Design (`antd`) component set for Reflex.
- General: Button, FloatButton (+ Group, BackTop), Typography (Title/Text/
  Paragraph/Link), and an `icon()` factory over `@ant-design/icons`.
- Layout: Divider, Flex, Grid (Row/Col), Layout (Header/Sider/Content/Footer),
  Space (+ Compact), Splitter (+ Panel).
- Navigation: Anchor, Breadcrumb, Dropdown (+ Button), Menu, Pagination, Steps,
  Tabs.
- Data Entry: Input (+ TextArea/Search/Password/OTP), InputNumber, Checkbox
  (+ Group), Radio (+ Group/Button), Select, Switch, Slider, Rate, DatePicker
  (+ RangePicker), TimePicker, AutoComplete, Cascader, TreeSelect, Mentions,
  ColorPicker, Transfer, Upload (+ Dragger), Form (+ Item/List).
- Data Display: Avatar (+ Group), Badge (+ Ribbon), Card (+ Meta/Grid),
  Carousel, Collapse, Descriptions, Empty, Image, List (+ Item/Meta), Popover,
  Tooltip, QRCode, Segmented, Statistic (+ Countdown), Table, Tag (+ Checkable),
  Timeline, Tour, Tree.
- Feedback: Alert, Drawer, Modal, Popconfirm, Progress, Result, Skeleton
  (+ Button/Image), Spin, Watermark.
- Theming via `ConfigProvider` and the `App` context wrapper.
- A flat factory API and an `antd.*` namespace.
- Demo app (`reflex_ant_design_demo`) exercising every category.
- Spec-Driven Design documentation under `docs/sdd` and usage/compatibility
  guides under `docs/guides`.

[0.1.0]: https://github.com/ecrespo/reflex-ant-design/releases/tag/v0.1.0
