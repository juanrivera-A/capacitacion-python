from typing import Protocol

from ...modulo08.domain.order import Order


class OrderRepositoryPort(Protocol):
    """Puerto para la persistencia de órdenes."""

    def save(self, order: Order) -> None: ...

    def get_by_id(self, order_id: str) -> Order | None: ...


class HTTPNotifierPort(Protocol):
    """Puerto para el envío de notificaciones HTTP externas."""

    def notify_order_created(
        self, order_id: str, customer_id: str, total_amount: float
    ) -> bool: ...
