from duckduckgo_search import DDGS

class SearchAgent:
    def search(self, query, max_results=5):
        print(f"[SearchAgent] Searching DuckDuckGo for: {query}")
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, region='wt-wt', safesearch='Off', max_results=max_results):
                results.append(f"{r['title']} - {r['body']}")
        return "\n\n".join(results)
