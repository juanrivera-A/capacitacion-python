from dataclasses import dataclass


@dataclass(frozen=True)
class OrderItemDTO:
    """DTO de entrada/salida para un ítem de la orden."""

    product_id: str
    quantity: int
    unit_price: float


@dataclass(frozen=True)
class CreateOrderDTO:
    """DTO de entrada para crear una orden."""

    customer_id: str
    items: list[OrderItemDTO]


@dataclass(frozen=True)
class OrderResponseDTO:
    """DTO de salida con los detalles de la orden creada."""

    order_id: str
    customer_id: str
    total_amount: float
    status: str
