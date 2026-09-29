import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modulo01.application.dtos import OrderItemDTO, PlaceOrderDTO
from src.modulo01.application.event_bus import EventBus
from src.modulo01.application.use_cases import PlaceOrderUseCase
from src.modulo01.domain.events import OrderPlacedEvent
from src.modulo01.infrastructure.database import Base
from src.modulo01.infrastructure.presenters_impl import JsonOrderPresenter
from src.modulo01.infrastructure.uow_impl import SQLAlchemyUnitOfWork


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def test_laboratorio_uow_presenter_and_events(session_factory):
    # Setup
    uow = SQLAlchemyUnitOfWork(session_factory)
    event_bus = EventBus()

    events_captured: list[OrderPlacedEvent] = []

    def spy_event_handler(event: OrderPlacedEvent) -> None:
        events_captured.append(event)

    event_bus.subscribe(OrderPlacedEvent, spy_event_handler)

    use_case = PlaceOrderUseCase(uow=uow, event_bus=event_bus)
    presenter = JsonOrderPresenter()

    # Act
    dto = PlaceOrderDTO(
        customer_id="CUST-LAB-100",
        items=[OrderItemDTO(product_id="PROD-01", quantity=2, unit_price=150.0)],
    )
    result_dto = use_case.execute(dto)
    response_payload = presenter.present_order_created(result_dto)

    # Assert 1: Presenter output
    assert response_payload["data"]["customer_id"] == "CUST-LAB-100"
    assert response_payload["data"]["total_amount"] == 300.0
    assert response_payload["meta"]["code"] == "ORDER_CREATED_SUCCESSFULLY"

    # Assert 2: Event published and handled
    assert len(events_captured) == 1
    assert events_captured[0].customer_id == "CUST-LAB-100"
    assert events_captured[0].total_amount == 300.0

    # Assert 3: Persisted via UoW
    with uow:
        assert uow.orders is not None
        saved_order = uow.orders.get_by_id(result_dto.order_id)
        assert saved_order is not None
        assert saved_order.customer_id == "CUST-LAB-100"
