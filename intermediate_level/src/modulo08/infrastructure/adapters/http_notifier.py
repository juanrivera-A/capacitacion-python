from typing import Any

from ....modulo08.application.order_ports import HTTPNotifierPort


class MockHTTPNotifierAdapter(HTTPNotifierPort):
    """Adaptador de infraestructura: Notificador HTTP simulado para pruebas."""

    def __init__(self) -> None:
        self.requests_log: list[dict[str, Any]] = []

    def notify_order_created(
        self, order_id: str, customer_id: str, total_amount: float
    ) -> bool:
        payload: dict[str, Any] = {
            "order_id": order_id,
            "customer_id": customer_id,
            "total_amount": total_amount,
        }
        self.requests_log.append(payload)
        return True
