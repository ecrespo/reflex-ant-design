# Contributing to reflex-ant-design

Thanks for your interest in improving this library! It wraps the
[Ant Design](https://ant.design) React components as
[Reflex](https://reflex.dev) components.

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) as the package manager.

```bash
git clone https://github.com/ecrespo/reflex-ant-design
cd reflex-ant-design
make install          # uv venv + editable install with dev deps
```

## Workflow

```bash
make lint             # ruff checks
make format           # ruff auto-fix
make test             # pytest
cd reflex_ant_design_demo && uv run reflex run   # try it live
```

## Adding or extending a component

1. Find the component in the [Ant Design docs](https://ant.design/components/overview)
   and note its props and events.
2. Add (or edit) the wrapper class in the matching module under
   `custom_components/reflex_ant_design/` (`general`, `layout`, `navigation`,
   `data_entry`, `data_display`, `feedback`).
3. Subclass `AntdComponent`, set `tag` (use a dotted tag like `Input.TextArea`
   for compound components), declare props as `rx.Var[...]`, and declare events
   as `rx.EventHandler[...]` with a spec that extracts a serializable payload.
4. Export a snake_case factory (`name = Name.create`) at the bottom of the
   module, and register it in `__init__.py` (`__all__`) and `namespace.py`.
5. Add a usage example to the demo app and a test in `tests/`.

Keep public classes and factories documented with Google-style docstrings; ruff
enforces this (`make lint`).

## Commit & PR

- Keep changes focused and update `CHANGELOG.md`.
- Make sure `make lint` and `make test` pass before opening a PR.
