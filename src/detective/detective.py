import sys
import warnings
from datetime import datetime

# Handle the import for duckduckgo_search which might be renamed to ddgs
try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        print("❌ Critical Error: 'duckduckgo-search' library not found.")
        sys.exit(1)

try:
    from googlesearch import search as google_search
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

class Detective:
    """
    The Detective module: Intelligence.
    Searches the web for facts and news related to a specific keyword or event.
    """

    def __init__(self):
        self.ddgs = DDGS()

    def investigate(self, query: str, max_results: int = 5):
        """
        Searches the web for the given query.

        Args:
            query (str): The keyword or sentence to search for.
            max_results (int): Maximum number of results to return.

        Returns:
            list: A list of dictionaries containing title, href, and body of results.
        """
        print(f"🕵️  Detective is investigating: '{query}'...")
        
        results = []
        max_retries = 3
        
        import time
        
        # List of backends to try in order
        # 'api' is deprecated -> 'auto'
        backends = ['auto', 'html', 'lite']
        
        for attempt in range(max_retries):
            # Cycle through backends: 0->api, 1->html, 2->lite, etc.
            current_backend = backends[attempt % len(backends)]
            
            try:
                print(f"   (Attempt {attempt + 1} using backend: '{current_backend}')")
                # simple text search
                search_generator = self.ddgs.text(query, max_results=max_results, backend=current_backend)
                
                # The generator might be lazy, so we iterate to fetch
                found_new = False
                if search_generator:
                    for result in search_generator:
                        results.append({
                            "title": result.get("title"),
                             "link": result.get("href"),
                            "snippet": result.get("body"),
                            "timestamp": datetime.now().isoformat()
                        })
                        found_new = True
                
                # If we got results, break
                if found_new:
                    break
                else:
                    # If generator was empty but no exception
                    print(f"⚠️  Attempt {attempt + 1}: No results returned. Retrying...")
            
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} Error ({current_backend}): {e}")
            
            # Wait before retrying
            if attempt < max_retries - 1:
                time.sleep(2)
        
        # Fallback to Google Search if enabled and no results from DDGS
        if not results and HAS_GOOGLE:
            print("\n⚠️  DuckDuckGo failed. Attempting fallback to Google Search...")
            try:
                # advanced=True returns objects with title/desc/url, but googlesearch-python might just yield urls
                # Checking library capability: 'googlesearch-python' yields strings (URLs) by default, 
                # but 'search' function has 'advanced=True' in some versions.
                # simpler approach: just get URLs and fake the title for now or use advanced=True if available.
                
                # We will just get links for robustness.
                g_results = google_search(query, num_results=max_results, advanced=True)
                for res in g_results:
                    # 'res' might be an object with title/description/url
                    results.append({
                        "title": getattr(res, 'title', res.url if hasattr(res, 'url') else str(res)),
                        "link": getattr(res, 'url', str(res)) if hasattr(res, 'url') else str(res),
                        "snippet": getattr(res, 'description', "No description available.") if hasattr(res, 'description') else "",
                        "timestamp": datetime.now().isoformat()
                    })
                
                if results:
                    print(f"✅  Google Search found {len(results)} clues.")
                    
            except Exception as e:
                 print(f"❌  Google Search fallback also failed: {e}")

        if not results:
             print("❌  Detective failed to find any clues after retries and fallback.")
             
             # MOCK FALLBACK for demonstration/dev environment if network is blocked
             print("\n⚠️  Network blocked? Engaging SIMULATION MODE (Mock Data)...")
             results = [
                 {
                     "title": f"Simulation: Latest news on '{query}'",
                     "link": "http://simulation.local/news/1",
                     "snippet": f"This is a simulated news snippet about {query} generated because external network access was denied. In a real scenario, this would be live data.",
                     "timestamp": datetime.now().isoformat()
                 },
                 {
                     "title": f"Simulation: Analysis of '{query}'",
                     "link": "http://simulation.local/news/2",
                     "snippet": "Experts suggest that this topic is trending significantly in the simulated environment domain.",
                     "timestamp": datetime.now().isoformat()
                 }
             ]
             print(f"✅  Detective generated {len(results)} SIMULATED clues.")
             return results

        print(f"✅  Detective found {len(results)} clues.")
        return results

if __name__ == "__main__":
    # Test the Detective
    d = Detective()
    
    # Use command line arguments if provided
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "latest developments in AI alignment 2025"
        
    clues = d.investigate(query, max_results=3)
    
    print("\n--- DETECTIVE REPORT ---")
    for i, clue in enumerate(clues, 1):
        print(f"{i}. {clue.get('title', 'No Title')}")
        print(f"   {clue.get('link', 'No Link')}")
        print(f"   {clue.get('snippet', 'No Snippet')}\n")
