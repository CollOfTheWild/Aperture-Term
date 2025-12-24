from textual.app import ComposeResult
from textual.widgets import Static, RichLog
from textual import work
from backend.search_tool import search_web

class ContextSwarm(Static):
    """
    [Top-Right] Search & RAG Tools
    Handles async context fetching.
    """
    BORDER_TITLE = "CONTEXT SWARM [2]"

    def compose(self) -> ComposeResult:
        yield RichLog(id="search_log", highlight=True, markup=True)

    @work(exclusive=True, thread=True)
    def perform_search(self, query: str) -> None:
        """Execute a search query asynchronously."""
        log = self.query_one("#search_log", RichLog)
        log.clear()
        log.write(f"[blink]SCANNING:[/blink] {query}...")
        
        try:
            results = search_web(query)
            
            if not results:
                log.write("[red]No results found.[/red]")
                return

            log.write(f"[green]FOUND {len(results)} ENTRIES:[/green]\n")
            
            for i, res in enumerate(results, 1):
                title = res.get('title', 'No Title')
                body = res.get('body', '')
                link = res.get('href', '')
                
                log.write(f"[bold cyan][{i}] {title}[/bold cyan]")
                log.write(f"[dim]{link}[/dim]")
                log.write(f"{body}\n")
                
        except Exception as e:
            log.write(f"[bold red]SEARCH ERROR:[/bold red] {str(e)}")