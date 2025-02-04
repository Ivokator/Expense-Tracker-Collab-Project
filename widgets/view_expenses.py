from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Digits, Footer, Header, Label, Static, Collapsible


class ExpenseCategory(Widget):
        
        def __init__(self, category):
                super().__init__()
                self.category = category
                
        def compose(self) -> ComposeResult:
                with Collapsible(title=self.category):
                        yield Button("add expenses")
                        
class ViewExpenses(Screen):

        def compose(self) -> ComposeResult:
                yield Header()
                yield Footer()
                yield VerticalScroll()
                
                yield ExpenseCategory("Food")
                yield ExpenseCategory("Housing")
                yield ExpenseCategory("Transportation")
                yield ExpenseCategory("Healthcare") 
                yield ExpenseCategory("Entertainment")
                yield ExpenseCategory("Clothing")
                yield ExpenseCategory("Education")
                yield ExpenseCategory("Insurance")
                
                def action_collapse_or_expand(self, collapse: bool) -> None:
                        for child in self.walk_children(Collapsible):
                                child.collapsed = collapse