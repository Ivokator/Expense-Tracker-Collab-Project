from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, Static

from widgets.info_screen import InfoScreen
from widgets.main_menu import MainMenu


class ExpenseTrackerApp(App):

    CSS_PATH = "styles/expenseTracker.tcss" # constant!

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()
        yield VerticalScroll(MainMenu())

    def on_mount(self) -> None:
        self.title = "Expenses Tracker App"


    @on(Button.Pressed, ".main_menu")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        if event.button.id == "view_expenses":
            ...
        elif event.button.id == "info":
            self.push_screen(InfoScreen())
        elif event.button.id == "exit":
            ...