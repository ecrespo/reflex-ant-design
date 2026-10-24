# reflex-ant-design — developer tasks (uv-based)
#
# Usage: make <target>. All Python commands run inside the uv-managed venv.

.PHONY: help install dev lint format test demo build publish clean

help:
	@echo "install   Create the venv and install the package (editable) + dev deps"
	@echo "dev       Alias for install"
	@echo "lint      Run ruff checks"
	@echo "format    Auto-fix lint/format issues with ruff"
	@echo "test      Run the pytest suite"
	@echo "demo      Run the demo app (reflex run)"
	@echo "build     Regenerate the .pyi stubs and build the wheel + sdist"
	@echo "publish   Publish to PyPI with uv (needs credentials)"
	@echo "clean     Remove build artifacts and caches"

install:
	uv venv
	uv pip install -e ".[dev]"

dev: install

lint:
	uv run ruff check custom_components tests

format:
	uv run ruff check --fix custom_components tests

test:
	uv run pytest -q

demo:
	cd reflex_ant_design_demo && uv run reflex run

build:  # Reflex 0.10 removed `reflex component build`
	uv run python -m reflex_base.utils.pyi_generator custom_components/reflex_ant_design
	uv build

publish: build
	uv publish

clean:
	rm -rf dist build *.egg-info custom_components/*.egg-info \
		.pytest_cache .ruff_cache .web .states
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
