from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, Static

from widgets.info_screen import InfoScreen
from widgets.main_menu import MainMenu
from widgets.view_expenses import ViewExpenses


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
            self.push_screen(ViewExpenses())
        elif event.button.id == "info":
            self.push_screen(InfoScreen())
        elif event.button.id == "exit":
            self.app.exit()
            
    @on(Button.Pressed, ".info_screen")
    def go_back(self, event: Button.Pressed) -> None:
        if event.button.id == "return_button":
            self.app.pop_screen()
            
    def action_collapse_or_expand(self, collapse: bool) -> None:
        for child in self.walk_children(Collapsible):
            child.collapsed = collapse