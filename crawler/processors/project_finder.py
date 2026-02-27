import httpx
from db import get_conn


def find_related_projects(title: str, keywords: list[str]) -> list[dict]:
    """Search GitHub for projects mentioned in article titles."""
    projects = []
    search_terms = [k for k in keywords if len(k) > 3][:3]

    for term in search_terms:
        try:
            resp = httpx.get(
                "https://api.github.com/search/repositories",
                params={"q": term, "sort": "stars", "per_page": 3},
                headers={"Accept": "application/vnd.github+json"},
                timeout=10,
            )
            if resp.status_code != 200:
                continue

            for repo in resp.json().get("items", []):
                projects.append({
                    "name": repo["full_name"],
                    "url": repo["html_url"],
                    "platform": "github",
                    "description": (repo.get("description") or "")[:200],
                    "stars": repo.get("stargazers_count", 0),
                })
        except Exception as e:
            print(f"[ProjectFinder] Error: {e}")

    # Deduplicate by URL
    seen = set()
    unique = []
    for p in projects:
        if p["url"] not in seen:
            seen.add(p["url"])
            unique.append(p)
    return unique[:5]
