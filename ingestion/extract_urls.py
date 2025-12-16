from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List


class URLExtractionError(Exception):
    """Custom exception for URL extraction failures."""
    pass


def extract_child_urls(html: str, base_url: str) -> List[str]:
    """
    Extract and normalize child URLs from main page HTML.
    (Logic EXACTLY same as notebook)
    """
    try:
        soup = BeautifulSoup(html, "html.parser")

        links = []

        for a in soup.find_all("a"):
            href = a.get("href")

            if href and href.strip():
                # same logic as notebook
                href = href.strip().replace("\\", "/")
                full_url = urljoin(base_url, href)
                links.append(full_url)

        return list(set(links))

    except Exception as e:
        raise URLExtractionError(f"Failed to extract child URLs: {e}")
"""
if __name__ == "__main__":
    from fetch_main_url import fetch_main_url_html

    MAIN_URL = "https://www.rnc-pro.com/rnc-pro/pfm/100/192_0100.HTM"

    html = fetch_main_url_html(MAIN_URL)
    urls = extract_child_urls(html, MAIN_URL)

    print("Extracted child URLs:")
    for u in urls:
        print(u)
"""