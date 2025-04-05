import requests
from fastapi import HTTPException


def fetch_html(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content as a string.

    Raises:
        HTTPException: If the request fails.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch HTML content: {str(e)}")
