from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Perform a web search using DuckDuckGo.
    Returns a list of dictionaries with keys: 'title', 'href', 'body'.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        # Log error or re-raise depending on strategy
        print(f"Search Error: {e}")
        return []
