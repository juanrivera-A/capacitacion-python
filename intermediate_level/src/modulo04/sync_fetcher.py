# src/modulo04/sync_fetcher.py
import httpx


def fetch_url_sync(url: str, timeout: float = 5.0) -> dict:
    """Realiza una petición HTTP GET síncrona."""
    with httpx.Client(timeout=timeout) as client:
        response = client.get(url)
        return {
            "url": url,
            "status_code": response.status_code,
            "size": len(response.content),
        }


def fetch_all_sync(urls: list[str]) -> list[dict]:
    """Descarga secuencialmente una lista de URLs."""
    results = []
    for url in urls:
        results.append(fetch_url_sync(url))
    return results
