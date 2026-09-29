from typing import Any

from ...modulo01.application.dtos import OrderResponseDTO
from ...modulo01.application.presenters import OrderPresenterPort


class JsonOrderPresenter(OrderPresenterPort[dict[str, Any]]):
    """Implementación que genera un diccionario adecuado para respuestas JSON en API."""

    def present_order_created(self, dto: OrderResponseDTO) -> dict[str, Any]:
        return {
            "data": {
                "order_id": dto.order_id,
                "customer_id": dto.customer_id,
                "total_amount": dto.total_amount,
                "status": dto.status,
            },
            "meta": {
                "message": dto.message,
                "code": "ORDER_CREATED_SUCCESSFULLY",
            },
        }
