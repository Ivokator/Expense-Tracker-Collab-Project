from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid, HorizontalGroup, VerticalGroup, VerticalScroll
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Digits, Footer, Header, Label, Rule, Static, Collapsible, Input

import json


class AddExpense(Screen):
    def compose(self) -> ComposeResult:

        yield Header()
        yield Footer()
        with VerticalGroup():
            yield Input(placeholder="Expense")
            yield Input(placeholder="Amount")
            yield Input(placeholder="description")
            yield Input(placeholder="date")
        with HorizontalGroup():
            yield Button("Add", classes="add_expense")
            yield Button("Return", classes="return_button add_expense")

class ViewExpenses(Screen):

    def compose(self) -> ComposeResult:
        
        yield Header()
        yield Footer()
        yield VerticalScroll()

        # Load the expenses from the JSON file
        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)
            for category in data['categories']:
                with Collapsible(title=category, classes="category_collapsible"):
                    for expense in data['categories'][category]:  # 'expense' is the most inner dictionary
                        with Collapsible(title=f"{expense['name']}"):
                            yield Label(f"Amount: ${expense['amount']:.2f}")
                            yield Label(f"Date: {expense['date']}")
                            yield Rule(line_style="heavy")
                            if expense['description']:
                                yield Label(expense['description'])
                    yield Button("+", id="AddExpense", classes="expense_button")

        yield Button("Return", classes="return_button")

    def on_mount(self) -> None:
        self.title = "Your Expenses"
