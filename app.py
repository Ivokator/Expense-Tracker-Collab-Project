from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, OptionList, Static, Tabs
from widgets.info_screen import InfoScreen
from widgets.main_menu import MainMenu
from widgets.view_expenses import AddExpense, DeleteExpense, ViewExpenses

import json


class ExpenseTrackerApp(App):

    CSS_PATH = "styles/expenseTracker.tcss" # constant!
    SCREENS = {
        "ViewExpenses": ViewExpenses,
        "AddExpense": AddExpense,
        "InfoScreen": InfoScreen,
        "DeleteExpense": DeleteExpense
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
        
        elif event.button.id:
            self.push_screen(event.button.id)
            
    @on(Button.Pressed, ".AddExpense")
    def expense_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed in view expenses menu"""

        if event.button.id:
            self.push_screen("AddExpense")
            self.query_one(AddExpense).category_name = str(event.button.id)

    @on(Button.Pressed, ".DeleteExpense")
    def delete_confirmation_static(self, event: Button.Pressed) -> None:
        """Called when the delete button is pressed."""
        if event.button.name:
            self.push_screen("DeleteExpense")

            self.query_one(DeleteExpense).expense_name = str(event.button.name)
            self.query_one(DeleteExpense).category_name = str(event.button.id) # str | None otherwise if without str()

    @on(Button.Pressed, "#cancel_delete")
    def cancel_delete(self, event: Button.Pressed) -> None:
        """Cancel the deletion of an expense."""
        self.app.pop_screen()
            

    @on(Button.Pressed, ".return_button")
    def go_back(self, event: Button.Pressed) -> None:
        """Return to the previous screen."""
        self.app.pop_screen()
    
    @on(OptionList.OptionSelected, ".time_period_option_list")
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_name = str(event.option.prompt)

        if option_name in ["All time", "This year", "This month", "This week"]:
            self.query_one(ViewExpenses).current_filter = option_name
        else:
            self.notify("Invalid option selected")

    @on(Tabs.TabActivated, ".main_tabs")
    def switch_main_tabs(self, event: Tabs.TabActivated) -> None:
        activated_tab = str(event.tab.id)
        self.notify(activated_tab)
        if event.tab is None:
            ...
        