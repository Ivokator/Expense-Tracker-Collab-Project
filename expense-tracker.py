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




class InfoScreen(Screen):
    """Info screen for the expense tracker"""

    CSS_PATH = "expenseTracker.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()
        yield Label("""     

Contributers:
    - Jasper Wan
    

Python third-party packages used:
    - Textual 1.0.0
    
        """, classes="title")

    def on_mount(self) -> None:
        self.title = "Info"
        self.sub_title = "v0.0 | Python 3.12.4"



class ExpenseTrackerApp(App):

    CSS_PATH = "expenseTracker.tcss" # constant!

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




if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()
