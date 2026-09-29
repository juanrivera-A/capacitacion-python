from src.modulo01.application.dtos import OrderResponseDTO, PlaceOrderDTO
from src.modulo01.application.event_bus import EventBus
from src.modulo01.application.unit_of_work import UnitOfWorkPort
from src.modulo01.domain.order import Order, OrderItem


class PlaceOrderUseCase:
    """Caso de Uso: Registrar una orden de compra en el sistema."""

    def __init__(self, uow: UnitOfWorkPort, event_bus: EventBus) -> None:
        self.uow = uow
        self.event_bus = event_bus

    def execute(self, dto: PlaceOrderDTO) -> OrderResponseDTO:
        # 1. Crear los objetos de valor/entidades del dominio
        items = [
            OrderItem(
                product_id=item_dto.product_id,
                quantity=item_dto.quantity,
                unit_price=item_dto.unit_price,
            )
            for item_dto in dto.items
        ]

        order = Order.create(customer_id=dto.customer_id, items=items)

        # 2. Ejecutar la persistencia atómica con Unit of Work
        with self.uow:
            self.uow.orders.add(order)
            self.uow.commit()

        # 3. Despachar eventos de dominio acumulados en la entidad tras el commit exitoso
        self.event_bus.publish(order.events)
        order.events.clear()

        # 4. Retornar DTO de respuesta
        return OrderResponseDTO(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total_amount=order.total_amount,
            status=order.status,
        )
