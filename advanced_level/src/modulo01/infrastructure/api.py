from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ...modulo01.application.dtos import OrderItemDTO, PlaceOrderDTO
from ...modulo01.application.event_bus import EventBus
from ...modulo01.application.handlers import OrderNotificationsHandler
from ...modulo01.application.use_cases import PlaceOrderUseCase
from ...modulo01.domain.events import OrderPlacedEvent
from ...modulo01.domain.exceptions import DomainError
from ...modulo01.infrastructure.presenters_impl import JsonOrderPresenter
from ...modulo01.infrastructure.uow_impl import SQLAlchemyUnitOfWork


class ItemRequestSchema(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0.0)


class PlaceOrderRequestSchema(BaseModel):
    customer_id: str = Field(min_length=1)
    items: list[ItemRequestSchema] = Field(min_length=1)


def create_order_router(uow: SQLAlchemyUnitOfWork, event_bus: EventBus) -> APIRouter:
    router = APIRouter(prefix="/orders", tags=["Orders"])

    @router.get("/healt", tags=["Healt"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    # 1. Subscribir el manejador de eventos
    notification_handler = OrderNotificationsHandler()
    event_bus.subscribe(OrderPlacedEvent, notification_handler.handle_order_created)

    presenter = JsonOrderPresenter()

    @router.post("", status_code=status.HTTP_201_CREATED)
    def place_order(payload: PlaceOrderRequestSchema) -> dict[str, Any]:
        use_case = PlaceOrderUseCase(uow=uow, event_bus=event_bus)

        items_dto = [
            OrderItemDTO(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in payload.items
        ]

        dto = PlaceOrderDTO(customer_id=payload.customer_id, items=items_dto)

        try:
            result_dto = use_case.execute(dto)
            # 2. El Presenter da el formato final de respuesta
            return presenter.present_order_created(result_dto)
        except DomainError as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
            )

    return router
