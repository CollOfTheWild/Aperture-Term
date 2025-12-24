from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, DataTable, ContentSwitcher, Label
from textual.containers import Vertical, Horizontal
from textual import work
from textual.reactive import reactive

from backend.model_manager import search_models, list_local_models
from assets.logos import get_logo

class Armory(Static):
    """
    [Top-Left] Model Loader & Config
    Displays model list and Neofetch card.
    """
    BORDER_TITLE = "THE ARMORY [1]"
    
    CSS = """
    Armory {
        layout: vertical;
        overflow: hidden;
    }
    
    #armory_tabs {
        height: 3;
        dock: top;
        align: center middle;
    }
    
    .tab-btn {
        width: 1fr;
    }

    #card_container {
        align: center middle;
        height: 100%;
    }
    
    #logo_art {
        text-align: center;
        width: 100%;
    }
    
    #model_info {
        text-align: center;
        color: $text-muted;
    }
    
    #browser_input {
        dock: top;
    }
    """

    # Track current model state
    current_model = reactive("None")
    
    def compose(self) -> ComposeResult:
        # Navigation Tabs
        with Horizontal(id="armory_tabs"):
            yield Button("STATUS", id="btn_status", classes="tab-btn", variant="primary")
            yield Button("BROWSER", id="btn_browser", classes="tab-btn")
            yield Button("LIBRARY", id="btn_library", classes="tab-btn")

        # Main Content Switcher
        with ContentSwitcher(initial="armory_status"):
            
            # 1. Status View (Neofetch Card)
            with Vertical(id="armory_status"):
                with Vertical(id="card_container"):
                    yield Label("", id="logo_art")
                    yield Label("NO MODEL LOADED", id="model_info")

            # 2. Browser View (HF Search)
            with Vertical(id="armory_browser"):
                yield Input(placeholder="Search HuggingFace...", id="browser_input")
                yield DataTable(id="browser_table")

            # 3. Library View (Local Files)
            with Vertical(id="armory_library"):
                yield DataTable(id="library_table")

    def on_mount(self) -> None:
        """Initialize tables and load data."""
        # Setup Browser Table
        b_table = self.query_one("#browser_table", DataTable)
        b_table.cursor_type = "row"
        b_table.add_columns("Model ID", "Downloads", "Likes")

        # Setup Library Table
        l_table = self.query_one("#library_table", DataTable)
        l_table.cursor_type = "row"
        l_table.add_columns("Filename", "Size (MB)")
        
        self.update_library()
        self.show_model_card("Unknown")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle tab switching."""
        switcher = self.query_one(ContentSwitcher)
        
        if event.button.id == "btn_status":
            switcher.current = "armory_status"
        elif event.button.id == "btn_browser":
            switcher.current = "armory_browser"
        elif event.button.id == "btn_library":
            switcher.current = "armory_library"
            self.update_library()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search input."""
        if event.input.id == "browser_input":
            self.perform_search(event.value)

    @work(exclusive=True, thread=True)
    def perform_search(self, query: str) -> None:
        """Async HF Search."""
        table = self.query_one("#browser_table", DataTable)
        table.clear()
        
        results = search_models(query)
        
        for r in results:
            table.add_row(r["id"], str(r["downloads"]), str(r["likes"]))

    def update_library(self) -> None:
        """Refresh local file list."""
        table = self.query_one("#library_table", DataTable)
        table.clear()
        
        models = list_local_models()
        for m in models:
            table.add_row(m["name"], f"{m['size_mb']:.1f}")

    def show_model_card(self, model_name: str) -> None:
        """Render the ASCII card."""
        logo_data = get_logo(model_name)
        art = logo_data["art"][0] # Static frame 0 for now
        color = logo_data["color"]
        
        logo_label = self.query_one("#logo_art", Label)
        logo_label.update(art)
        logo_label.styles.color = color
        
        info_label = self.query_one("#model_info", Label)
        info_label.update(f"[b]{model_name}[/b]\n[dim]Ready for Inference[/dim]")