from camel.agents import BaseAgent
from duckduckgo_search import DDGS

class WebAgent(BaseAgent):
    """
    Uses DuckDuckGo to find materials for Python interview preparation.
    """
    def __init__(self, name="WebAgent"):
        super().__init__(name=name)

    def step(self, job_results, *args, **kwargs):
        print("=== [WebAgent] Searching for interview preparation resources ===")
        
        query = "Python developer interview preparation guide site:medium.com OR site:github.com OR site:realpython.com"
        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=10):
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "body": r.get("body"),
                })

        print(f"[WebAgent] Found {len(results)} resources.")
        return {
            "jobs": job_results,
            "resources": results,
        }
