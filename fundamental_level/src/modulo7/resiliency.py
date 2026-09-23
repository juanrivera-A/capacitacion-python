from collections.abc import Callable
from typing import TypeVar

import httpx

T = TypeVar("T")


def execute_safe_request(func: Callable[[], T]) -> T | None:
    """Ejecuta una petición HTTP capturando errores de estado y timeouts."""
    try:
        return func()
    except (httpx.HTTPStatusError, httpx.TimeoutException) as exc:
        print(f"\n[Resiliency Log] Error capturado: {exc}")
        return None
