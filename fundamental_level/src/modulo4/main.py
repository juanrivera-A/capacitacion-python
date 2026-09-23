from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ValidationError, field_validator

# 1. Entidades de Dominio (DATACLASSES)


@dataclass(frozen=True)
class OrderItem:
    """Item individual de un pedido. Inmutable (frozen)."""

    product_id: str
    quantity: int
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        """Cálculo derivado del subtotal de esta línea"""
        return self.quantity * self.unit_price


@dataclass
class Order:
    """Entidad principal de Pedido

    Permite cálculo de total y comparación por monto usando dunder methods
    """

    customer_id: str
    items: list[OrderItem] = field(default_factory=list)
    order_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total_amount(self) -> Decimal:
        """Cálculo derivado del monto total del pedido."""
        return sum((item.subtotal for item in self.items), Decimal("0.00"))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other: "Order") -> bool:
        """Permite comparar pedidos por monto total (ordemaniento)."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.total_amount < other.total_amount


# 2. Esquemas de validación y serialización (PYDANTIC)


class OrderItemSchema(BaseModel):
    """Esquema de entrada/salida para un item del pedido."""

    product_id: str = Field(..., min_length=3, description="SKU o ID del producto")
    quantity: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")
    unit_price: Decimal = Field(
        ..., gt=0, description="El precio unitario debe ser mayor a 0"
    )


class OrderIn(BaseModel):
    """Modelo DTO para recibir la petición de creación de un pedido."""

    customer_id: str = Field(..., min_length=1)
    items: list[OrderItemSchema] = Field(..., min_length=1)

    @field_validator("items")
    @classmethod
    def validar_items_no_vacios(
        cls, items: list[OrderItemSchema]
    ) -> list[OrderItemSchema]:
        """Asegura que la orden contenga al menos un ítem válido."""
        if not items:
            raise ValueError("El pedido debe contener al meno un elemento.")
        return items


class OrderOut(BaseModel):
    """Modelo DTO de salida serializable a JSON."""

    order_id: UUID
    customer_id: str
    items: list[OrderItemSchema]
    total_amount: Decimal
    created_at: datetime


# 3. Funciones de conversión y fluo principal


def payload_a_entidad(payload: dict) -> Order:
    """Valida los datos de entrada mediante Pydantic y los convierte a la entidad Order."""
    # 1. Validación de entrada (Pydantic)
    order_in = OrderIn(**payload)

    # 2. Conversión a objetos de dominio (Dataclass)
    domain_items = [
        OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        for item in order_in.items
    ]

    return Order(
        customer_id=order_in.customer_id,
        items=domain_items,
    )


def entidad_a_dto_salida(order: Order) -> OrderOut:
    """Convierte la entidad interna Order al esquema de salida OrderOut."""
    return OrderOut(
        order_id=order.order_id,
        customer_id=order.customer_id,
        items=[
            OrderItemSchema(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in order.items
        ],
        total_amount=order.total_amount,
        created_at=order.created_at,
    )


if __name__ == "__main__":
    print("LABORATORIO MÓDULO 4: OBJETOS Y MODELOS DE DATOS\n")

    # 1. Simulación de payload JSON válido
    payload_valido = {
        "customer_id": "CUST-9982",
        "items": [
            {"product_id": "PROD-A", "quantity": 2, "unit_price": "150.50"},
            {"product_id": "PROD-B", "quantity": 1, "unit_price": "499.00"},
        ],
    }

    # Creación del primer pedido a través del flujo
    pedido_1 = payload_a_entidad(payload_valido)
    print(f"Pedido 1 Creado: ID{pedido_1.order_id}")
    print(f"Total calculado en la dataclass: ${pedido_1.total_amount}")

    # 2. Creación de un segundo pedido directamente en dominio para probar duncer methods
    pedido_2 = Order(
        customer_id="CUST-1001",
        items=[
            OrderItem(product_id="PROD-C", quantity=1, unit_price=Decimal("1200.00"))
        ],
    )
    print(f"\nPedido 2 Creado: Total ${pedido_2.total_amount}")

    # Uso del dunde method __lt__ (<)
    if pedido_1 < pedido_2:
        print(
            f"El pedido 1 (${pedido_1.total_amount}) es MENOR que el Pedido 2 (${pedido_2.total_amount})"
        )

    # 3. Serialización a JSON usando OrderOut
    dto_salida = entidad_a_dto_salida(pedido_1)
    print(f"\n JSON de Salida (OrderOut):\n{dto_salida.model_dump_json(indent=2)}")

    # 4 Prueba de error de validaciones de Pydantic
    print("\n Probando entrada enválida (precio negativo y cantidad en 0)...")
    payload_invalido = {
        "cutomer_id": "CUST-000",
        "items": [{"product_id": "PROD-X", "quantity": 0, "unit_price": "-50.00"}],
    }

    try:
        payload_a_entidad(payload_invalido)
    except ValidationError as e:
        print(f"Pydantic capturó el error correctamente:\n{e}")
