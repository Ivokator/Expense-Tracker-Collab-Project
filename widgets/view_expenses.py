from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Digits, Footer, Header, Label, Static


class ExpenseCategory(Widget):
        def __init__(self, category):
                self.category = category
        def compose(self) -> ComposeResult:
                yield Collapsible(title=category)
class ViewExpenses(Screen):

        def compose(self) -> ComposeResult:
                yield Button("Add a category", id="add_category")
        
        def on_button_pressed(self, event: Button.Pressed) -> None:
                if event.button.id == "add_category":
                        widget = ExpenseCategory()
                        widget.run()
