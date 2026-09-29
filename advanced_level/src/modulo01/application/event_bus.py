from collections import defaultdict
from collections.abc import Callable
from typing import Any, TypeVar

from ...modulo01.domain.events import DomainEvent

E = TypeVar("E", bound=DomainEvent)
EventHandler = Callable[[E], None]


class EventBus:
    """Manejador/Despachador central de eventos de dominio."""

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Callable[[Any], None]]] = (
            defaultdict(list)
        )

    def subscribe(self, event_type: type[E], handler: EventHandler[E]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            event_type = type(event)
            handlers = self._handlers.get(event_type, [])
            for handler in handlers:
                handler(event)
