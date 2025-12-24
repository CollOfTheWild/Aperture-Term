from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, DataTable, ContentSwitcher, Label, ProgressBar
from textual.containers import Vertical, Horizontal
from textual import work
from textual.reactive import reactive

from backend.model_manager import search_models, list_local_models, get_repo_ggufs, download_model
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
    }
    
    #armory_tabs {
        height: 3;
        dock: top;
        background: $surface;
        border-bottom: solid $primary;
    }
    
    .tab-btn {
        width: 1fr;
        height: 100%;
        border: none;
        background: $surface-lighten-1; 
        color: $text;
    }
    
    .tab-btn:hover {
        background: $primary;
        color: $background;
    }
    
    .tab-btn.-primary {
        background: $primary;
        color: $background;
    }

    #armory_status {
        align: center middle;
        height: 1fr;
    }
    
    #logo_art {
        text-align: center;
        width: 100%;
        height: 8;
        content-align: center middle;
        text-style: bold;
    }
    
    #model_info {
        text-align: center;
        width: 100%;
        margin-top: 1;
    }
    
    #armory_browser, #armory_library {
        layout: vertical;
        overflow: hidden;
        height: 1fr;
    }
    
    #browser_input {
        height: 3;
        dock: top;
    }

    DataTable {
        height: 1fr;
        margin-top: 1;
        border-bottom: solid $secondary;
    }

    #library_actions, #browser_actions {
        height: 3;
        min-height: 3;
        background: $surface;
        align-vertical: middle;
        dock: bottom;
    }

    #download_progress {
        width: 100%;
        height: 1;
        display: none;
    }
    """

    # Reactive state
    current_model_id = reactive("None")
    logo_frame = reactive(0)
    selected_repo = reactive("")
    
    def compose(self) -> ComposeResult:
        # Navigation Tabs
        with Horizontal(id="armory_tabs"):
            yield Button("STATUS", id="btn_status", classes="tab-btn", variant="primary")
            yield Button("BROWSER", id="btn_browser", classes="tab-btn")
            yield Button("LIBRARY", id="btn_library", classes="tab-btn")

        # Main Content Switcher
        with ContentSwitcher(initial="armory_status"):
            
            # 1. Status View (Animated Neofetch Card)
            with Vertical(id="armory_status"):
                yield Label("", id="logo_art")
                yield Label("NO MODEL LOADED", id="model_info")

            # 2. Browser View (HF Search)
            with Vertical(id="armory_browser"):
                yield Input(placeholder="Search HuggingFace...", id="browser_input")
                yield DataTable(id="browser_table")
                yield ProgressBar(id="download_progress", show_percentage=True)
                with Horizontal(id="browser_actions"):
                    yield Button("SELECT REPO", id="btn_select_repo", variant="primary")
                    yield Button("DOWNLOAD", id="btn_download", variant="success", disabled=True)
                    yield Button("BACK", id="btn_browser_back", disabled=True)

            # 3. Library View (Local Files)
            with Vertical(id="armory_library"):
                yield DataTable(id="library_table")
                with Horizontal(id="library_actions"):
                    yield Button("LOAD SELECTED", id="btn_load", variant="success")
                    yield Button("REFRESH", id="btn_refresh_lib")

    def on_mount(self) -> None:
        """Initialize and start animation."""
        b_table = self.query_one("#browser_table", DataTable)
        b_table.cursor_type = "row"
        b_table.add_columns("Model ID", "Downloads", "Likes")

        l_table = self.query_one("#library_table", DataTable)
        l_table.cursor_type = "row"
        l_table.add_columns("Filename", "Size (MB)")
        
        self.update_library()
        self.update_status_card()
        
        # Start the "3D" animation (200ms interval)
        self.set_interval(0.2, self.animate_logo)

    def animate_logo(self) -> None:
        """Cycle through logo frames for a 'spinning' effect."""
        self.logo_frame = (self.logo_frame + 1) % 2
        self.update_status_card()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        switcher = self.query_one(ContentSwitcher)
        
        # Handle Tab Switching
        if event.button.id in ["btn_status", "btn_browser", "btn_library"]:
            # Reset all tabs
            for btn_id in ["btn_status", "btn_browser", "btn_library"]:
                self.query_one(f"#{btn_id}", Button).variant = "default"
            
            # Set active tab
            event.button.variant = "primary"

        if event.button.id == "btn_status":
            switcher.current = "armory_status"
        elif event.button.id == "btn_browser":
            switcher.current = "armory_browser"
        elif event.button.id == "btn_library":
            switcher.current = "armory_library"
            self.update_library()
        elif event.button.id == "btn_refresh_lib":
            self.update_library()
        elif event.button.id == "btn_load":
            self.load_selected_model()
        elif event.button.id == "btn_select_repo":
            self.show_repo_files()
        elif event.button.id == "btn_browser_back":
            self.reset_browser()
        elif event.button.id == "btn_download":
            self.start_download()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "browser_input":
            self.selected_repo = ""
            self.perform_search(event.value)

    @work(exclusive=True, thread=True)
    def perform_search(self, query: str) -> None:
        table = self.query_one("#browser_table", DataTable)
        table.clear()
        results = search_models(query)
        for r in results:
            table.add_row(r["id"], str(r["downloads"]), str(r["likes"]))

    def show_repo_files(self) -> None:
        """Show GGUF files for the selected repository."""
        table = self.query_one("#browser_table", DataTable)
        try:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            row = table.get_row(row_key)
            self.selected_repo = row[0]
            self.fetch_files(self.selected_repo)
        except Exception:
            pass

    @work(exclusive=True, thread=True)
    def fetch_files(self, repo_id: str) -> None:
        """Async fetch files in repo."""
        table = self.query_one("#browser_table", DataTable)
        table.clear()
        table.update_cell(table.add_row("Scanning...", "", ""), 0, 0, "Scanning...") # Temp row
        
        files = get_repo_ggufs(repo_id)
        table.clear()
        table.add_columns("GGUF File", "Size") # Overwrites columns? No, better clear and rebuild
        
        # Reset columns
        table.clear(columns=True)
        table.add_columns("GGUF File", "Source")
        
        for f in files:
            table.add_row(f, repo_id)
        
        self.query_one("#btn_select_repo").disabled = True
        self.query_one("#btn_download").disabled = False
        self.query_one("#btn_browser_back").disabled = False

    def reset_browser(self) -> None:
        """Go back to repo search results."""
        table = self.query_one("#browser_table", DataTable)
        table.clear(columns=True)
        table.add_columns("Model ID", "Downloads", "Likes")
        self.selected_repo = ""
        self.query_one("#btn_select_repo").disabled = False
        self.query_one("#btn_download").disabled = True
        self.query_one("#btn_browser_back").disabled = True
        # Re-trigger search for the current input
        query = self.query_one("#browser_input", Input).value
        if query:
            self.perform_search(query)

    def start_download(self) -> None:
        """Begin downloading the selected file."""
        table = self.query_one("#browser_table", DataTable)
        try:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            row = table.get_row(row_key)
            filename = row[0]
            repo_id = row[1]
            self.run_download(repo_id, filename)
        except Exception:
            pass

    @work(exclusive=True, thread=True)
    def run_download(self, repo_id: str, filename: str) -> None:
        """Threaded download execution."""
        progress = self.query_one("#download_progress", ProgressBar)
        progress.styles.display = "block"
        progress.update(total=100, progress=0)
        
        # Note: hf_hub_download doesn't easily expose progress percentage to a callback
        # for a simple TUI, we'll just show it's active.
        progress.update(progress=50) # Fake progress for now
        
        path = download_model(repo_id, filename)
        
        if path:
            progress.update(progress=100)
            self.app.notify(f"Download Complete: {filename}")
        else:
            self.app.notify(f"Download Failed: {filename}", severity="error")
        
        # Hide progress after a delay
        import time
        time.sleep(2)
        progress.styles.display = "none"
        self.update_library()

    def update_library(self) -> None:
        table = self.query_one("#library_table", DataTable)
        table.clear()
        models = list_local_models()
        for m in models:
            table.add_row(m["name"], f"{m['size_mb']:.1f}")

    def load_selected_model(self) -> None:
        """Trigger model loading."""
        table = self.query_one("#library_table", DataTable)
        try:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            row = table.get_row(row_key)
            model_name = row[0]
            self.current_model_id = model_name
            self.query_one(ContentSwitcher).current = "armory_status"
            # TODO: Post ModelLoadRequest to App
        except Exception:
            pass

    def update_status_card(self) -> None:
        """Update the UI card with current model and logo frame."""
        logo_data = get_logo(self.current_model_id)
        art = logo_data["art"][self.logo_frame]
        color = logo_data["color"]
        
        logo_label = self.query_one("#logo_art", Label)
        logo_label.update(art)
        logo_label.styles.color = color
        
        info_label = self.query_one("#model_info", Label)
        if self.current_model_id == "None":
             info_label.update("[dim]SYSTEM STANDBY\nNO MODEL LOADED[/dim]")
        else:
             info_label.update(f"[b cyan]{self.current_model_id}[/b cyan]\n[green]LOADED & ONLINE[/green]")