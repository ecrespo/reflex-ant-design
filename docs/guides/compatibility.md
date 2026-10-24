# Compatibility guide

## Version matrix

| reflex-ant-design | Reflex | antd (npm) | React | Python |
| --- | --- | --- | --- | --- |
| 0.2.x | ≥ 0.10 | `antd@^6` (default) | 19 | ≥ 3.11 |
| 0.2.x (React 18 apps) | ≥ 0.10 | pin `antd@^5` | 18 | ≥ 3.11 |
| 0.1.x | ≥ 0.7 | `antd@^6` (default) | 19 | ≥ 3.10 |
| 0.1.x (React 18 apps) | ≥ 0.7 | pin `antd@^5` | 18 | ≥ 3.10 |

The pinned npm version lives in `custom_components/reflex_ant_design/base.py`:

```python
ANTD_VERSION = "antd@^6.0.0"
ANTD_ICONS_VERSION = "@ant-design/icons@^6.0.0"
```

## antd v5 vs v6

Ant Design v6 is largely a technical upgrade; the component **APIs used by these
wrappers are compatible across v5 and v6**. The main difference relevant here:

- **v6 requires React 18+** and drops React 17. Reflex ≥ 0.7 ships React 19, so
  `antd@^6` is the default.
- If your Reflex/React toolchain is on React 18 and you hit a peer warning,
  pin `antd@^5`:

  ```python
  # base.py
  ANTD_VERSION = "antd@^5.0.0"
  ANTD_ICONS_VERSION = "@ant-design/icons@^5.0.0"
  ```

## Pinning a different version

Because the version is declared once in `base.py`, changing it updates every
component. Always pin to a caret/exact range so the npm dependency only moves
when you intend it to.

## Styling & reset

The base component imports `antd/dist/reset.css` exactly once. antd v5/v6 are
CSS-in-JS, so component styles are injected at runtime; the reset only
normalizes base element styles. No additional global stylesheet is required.

## SSR

Ant Design renders under server-side rendering, so wrappers extend
`rx.Component` (not `rx.NoSSRComponent`). If a specific component must be
client-only in your setup, subclass it and switch its base to
`rx.NoSSRComponent`.

## dayjs / locale

`antd` bundles `dayjs` for date/time components — no extra install needed.
Localization beyond passing a `locale` dict to `config_provider` (importing
`antd/locale/*`) is out of scope for 0.1.0.

## Known limitations (0.1.0)

- Imperative `message` / `notification` / `Modal.confirm` are not wrapped.
- Date pickers exchange formatted strings, not native `datetime` objects.
- Not every antd prop is typed; unlisted props use `custom_attrs`.
