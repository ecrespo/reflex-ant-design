"""Catalog-level tests: every exported factory exists and renders."""

from __future__ import annotations

import reflex_ant_design as rad
from reflex_ant_design import antd

# Factories that need a required argument and cannot be called bare.
_NEEDS_ARG = {"icon"}


def test_namespace_matches_flat_exports():
    ns_names = {a for a in dir(antd) if not a.startswith("_")}
    flat_names = set(rad.__all__)
    # Every namespaced factory (except aliases) is also a flat export, modulo a
    # couple of intentional renames (list -> list_view).
    missing = ns_names - flat_names - {"list", "app", "config_provider"}
    assert not missing, f"namespace factories missing from __all__: {missing}"


def test_all_namespace_factories_render():
    rendered = 0
    for name in (a for a in dir(antd) if not a.startswith("_")):
        if name in _NEEDS_ARG:
            continue
        factory = getattr(antd, name)
        component = factory()
        assert component.render(), name
        rendered += 1
    assert rendered >= 90


def test_icon_factory_renders_and_imports_icons_package():
    component = antd.icon("SearchOutlined", spin=True)
    assert component.render()
    assert any("icons" in key for key in component._get_all_imports())


def test_version_exposed():
    assert rad.__version__
    assert rad.ANTD_VERSION.startswith("antd@")
