from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, ListView, OptionList, Static, Tabs
from widgets.info_screen import InfoScreen
from widgets.main_menu import MainMenu
from widgets.view_expenses import AddCategory, AddExpense,  DeleteCategory, DeleteExpense, ErrorScreen, SummaryTab, ViewExpenses

import json


class ExpenseTrackerApp(App):

    CSS_PATH = "styles/expenseTracker.tcss" # constant!
    SCREENS = {
        "ViewExpenses": ViewExpenses,
        "AddExpense": AddExpense,
        "InfoScreen": InfoScreen,
        "DeleteExpense": DeleteExpense,
        "AddCategory": AddCategory,
        "DeleteCategory": DeleteCategory,
        "ErrorScreen": ErrorScreen
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
    
    @on(ListView.Selected, ".time_period_list_view")
    def on_list_view_option_selected(self, event: ListView.Selected) -> None:
        option_name = str(event.item.id)
        expense_screen = self.query_one(ViewExpenses)

        if option_name in ["option_all_time", "option_this_year", "option_this_month", "option_this_week"]:
            expense_screen.current_filter = option_name
        else:
            self.notify("Invalid option selected")

    @on(Tabs.TabActivated, ".main_tabs")
    def switch_main_tabs(self, event: Tabs.TabActivated) -> None:
        activated_tab = str(event.tab.id)
        current_tab = self.query_one(ViewExpenses).children

        for widget in current_tab:
            if isinstance(widget, (Static, SummaryTab)):
                if widget.id == activated_tab or widget.id == "docked_side_bar":
                    widget.remove_class("hidden") # <--- damn this is very smart 
                else:
                    widget.add_class("hidden")

    @on(Tabs.TabActivated, ".spending_trends_tabs")
    def switch_spending_trends_tabs(self, event: Tabs.TabActivated) -> None:
        activated_tab = str(event.tab.id)
        spending_trends_tabs = self.query_one(ViewExpenses).query(".spending_trends_tabbed")

        for widget in spending_trends_tabs:
            if widget.id == activated_tab:
                widget.remove_class("hidden") 
            else:
                widget.add_class("hidden")
        
    @on(Button.Pressed, ".add_category_button")
    def add_category_button(self, event: Button.Pressed) -> None:

        self.push_screen("AddCategory")

    @on(Button.Pressed, ".delete_category_button")
    def delete_category_screen(self, event: Button.Pressed) -> None:
        self.push_screen("DeleteCategory")
        self.query_one(DeleteCategory).category_name = str(event.button.name)

    def invalid_input_error(self) -> None:
        self.push_screen("ErrorScreen")

