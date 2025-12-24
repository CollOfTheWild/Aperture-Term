from textual.app import ComposeResult
from textual.widgets import Static

class ContextSwarm(Static):
    """
    [Top-Right] Search & RAG Tools
    Handles async context fetching.
    """
    BORDER_TITLE = "CONTEXT SWARM [2]"

    def compose(self) -> ComposeResult:
        yield Static("[blink]SCANNING INPUT...[/blink]")