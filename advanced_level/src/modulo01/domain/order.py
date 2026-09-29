import uuid
from dataclasses import dataclass, field

from src.modulo01.domain.events import (
    DomainEvent,
    OrderPlacedEvent,
)
from src.modulo01.domain.exceptions import InvalidOrderError


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise InvalidOrderError("La cantidad del producto debe ser mayor a 0.")
        if self.unit_price <= 0.0:
            raise InvalidOrderError("El precio unitario debe ser mayor a 0.")

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[OrderItem] = field(default_factory=list)
    status: str = "PENDING"
    events: list[DomainEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.customer_id.strip():
            raise InvalidOrderError("El cliente no puede ser un valor vacío.")
        if not self.items:
            raise InvalidOrderError("Un pedido debe contener al menos un ítem.")

    @classmethod
    def create(cls, customer_id: str, items: list[OrderItem]) -> "Order":
        order = cls(
            order_id=str(uuid.uuid4()),
            customer_id=customer_id,
            items=items,
            status="PLACED",
        )
        # Registramos el evento de dominio tras crearse exitosamente
        order.events.append(
            OrderPlacedEvent(
                order_id=order.order_id,
                customer_id=order.customer_id,
                total_amount=order.total_amount,
            )
        )
        return order

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.items)
