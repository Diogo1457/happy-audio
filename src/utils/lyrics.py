import requests
from bs4 import BeautifulSoup
import re
import sys
from rich.console import Console
from rich.traceback import install

# Enable rich tracebacks
install(show_locals=True)
console = Console()

class LyricsNotFoundError(Exception):
    """Raised when lyrics cannot be found for the given query"""
    pass

def search_genius_public_multiple(query: str, per_page: int = 5, silent: bool = False) -> list[dict]:
    """Search Genius public API and return up to `per_page` song results"""
    url = "https://genius.com/api/search/multi"
    params = {"per_page": per_page, "q": query}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    results = []
    sections = data.get("response", {}).get("sections", [])
    for section in sections:
        hits = section.get("hits", [])
        for hit in hits:
            result = hit.get("result", {})
            if result.get("_type") == "song" and len(results) < per_page:
                results.append({
                    "title": result.get("title", "Unknown Title"),
                    "artist": result.get("primary_artist", {}).get("name", "Unknown Artist"),
                    "url": result.get("url")
                })
    return results

def scrape_lyrics(url: str) -> str | None:
    """Scrape Genius lyrics and clean them"""
    try:
        html = requests.get(url, timeout=10).text
    except Exception:
        return None

    soup = BeautifulSoup(html, "html.parser")
    containers = soup.find_all("div", {"data-lyrics-container": "true"})
    if not containers:
        return None

    lyrics = "\n".join(c.get_text(separator="\n") for c in containers)

    # Keep everything after "Read More" if it exists
    match = re.search(r'Read More\s*(.*)', lyrics, flags=re.DOTALL | re.IGNORECASE)
    if match:
        lyrics = match.group(1)

    # Remove [Pre-Chorus] and any other [..] or (..) content
    lyrics = re.sub(r'\[Pre-Chorus\]', '', lyrics, flags=re.IGNORECASE)
    lyrics = re.sub(r'\[.*?\]', '', lyrics)
    lyrics = re.sub(r'\(.*?\)', '', lyrics)
    lyrics = re.sub(r'\n{2,}', '\n\n', lyrics).strip()

    return lyrics.strip("\n") or None


def lyrics_from_filename(filename_no_ext: str, silent: bool = False) -> str | list[dict] | None:
    """Search Genius using filename and optionally prompt user to select a song"""
    def split_camel_case(text: str) -> str:
        return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)

    query = (
        filename_no_ext
        .replace("_", " ")
        .replace("-", " ")
        .replace(".", " ")
        .strip()
    )
    query = split_camel_case(query)

    results = search_genius_public_multiple(query, per_page=5, silent=silent)
    if not results:
        if silent:
            return []
        else:
            raise LyricsNotFoundError(f"No results found for '{filename_no_ext}'")

    if silent:
        return results

    # Interactive mode
    if len(results) > 1:
        console.print("[bold yellow]Multiple songs found:[/bold yellow]")
        for i, r in enumerate(results, 1):
            console.print(f"{i}. [bold]{r['title']}[/bold] - {r['artist']}")
        console.print("0. None of the above (exit)")

        while True:
            try:
                choice = console.input(f"Select a song (0-{len(results)}): ").strip()
                if choice.isdigit():
                    choice_num = int(choice)
                    if choice_num == 0:
                        raise LyricsNotFoundError("User exited selection.")
                    elif 1 <= choice_num <= len(results):
                        selected = results[choice_num - 1]
                        break
                console.print("[red]Invalid choice, try again.[/red]")
            except KeyboardInterrupt:
                console.print("\n[red]Program interrupted.[/red]")
                sys.exit()
    else:
        selected = results[0]

    lyrics = scrape_lyrics(selected["url"])
    if not lyrics:
        raise LyricsNotFoundError(f"Lyrics could not be scraped for '{selected['title']}'")
    return lyrics

# Example usage
if __name__ == "__main__":
    lyrics = lyrics_from_filename("Heathens", silent=False)

