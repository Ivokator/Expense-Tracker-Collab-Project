from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Grid, Container, HorizontalGroup, VerticalGroup, VerticalScroll
from textual.validation import Function, Number, ValidationResult, Validator
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Collapsible, ContentSwitcher, Digits, Footer, Header, Input, Label, ListItem, ListView, OptionList, Rule, Static, Tab, Tabs, Tree
from textual_plotext import PlotextPlot

import re
import json
from datetime import datetime


class AddExpense(Screen):
    """A widget to add an expense."""

    #Do NOT touch this code, if it breaks, it breaks. I'm not fixing it.
        # 2025-02-18: haha i did

    category_name = reactive("this category")

    valid_name: bool = False
    valid_amount: bool = False
    valid_date: bool = False

    

    def compose(self) -> ComposeResult:

        yield Header()
        yield Footer()
        with VerticalGroup(classes="add_expense_group"):
            self.expense_input = Input(
                placeholder="Expense name", 
                valid_empty=False, 
                id="expense_name",
                validators=[
                    IsNotEmpty()
                ]
                )
            self.amount_input = Input(
                id="expense_amount",
                placeholder="Amount",
                validators=[
                    IsValidCurrency(),
                    IsNotEmpty()
                    ]
                )
            self.description_input = Input(placeholder="Description")
            self.date_input = Input(
                placeholder="Date of expense (YYYY-MM-DD)", 
                max_length=10,
                id="expense_date",
                validators=[
                    IsValidDate(),
                    IsNotEmpty()
                        ]
                                    ) #TODO: Add a date picker
            

            yield self.expense_input
            yield self.amount_input
            yield self.description_input
            yield self.date_input

        with HorizontalGroup():
            yield Button("Add", classes="add_expense", id="add_expense_button")
            yield Button("Return", classes="return_button add_expense")


    @on(Button.Pressed, "#add_expense_button")
    def check_expense(self, event: Button.Pressed) -> None:
        if self.valid_name and self.valid_amount and self.valid_date:
            self.add_expense()
        else:
            self.app.push_screen("ErrorScreen")

    # most efficient way :)
    @on(Input.Changed, "#expense_name")
    def on_name_changed(self, event: Input.Changed) -> None:

        if event.validation_result and event.validation_result.is_valid:
            self.valid_name = True
        else:
            if event.validation_result:
                self.notify(str(event.validation_result.failure_descriptions))
            self.valid_name = False

    @on(Input.Changed, "#expense_amount")
    def on_amount_changed(self, event: Input.Changed) -> None:

        if event.validation_result and event.validation_result.is_valid:
            self.valid_amount = True
        else:
            self.valid_amount = False

    @on(Input.Changed, "#expense_date")
    def on_date_changed(self, event: Input.Changed) -> None:

        if event.validation_result and event.validation_result.is_valid:
            self.valid_date = True
        else:
            self.valid_date = False

    def add_expense(self):
        
        expense = {
            "name": self.expense_input.value,
            "amount": float(self.amount_input.value.lstrip("$")),
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


class IsNotEmpty(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value:
            return self.success()
        else:
            return self.failure("Value cannot be empty.")

class IsValidCurrency(Validator):
    def validate(self, value: str) -> ValidationResult:

        # Input may have a '$' symbol
        stripped_value = value.lstrip("$")

        try:
            float(stripped_value)
            return self.success()
        except ValueError:
            return self.failure("Invalid number!")

class IsValidDate(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            datetime.fromisoformat(value)
            return self.success()
        except ValueError:
            return self.failure("Invalid date!")

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

class DeleteCategory(ModalScreen):

    category_name = reactive("this category", recompose=True)

    def compose(self) -> ComposeResult:
        with Static(f"Are you sure you want to delete [bold italic]{self.category_name}[/]?", id="delete_confirmation_static"):
            yield Button("Yes", variant="error", id="confirm_delete")
            yield Button("No", variant="primary", id="cancel_delete")

            
    @on(Button.Pressed, "#confirm_delete")
    def delete_category(self, event: Button.Pressed) -> None:
        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)
            data['categories'].pop(self.category_name)

        with open('user_data/expenses.json', 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True, separators=(',', ': '))

        self.app.pop_screen()
        self.app.push_screen(ViewExpenses())


class ErrorScreen(ModalScreen):
    """Error screen for invalid inputs"""

    def compose(self) -> ComposeResult:
        with Static(f"Error: Invalid input", id="error_static"):
            yield Button("Return", variant="primary", classes="return_button")



class IsValidJSONID(Validator):
    def validate(self, value: str) -> ValidationResult:
        disallowed_characters = re.compile('[^a-zA-Z0-9]')
        if disallowed_characters.findall(value):
            return self.failure("Invalid character!")
        return self.success()
        
class CheckUniqueCategory(Validator):
    """Check if category already exists."""
    def validate(self, value: str) -> ValidationResult:
        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)
            if value in data['categories']:
                return self.failure("Category already exists!")
            else:
                return self.success()

class AddCategory(Screen):
    valid_input: bool = False

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            self.category_name = Input(placeholder="Category name", id="add_category_input",validators=[IsValidJSONID(), CheckUniqueCategory()]) 

            yield self.category_name

        with HorizontalGroup():
            yield Button("Add", classes="add_expense", id="add_category")
            yield Button("Return", classes="return_button")
    
    @on(Button.Pressed, "#add_category")
    def on_add_category(self, event: Button.Pressed) -> None:
        if self.valid_input:
            self.add_category()
    
    @on(Input.Changed, "#add_category_input")
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.validation_result and event.validation_result.is_valid:
            self.valid_input = True
        else:
            self.valid_input = False

    def add_category(self):
        with open('user_data/expenses.json', 'r+') as file:
            data = json.load(file)
            data['categories'][str(self.category_name.value)] = []
            file.seek(0)
            json.dump(data, file, indent=4, sort_keys=True, separators=(',', ': '))
            file.truncate()

        self.app.pop_screen()
        self.app.push_screen(ViewExpenses())


class ViewExpenses(Screen):

    current_filter = reactive("option_all_time", recompose=True)
    activated_tab = reactive("basic_tab", recompose=True)

    def compose(self) -> ComposeResult:

        yield Tabs(
            Tab("Expenses", id="basic_tab"), 
            Tab("Summary", id="summary_tab"), 
            Tab("Spending Trends", id="spending_trends_tab"), 
            
            classes="main_tabs")


        # Load the expenses from the JSON file
        with open('user_data/expenses.json', 'r') as file:
            data = json.load(file)
            total_expenses: float | int = 0

            year_expenses: float | int = 0
            month_expenses: float | int = 0
            week_expenses: float | int = 0

            tree: Tree[str] = Tree("All Expenses", classes="expenses_tree")
            tree.root.expand()
            
            with (basic_tab := Static(classes="expense_static expense_tabbed", id="basic_tab")):
                with VerticalScroll():
                    for category in data['categories']:
                        tree_category = tree.root.add(category)

                        with (category_collapsible := Collapsible(title=category, classes="category_collapsible")):
                            for expense in data['categories'][category]:  # 'expense' is the most inner dictionary
                                
                                expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
                                current_date = datetime.now()

                                include_expense: bool
                                diminish_category: bool = True
                                filter_index: int = 0
                                
                                if self.current_filter == "option_all_time":
                                    include_expense, filter_index = True, 0
                                elif self.current_filter == "option_this_year":
                                    include_expense, filter_index = is_expense_this_year(expense_date, current_date)
                                elif self.current_filter == "option_this_month":
                                    include_expense, filter_index = is_expense_this_month(expense_date, current_date)
                                elif self.current_filter == "option_this_week":
                                    include_expense, filter_index = is_expense_this_week(expense_date, current_date)
                                else:
                                    include_expense = False

                                if is_expense_this_year(expense_date, current_date)[0]:
                                    year_expenses += expense['amount']

                                    if is_expense_this_month(expense_date, current_date)[0]:
                                        month_expenses += expense['amount']

                                        if is_expense_this_week(expense_date, current_date)[0]:
                                            week_expenses += expense['amount']

                                total_expenses += expense['amount']
                                tree_category.add_leaf(expense['name'])

                                if include_expense:
                                    diminish_category = False
                                    
                                    with Collapsible(title=f"{expense['name']}", classes="expense_collapsible"):
                                        yield Label(f"Amount: ${expense['amount']:.2f}")
                                        yield Label(f"Date: {expense['date']}")
                                        yield Rule(line_style="heavy")

                                        if expense['description']:
                                            yield Label(expense['description'])

                                        yield Button("Delete", id=category, variant="error", classes="DeleteExpense", name=expense['name']) # absolutely trash disgusting code but it works
                                    

                            if diminish_category:
                                category_collapsible.add_class("diminish_category")
                                yield Label("No expenses in this category.", classes="no_expenses_label")
                            
                            with HorizontalGroup(classes="category_options"):

                                yield Button("Add an expense", id=category, classes="AddExpense")
                                yield Button("Delete category", variant="error", classes="delete_category_button", name=category)

                with Static(id="expense_side_bar"):
                        # Filter time period
                        yield Label("Filter by time\n", classes="side_bar_label")


                        yield ListView(
                            ListItem(Label("All time"), id="option_all_time"),
                            ListItem(Label("This year"), id="option_this_year"),
                            ListItem(Label("This month"), id="option_this_month"),
                            ListItem(Label("This week"), id="option_this_week"),
                            classes="time_period_list_view",
                            initial_index=filter_index
                        )

            yield SummaryTab(total_expenses, year_expenses, month_expenses, week_expenses)
            
            # Spending Trends tab
            with (spending_trends_tab := Static(classes="expense_tabbed", id="spending_trends_tab")):
                yield Tabs(
                    Tab("This Year", id="this_year_tab"),
                    Tab("This Month", id="this_month_tab"),
                    Tab("This Week", id="this_week_tab"),
                    classes="spending_trends_tabs"
                )

                # This Month tab
                with (this_month_tab := Static(classes="spending_trends_tabbed", id="this_month_tab")):
                    plot = PlotextPlot()
                    plt = plot.plt

                    this_month_expenses = [0] * 30
                    current_date = datetime.now()
                    for category in data['categories']:
                        for expense in data['categories'][category]:
                            expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
                            days_diff = (current_date - expense_date).days
                            if 0 <= days_diff < 30:
                                index = 29 - days_diff
                                if 0 <= index < len(this_month_expenses):
                                    this_month_expenses[index] += expense['amount']
                                else:
                                    this_month_expenses[index] = 0

                    # Plot the expenses
                    plt.plot(this_month_expenses)
                    plt.title("Expenses in the Last 30 Days")
                    plt.xlabel("Days")
                    plt.ylabel("Amount ($)")
                    plt.xticks(range(30))
                    yield plot

                # This Year tab
                with (this_year_tab := Static(classes="spending_trends_tabbed", id="this_year_tab")):
                    plot = PlotextPlot()
                    plt = plot.plt
                    this_year_expenses = [0] * 12
                    current_date = datetime.now()

                    for category in data['categories']:
                        for expense in data['categories'][category]:
                            expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
                            
                            months_diff = (current_date.year - expense_date.year) * 12 + (current_date.month - expense_date.month)
                            
                            if 0 <= months_diff < 12:
                                index = 11 - months_diff
                                if 0 <= index < len(this_year_expenses):
                                    this_year_expenses[index] += expense['amount']
                                else:
                                    this_year_expenses[index] = 0

                    # Plot the expenses
                    plt.plot(this_year_expenses)
                    plt.title("Expenses This Year")
                    plt.xlabel("Months")
                    plt.ylabel("Amount ($)")
                    plt.xticks(range(12))
                    yield plot

                # This Week tab
                with (this_week_tab := Static(classes="spending_trends_tabbed", id="this_week_tab")):
                    plot = PlotextPlot()
                    plt = plot.plt

                    this_week_expenses = [0] * 7
                    current_date = datetime.now()
                    for category in data['categories']:
                        for expense in data['categories'][category]:
                            expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
                            days_diff = (current_date - expense_date).days
                            if 0 <= days_diff < 7:
                                index = 6 - days_diff
                                if 0 <= index < len(this_week_expenses):
                                    this_week_expenses[index] += expense['amount']
                                else:
                                    this_week_expenses[index] = 0

                    # Plot the expenses
                    plt.plot(this_week_expenses)
                    plt.title("Expenses This Week")
                    plt.xlabel("Days")
                    plt.ylabel("Amount ($)")
                    plt.xticks(range(7))
                    yield plot



            # Always left-docked side bar
            with Static(classes="side_bar", id="docked_side_bar"):
                with VerticalScroll():
                    
                    yield Rule(line_style="heavy")
                    yield tree
                    yield Rule(line_style="heavy")

                
                yield Button("Add a category", classes="add_category_button")
                yield Button("Return", classes="return_button")
                    
        yield Header()
        yield Footer()

class SummaryTab(Static):
    def __init__(self, 
                 total_expenses: float | int, 
                 year_expenses: float | int, 
                 month_expenses: float | int, 
                 week_expenses: float | int) -> None:
        
        super().__init__()
        self.total_expenses = total_expenses
        self.year_expenses = year_expenses
        self.month_expenses = month_expenses
        self.week_expenses = week_expenses

        self.id = "summary_tab"
        self.classes = "expense_tabbed"
    
    def compose(self) -> ComposeResult:
        with HorizontalGroup(classes="expense_digits_by_time"):
            with Static():
                yield Label("Total expenses", classes="side_bar_label")
                yield Digits(f"${self.total_expenses:,.2f}", id="total_expense_digits")
            
            with Static():
                yield Label("This year's expenses", classes="side_bar_label")
                yield Digits(f"${self.year_expenses:,.2f}", id="year_expense_digits", classes="filtered_expense_digits")
                
            with Static():
                yield Label("This month's expenses", classes="side_bar_label")
                yield Digits(f"${self.month_expenses:,.2f}", id="month_expense_digits", classes="filtered_expense_digits")

            with Static():
                yield Label("This week's expenses", classes="side_bar_label")
                yield Digits(f"${self.week_expenses:,.2f}", id="week_expense_digits", classes="filtered_expense_digits")

        yield VerticalScroll()



# functions, fns, funcs, unions, etc.

def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False



def is_expense_this_year(expense_date: datetime, current_date: datetime) -> tuple[bool, int]:
    return expense_date.year == current_date.year, 1

def is_expense_this_month(expense_date: datetime, current_date: datetime) -> tuple[bool, int]:
    return expense_date.year == current_date.year and expense_date.month == current_date.month, 2

def is_expense_this_week(expense_date: datetime, current_date: datetime) -> tuple[bool, int]:
    # isocalendar() returns a tuple (year, week number, weekday)
    return expense_date.isocalendar()[1] == current_date.isocalendar()[1] and expense_date.year == current_date.year, 3