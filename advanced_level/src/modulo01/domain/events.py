import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class DomainEvent:
    """Clase base para todos los eventos de dominio del sistema."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_on: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class OrderPlacedEvent(DomainEvent):
    """Evento emitido cuando un pedido es creado y registrado con éxito."""

    order_id: str = ""
    customer_id: str = ""
    total_amount: float = 0.0
