from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalGroup, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, Header, Label, Static

class InfoScreen(Screen):
    """Info screen for the expense tracker"""

    CSS_PATH = "../styles/expenseTracker.tcss"
    

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()
        yield Container(Label("""  

Created on Jan. 29, 2025.

Contributers:
    - Jasper Wan
    - Andrii Aksonov

Python third-party packages used:
    - Textual 1.0.0
    - Textual-plotext 1.0.0
    
        """), id="info")

        yield Button("Return", classes="return_button")
        

    def on_mount(self) -> None:
        self.title = "Info"
        self.sub_title = "v0.0 | Python 3.12.4"