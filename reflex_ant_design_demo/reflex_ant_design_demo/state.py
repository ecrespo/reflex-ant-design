"""State for the reflex-ant-design demo app.

Holds the interactive values bound to the Ant Design components across the
demo pages: form fields, a switch/slider, the selected table rows and the
modal/drawer open flags.
"""

from __future__ import annotations

import reflex as rx


class DemoState(rx.State):
    """Shared state driving the interactive examples."""

    # --- Data entry bindings ------------------------------------------------
    name: str = ""
    bio: str = ""
    country: str = "us"
    newsletter: bool = True
    volume: int = 30
    rating: float = 3.0
    color: str = "#1677ff"
    birthday: str = ""

    # --- Feedback / overlay flags ------------------------------------------
    modal_open: bool = False
    drawer_open: bool = False

    # --- Navigation ---------------------------------------------------------
    active_tab: str = "overview"
    current_step: int = 1
    affixed: bool = False

    # --- Data display -------------------------------------------------------
    selected_date: str = ""

    # --- Theme --------------------------------------------------------------
    primary_color: str = "#1677ff"
    dark: bool = False

    @rx.event
    def set_name(self, value: str):
        """Update the name field."""
        self.name = value

    @rx.event
    def set_bio(self, value: str):
        """Update the bio field."""
        self.bio = value

    @rx.event
    def set_country(self, value: str):
        """Update the selected country."""
        self.country = value

    @rx.event
    def toggle_newsletter(self, value: bool):
        """Toggle the newsletter switch."""
        self.newsletter = value

    @rx.event
    def set_volume(self, value: int):
        """Update the slider volume."""
        self.volume = value

    @rx.event
    def set_rating(self, value: float):
        """Update the star rating."""
        self.rating = value

    @rx.event
    def set_color(self, value: str):
        """Update the picked color."""
        self.color = value

    @rx.event
    def set_birthday(self, value: str):
        """Update the date picker value (formatted string)."""
        self.birthday = value

    @rx.event
    def open_modal(self):
        """Open the modal dialog."""
        self.modal_open = True

    @rx.event
    def close_modal(self):
        """Close the modal dialog."""
        self.modal_open = False

    @rx.event
    def set_drawer(self, value: bool):
        """Set the drawer open state."""
        self.drawer_open = value

    @rx.event
    def set_active_tab(self, value: str):
        """Switch the active tab."""
        self.active_tab = value

    @rx.event
    def set_step(self, value: int):
        """Set the current step in the Steps component."""
        self.current_step = value

    @rx.event
    def set_affixed(self, value: bool):
        """Track whether the Affix element is currently pinned."""
        self.affixed = value

    @rx.event
    def set_selected_date(self, value: str):
        """Store the Calendar's selected date (ISO string)."""
        self.selected_date = value

    @rx.event
    def set_primary_color(self, value: str):
        """Update the ConfigProvider primary color token."""
        self.primary_color = value

    @rx.event
    def toggle_dark(self, value: bool):
        """Toggle dark mode."""
        self.dark = value

    @rx.var
    def greeting(self) -> str:
        """A greeting derived from the name field."""
        return f"Hello, {self.name}!" if self.name else "Hello, stranger!"

    @rx.var
    def theme_config(self) -> dict:
        """The antd theme dict fed to ConfigProvider.

        Only design *tokens* are set here, which are plain JSON. Switching the
        dark/light *algorithm* needs the antd ``theme.darkAlgorithm`` function
        reference (not a string); see ``docs/guides/usage.md`` for how to wire
        that with custom code.
        """
        return {"token": {"colorPrimary": self.primary_color, "borderRadius": 8}}
