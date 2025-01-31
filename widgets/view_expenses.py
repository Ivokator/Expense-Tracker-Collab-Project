from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, Static

class ViewExpenses(Screen):
        
        def compose(self) -> ComposeResult:
                yield Button("Button")
