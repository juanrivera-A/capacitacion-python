# src/modulo04/async_fetcher.py
import asyncio

import httpx


async def fetch_url_async(
    client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore
) -> dict:
    """Descarga una URL de forma asíncrona respetando el semáforo."""
    async with semaphore:
        response = await client.get(url)
        return {
            "url": url,
            "status_code": response.status_code,
            "size": len(response.content),
        }


async def fetch_all_async(
    urls: list[str], max_concurrent: int = 5, timeout: float = 5.0
) -> list[dict]:
    """Descarga múltiples URLs de forma concurrente usando httpx.AsyncClient y asyncio.Semaphore."""
    semaphore = asyncio.Semaphore(max_concurrent)
    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [fetch_url_async(client, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)
