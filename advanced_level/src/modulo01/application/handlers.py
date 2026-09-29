from ...modulo01.domain.events import OrderPlacedEvent


class OrderNotificationsHandler:
    """Suscriptor/Manejador de eventos que reacciona a OrderPlacedEvent."""

    def handle_order_created(self, event: OrderPlacedEvent) -> None:
        print(
            f"[EVENT HANDLER] Notificación enviada para el pedido {event.order_id} "
            f"del cliente {event.customer_id} por ${event.total_amount:.2f}"
        )
