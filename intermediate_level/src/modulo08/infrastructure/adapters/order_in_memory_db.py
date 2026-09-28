from ....modulo08.application.order_ports import OrderRepositoryPort
from ....modulo08.domain.order import Order


class InMemoryOrderRepositoryAdapter(OrderRepositoryPort):
    """Adaptador de infraestructura: Almacenamiento de órdenes en memoria."""

    def __init__(self) -> None:
        self._storage: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._storage[order.order_id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self._storage.get(order_id)
