from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, Static
from widgets.info_screen import InfoScreen
from widgets.main_menu import MainMenu
from widgets.view_expenses import AddExpense, ViewExpenses

class ExpenseTrackerApp(App):

    CSS_PATH = "styles/expenseTracker.tcss" # constant!
    SCREENS = {
        "ViewExpenses": ViewExpenses,
        "AddExpense": AddExpense,
        "InfoScreen": InfoScreen,
    }
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()
        yield VerticalScroll(MainMenu())

    def on_mount(self) -> None:
        self.title = "Expenses Tracker App"


    @on(Button.Pressed, ".main_menu")
    def main_menu_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed in main menu."""

        if event.button.id == "exit":
            self.app.exit()
            return
        
        if event.button.id is not None:
            self.push_screen(event.button.id)
            
    @on(Button.Pressed, ".expense_button")
    def view_expenses_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed in view expenses menu"""
        
        if event.button.id is not None:
            self.push_screen(event.button.id)
    
    @on(Button.Pressed, ".return_button")
    def go_back(self, event: Button.Pressed) -> None:
        """Return to the previous screen."""
        self.app.pop_screen()
        

    