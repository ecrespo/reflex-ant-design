"""Reflex configuration for the reflex-ant-design demo app."""

import reflex as rx

config = rx.Config(
    app_name="reflex_ant_design_demo",
    # The demo uses rx.* layout components; load the Radix CSS explicitly.
    plugins=[rx.plugins.RadixThemesPlugin()],
)
