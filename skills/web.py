"""Web skills: search the web, open a specific site."""
import webbrowser
import urllib.parse


def _search_match(t):
    return t.startswith("search for") or t.startswith("google") or t.startswith("look up")


def _search_handler(t):
    for prefix in ("search for", "google", "look up"):
        if t.startswith(prefix):
            query = t[len(prefix):].strip()
            break
    else:
        query = t
    if not query:
        return "What would you like me to search for?"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Searching for {query}."


COMMON_SITES = {
    "youtube": "https://youtube.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "reddit": "https://reddit.com",
}


def _open_site_match(t):
    return t.startswith("open ") and any(site in t for site in COMMON_SITES)


def _open_site_handler(t):
    for site, url in COMMON_SITES.items():
        if site in t:
            webbrowser.open(url)
            return f"Opening {site.capitalize()}."
    return "I don't know that site yet."


SKILLS = [
    (_open_site_match, _open_site_handler),  # check specific sites before generic search
    (_search_match, _search_handler),
]
