from textual.app import ComposeResult
from textual.widgets import Static

class Telemetry(Static):
    """
    [Bot-Right] Hardware Vitals
    GPU/CPU/RAM monitoring.
    """
    BORDER_TITLE = "TELEMETRY [4]"

    def compose(self) -> ComposeResult:
        yield Static("GPU: [||||||    ] 60%\nTMP: 45°C")