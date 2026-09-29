from typing import Protocol

from src.modulo01.domain.order import Order


class OrderRepositoryPort(Protocol):
    """Interfaz Gateway para la persistencia de órdenes."""

    def add(self, order: Order) -> None: ...

    def get_by_id(self, order_id: str) -> Order | None: ...
