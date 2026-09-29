from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderItemDTO:
    product_id: str
    quantity: int
    unit_price: float


@dataclass(frozen=True)
class PlaceOrderDTO:
    customer_id: str
    items: list[OrderItemDTO]


@dataclass(frozen=True)
class OrderResponseDTO:
    order_id: str
    customer_id: str
    total_amount: float
    status: str
    message: str = field(default="Pedido registrado exitosamente.")
