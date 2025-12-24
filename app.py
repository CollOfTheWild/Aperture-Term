import json
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container

# Component Imports
from components.armory import Armory
from components.context_swarm import ContextSwarm
from components.flight_deck import FlightDeck
from components.telemetry import Telemetry

class ApertureTerm(App):
    """
    Aperture-Term: The Cognition Dashboard.
    System 2 Wrapper for Llama.cpp.
    """
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 2;
        grid-rows: 40% 60%;
        grid-columns: 50% 50%;
        background: $surface;
    }

    Armory {
        row-span: 1;
        col-span: 1;
        border: heavy $primary;
    }

    ContextSwarm {
        row-span: 1;
        col-span: 1;
        border: heavy $secondary;
    }

    FlightDeck {
        row-span: 1;
        col-span: 1;
        border: heavy $primary;
    }

    Telemetry {
        row-span: 1;
        col-span: 1;
        border: heavy $secondary;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("tab", "focus_next", "Cycle Panel"),
    ]

    def compose(self) -> ComposeResult:
        yield Armory()
        yield ContextSwarm()
        yield FlightDeck()
        yield Telemetry()
        yield Footer()

if __name__ == "__main__":
    app = ApertureTerm()
    app.run()