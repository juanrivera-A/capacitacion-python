from ...modulo08.application.order_dtos import (
    CreateOrderDTO,
    OrderResponseDTO,
)
from ...modulo08.application.order_ports import (
    HTTPNotifierPort,
    OrderRepositoryPort,
)
from ...modulo08.domain.order import Order, OrderItem


class CreateOrderUseCase:
    """Caso de uso: Crear e ingresar una nueva orden en el sistema."""

    def __init__(
        self,
        repository: OrderRepositoryPort,
        notifier: HTTPNotifierPort,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def execute(self, dto: CreateOrderDTO) -> OrderResponseDTO:
        # 1. Convertir DTOs a entidades de dominio
        items = [
            OrderItem(
                product_id=item_dto.product_id,
                quantity=item_dto.quantity,
                unit_price=item_dto.unit_price,
            )
            for item_dto in dto.items
        ]

        # 2. Instanciar entidad y aplicar reglas de negocio
        order = Order.create(customer_id=dto.customer_id, items=items)

        # 3. Persistir usando el puerto
        self.repository.save(order)

        # 4. Notificar mediante el puerto HTTP
        self.notifier.notify_order_created(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total_amount=order.total_amount,
        )

        # 5. Retornar DTO de respuesta
        return OrderResponseDTO(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total_amount=order.total_amount,
            status=order.status.value,
        )
