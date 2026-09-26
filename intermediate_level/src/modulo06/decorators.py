from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def memoize_cache(func: Callable[P, R]) -> Callable[P, R]:
    """Decorador estructural para almacenar en caché resultados de llamadas a funciones."""
    cache: dict[tuple[Any, ...], R] = {}

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper
