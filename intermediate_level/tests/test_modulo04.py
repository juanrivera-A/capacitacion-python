# tests/test_modulo04.py
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.modulo04.async_fetcher import fetch_all_async, fetch_url_async
from src.modulo04.processor import compute_heavy_task, run_cpu_tasks_parallel
from src.modulo04.sync_fetcher import fetch_all_sync, fetch_url_sync

# --- Tests para Fetcher Síncrono ---


@patch("httpx.Client.get")
def test_fetch_url_sync(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Hello World"
    mock_get.return_value = mock_response

    result = fetch_url_sync("https://example.com")
    assert result["status_code"] == 200
    assert result["size"] == 11


@patch("src.modulo04.sync_fetcher.fetch_url_sync")
def test_fetch_all_sync(mock_fetch_one):
    mock_fetch_one.return_value = {
        "url": "https://example.com",
        "status_code": 200,
        "size": 10,
    }
    urls = ["https://example.com/1", "https://example.com/2"]

    results = fetch_all_sync(urls)
    assert len(results) == 2
    assert mock_fetch_one.call_count == 2


# --- Tests para Fetcher Asíncrono ---


@pytest.mark.asyncio
async def test_fetch_url_async():
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Async Data"
    mock_client.get.return_value = mock_response

    semaphore = asyncio.Semaphore(2)
    result = await fetch_url_async(mock_client, "https://example.com", semaphore)

    assert result["status_code"] == 200
    assert result["size"] == 10


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_all_async(mock_async_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"OK"
    mock_async_get.return_value = mock_response

    urls = [f"https://httpbin.org/delay/1?id={i}" for i in range(3)]
    results = await fetch_all_async(urls, max_concurrent=2)

    assert len(results) == 3
    assert all(r["status_code"] == 200 for r in results)


# --- Tests para Procesamiento CPU-Bound ---


def test_compute_heavy_task():
    assert compute_heavy_task(5) == 0 + 1 + 4 + 9 + 16


def test_run_cpu_tasks_parallel():
    numbers = [1000, 2000, 3000]
    results = run_cpu_tasks_parallel(numbers)
    expected = [compute_heavy_task(n) for n in numbers]
    assert results == expected
