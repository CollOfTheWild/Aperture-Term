from textual.app import ComposeResult
from textual.widgets import Static, Input, RichLog
from textual.containers import Vertical
from textual.message import Message

class FlightDeck(Static):
    """
    [Bot-Left] Chat Interface
    Main user interaction point.
    """
    BORDER_TITLE = "FLIGHT DECK [3]"
    
    CSS = """
    FlightDeck {
        layout: vertical;
    }
    #chat_log {
        height: 1fr;
        border: vkey $secondary;
    }
    #chat_input {
        height: 3;
        dock: bottom;
    }
    """

    class SearchRequest(Message):
        """Emitted when the user requests a search."""
        def __init__(self, query: str) -> None:
            self.query = query
            super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            yield RichLog(id="chat_log", highlight=True, markup=True, wrap=True)
            yield Input(placeholder="Initiate Protocol...", id="chat_input")

    def on_mount(self) -> None:
        """Post-mount initialization."""
        self.log_message("[bold green]SYSTEM ONLINE.[/bold green]")
        self.log_message("[dim]Aperture-Term v0.1 ready.[/dim]")

    def log_message(self, message: str) -> None:
        """Append a message to the chat log."""
        log = self.query_one("#chat_log", RichLog)
        log.write(message)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input."""
        user_input = event.value.strip()
        if not user_input:
            return

        # Check for commands
        if user_input.startswith("/search "):
            query = user_input[8:].strip()
            if query:
                self.post_message(self.SearchRequest(query))
                self.log_message(f"[bold yellow]SEARCH PROTOCOL:[/bold yellow] {query}")
                event.input.value = ""
                return
            
        # Echo user input
        self.log_message(f"[bold cyan]User:[/bold cyan] {user_input}")
        
        # Clear input
        event.input.value = ""
        
        # TODO: Trigger backend inference here