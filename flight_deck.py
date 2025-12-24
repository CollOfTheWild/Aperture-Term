from textual.app import ComposeResult
from textual.widgets import Static

class FlightDeck(Static):
    """
    [Bot-Left] Chat Interface
    Main user interaction point.
    """
    BORDER_TITLE = "FLIGHT DECK [3]"

    def compose(self) -> ComposeResult:
        yield Static("Wheatley: Systems Online.\n> [WAITING FOR INPUT]")