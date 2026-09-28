import uuid
from dataclasses import dataclass, field
from enum import Enum

from ...modulo08.domain.exceptions import DomainError


class InvalidOrderError(DomainError):
    """Excepción cuando una orden no cumple con las reglas del negocio."""


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise InvalidOrderError("La cantidad del producto debe ser mayor a cero.")
        if self.unit_price <= 0:
            raise InvalidOrderError("El precio unitario debe ser mayor a cero.")

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED

    def __post_init__(self) -> None:
        if not self.customer_id.strip():
            raise InvalidOrderError("El ID del cliente no puede estar vacío.")
        if not self.items:
            raise InvalidOrderError("Una orden debe tener al menos un ítem.")

    @classmethod
    def create(cls, customer_id: str, items: list[OrderItem]) -> "Order":
        return cls(
            order_id=str(uuid.uuid4()),
            customer_id=customer_id,
            items=items,
            status=OrderStatus.CREATED,
        )

    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)
