from collections.abc import Callable
from typing import Protocol


class DiscountStrategyProtocol(Protocol):
    """Protocolo opcional para tipar explícitamente las estrategias de descuento."""

    def __call__(self, price: float) -> float: ...


def no_discount(price: float) -> float:
    """Estrategia por defecto: sin descuento."""
    return price


def percentage_discount(percentage: float) -> Callable[[float], float]:
    """Closure fábrica de estrategia para aplicar un porcentaje de descuento."""
    if not (0 <= percentage <= 100):
        raise ValueError("El porcentaje debe estar entre 0 y 100")

    def strategy(price: float) -> float:
        return price * (1 - percentage / 100)

    return strategy


def fixed_amount_discount(amount: float) -> Callable[[float], float]:
    """Closure fábrica de estrategia para aplicar un descuento fijo en monto."""

    def strategy(price: float) -> float:
        return max(0.0, price - amount)

    return strategy
