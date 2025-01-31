from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, Static

class MainMenu(HorizontalGroup):
    """Main menu widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Button("View Expenses", id="view_expenses", classes="main_menu")
        yield Button("Info", id="info", classes="main_menu")
        yield Button("Exit Program", id="exit", classes="main_menu")

    