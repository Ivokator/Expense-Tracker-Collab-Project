from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid, Container, HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
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
            yield Input(placeholder="Description")
            yield Input(placeholder="Date")
        with HorizontalGroup():
            yield Button("Add", classes="add_expense")
            yield Button("Return", classes="return_button add_expense")


class DeleteExpense(ModalScreen):
    """A widget to confirm deletion of an expense."""

    category_name = reactive("this category")
    expense_name = reactive("this expense") # yes, formatted like this

    def compose(self) -> ComposeResult:
        with Static(f"Are you sure you want to delete [bold italic]{self.expense_name}[/]?", id="delete_confirmation_static"):
            yield Button("Yes", variant="error", id="confirm_delete")
            yield Button("No", variant="primary", id="cancel_delete")

    @on(Button.Pressed, "#confirm_delete")
    def confirm_delete(self, event: Button.Pressed) -> None:
        """Delete an expense."""

        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)


            #TODO: Find a better way to find the expense to delete in the JSON file.
            category = data['categories'][self.category_name]
            for i in range(len(category)):
                if category[i]['name'] == self.expense_name:
                    category.pop(i)
                    break

            with open('user_data/expenses.json', 'w') as file:
                json.dump(data, file, indent=4, sort_keys=True, separators=(',', ': '))
        self.app.pop_screen()
        self.app.push_screen(ViewExpenses()) # dammit, this is a hacky way to update the ViewExpenses screen

    

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
                        with Collapsible(title=f"{expense['name']}", classes="expense_collapsible"):
                            yield Label(f"Amount: ${expense['amount']:.2f}")
                            yield Label(f"Date: {expense['date']}")
                            yield Rule(line_style="heavy")

                            if expense['description']:
                                yield Label(expense['description'])
                        
                            yield Button("Delete", id=category, classes="DeleteExpense", name=expense['name']) # absolutely trash disgusting code but it works
                            
                    yield Button("Add an expense", id="AddExpense", classes="expense_button")
                    

        yield Button("Return", classes="return_button")

        

    def on_mount(self) -> None:
        self.title = "Your Expenses"
