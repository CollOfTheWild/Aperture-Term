from textual.app import ComposeResult
from textual.widgets import Static

class Armory(Static):
    """
    [Top-Left] Model Loader & Config
    Displays model list and Neofetch card.
    """
    BORDER_TITLE = "THE ARMORY [1]"

    def compose(self) -> ComposeResult:
        yield Static("[b]META[/b] Llama-3.2-1B-Instruct\n[dim]Quant: Q4_K_M[/dim]")