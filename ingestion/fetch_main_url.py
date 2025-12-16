import requests
from typing import Optional


class URLFetchError(Exception):
    """Custom exception for URL fetch failures."""
    pass


def fetch_main_url_html(url: str, timeout: int = 15) -> str:
    """
    Fetch raw HTML content from a URL.

    Args:
        url (str): URL to fetch
        timeout (int): request timeout in seconds

    Returns:
        str: HTML content

    Raises:
        URLFetchError: if the URL cannot be fetched
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text

    except requests.exceptions.Timeout:
        raise URLFetchError(f"Timeout while fetching URL: {url}")

    except requests.exceptions.HTTPError as e:
        raise URLFetchError(f"HTTP error while fetching URL: {url} | {e}")

    except requests.exceptions.RequestException as e:
        raise URLFetchError(f"Request failed for URL: {url} | {e}")

"""
if __name__ == "__main__":
    try : 
        html = fetch_main_url_html("https://www.rnc-pro.com/rnc-pro/pfm/100/192_0100.HTM")
        print("HTML fetched successfully:" , len(html))
    except URLFetchError as e : 
        print(e)

"""