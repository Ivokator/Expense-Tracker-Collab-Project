from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Grid, Container, HorizontalGroup, VerticalGroup, VerticalScroll
from textual.validation import Function, Number, ValidationResult, Validator
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Collapsible, ContentSwitcher, Digits, Footer, Header, Input, Label, OptionList, Rule, Static, Tab, Tabs, Tree




import json
from datetime import datetime

class AddExpense(Screen):
    """A widget to add an expense."""

    #Do NOT touch this code, if it breaks, it breaks. I'm not fixing it.

    category_name = reactive("this category")

    def compose(self) -> ComposeResult:

        yield Header()
        yield Footer()
        with VerticalGroup():
            self.expense_input = Input(placeholder="Expense")
            self.amount_input = Input(
                placeholder="Amount",
                validators=[
                    Function(is_integer)
                    ]
                )
            self.description_input = Input(placeholder="Description")
            self.date_input = Input(placeholder="Date (year-month-day)") #TODO: Add a date picker
            yield self.expense_input
            yield self.amount_input
            yield self.description_input
            yield self.date_input

        with HorizontalGroup():
            yield Button("Add", classes="add_expense", id="add_expense_button")
            yield Button("Return", classes="return_button add_expense")


    @on(Button.Pressed, "#add_expense_button")
    def check_expense(self, event: Button.Pressed) -> None:
        
        if is_integer(self.amount_input.value) == False:
            self.app.push_screen(ErrorScreen())
        else:
            self.add_expense()

        
    def add_expense(self):
        
        expense = {
            "name": self.expense_input.value,
            "amount": float(self.amount_input.value),
            "description": self.description_input.value,
            "date": self.date_input.value
        }
        
        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)

        if self.category_name not in data['categories']:
            data['categories'][self.category_name] = []

        data['categories'][self.category_name].append(expense)

        with open('user_data/expenses.json', 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True, separators=(',', ': ')) #I swear i did not copied the code down below from the DeleteExpense class, okay i did.

        self.app.pop_screen()
        self.app.push_screen(ViewExpenses())

class DeleteExpense(ModalScreen):
    """A widget to confirm deletion of an expense."""

    category_name = reactive("this category", recompose=True)
    expense_name = reactive("this expense", recompose=True) # yes, formatted like this

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
        
class ErrorScreen(ModalScreen):
    
    def compose(self) -> ComposeResult:
        with Static("Error: Invalid input", id="error_static"):
            yield Button("Return", variant="primary", classes="return_button")
        
    
class ViewExpenses(Screen):

    current_filter = reactive("All time", recompose=True)
    activated_tab = reactive("tab-1", recompose=True)

    def compose(self) -> ComposeResult:
        
        
        yield VerticalScroll()
        yield Tabs(
            Tab("Basic", id="basic_tab"), 
            Tab("Summary", id="summary_tab"), 
            Tab("Spending Trends", id="spending_trends_tab"), 
            
            classes="main_tabs")


        # Load the expenses from the JSON file
        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)
            total_expenses: float = 0

            tree: Tree[str] = Tree("All Expenses", classes="expenses_tree")
            tree.root.expand()


            
            with (basic_tab := Static(classes="expense_static")):
                for category in data['categories']:
                    tree_category = tree.root.add(category)

                    with (category_collapsible := Collapsible(title=category, classes="category_collapsible")):
                        for expense in data['categories'][category]:  # 'expense' is the most inner dictionary
                            
                            expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
                            current_date = datetime.now()

                            include_expense: bool
                            diminish_category: bool = True

                            if self.current_filter == "All time":
                                include_expense = True
                            elif self.current_filter == "This year":
                                include_expense = expense_date.year == current_date.year
                            elif self.current_filter == "This month":
                                include_expense = expense_date.year == current_date.year and expense_date.month == current_date.month
                            elif self.current_filter == "This week":
                                # isocalendar() returns a tuple (year, week number, weekday)
                                include_expense = expense_date.isocalendar()[1] == current_date.isocalendar()[1] and expense_date.year == current_date.year
                            else:
                                include_expense = False

                            total_expenses += expense['amount']

                            if include_expense:
                                diminish_category = False
                                
                                tree_category.add_leaf(expense['name'])

                                with Collapsible(title=f"{expense['name']}", classes="expense_collapsible"):
                                    yield Label(f"Amount: ${expense['amount']:.2f}")
                                    yield Label(f"Date: {expense['date']}")
                                    yield Rule(line_style="heavy")

                                    if expense['description']:
                                        yield Label(expense['description'])

                                    yield Button("Delete", id=category, classes="DeleteExpense", name=expense['name']) # absolutely trash disgusting code but it works
                                

                        if diminish_category:
                            category_collapsible.add_class("diminish_category")
                            yield Label("No expenses in this category.", classes="no_expenses_label")

                        yield Button("Add an expense", id=category, classes="AddExpense")

            with (summary_tab := Static(classes="")):
                ...
            
            with (spending_trends_tab := Static(classes="")):
                ...

            with Static(classes="side_bar"):
                with VerticalScroll():
                    yield Label("Total expenses", classes="side_bar_label")
                    yield Digits(str(total_expenses), id="total_expense_digits")
                    yield Rule(line_style="heavy")
                    yield tree
                    yield Rule(line_style="heavy")

                    # Filter time period
                    yield Label("Filter by time", classes="side_bar_label")

                    yield OptionList(
                        "All time",
                        "This year",
                        "This month",
                        "This week",
                        classes="time_period_option_list"
                    )

                yield Button("Return", classes="return_button")

        yield Header()
        yield Footer()



class SummaryTab(Static):
    def on_mount(self):
        ...




# union

def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False

    def on_mount(self) -> None:
        self.title = "Your Expenses"
