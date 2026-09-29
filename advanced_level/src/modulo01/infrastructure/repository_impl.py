from sqlalchemy.orm import Session

from ...modulo01.adapters.repositories import OrderRepositoryPort
from ...modulo01.domain.order import Order, OrderItem


class SQLAlchemyOrderRepository(OrderRepositoryPort):
    """Adaptador de persistencia usando una sesión activa de SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, order: Order) -> None:
        from ...modulo01.infrastructure.database import (
            OrderItemModel,
            OrderModel,
        )

        order_record = OrderModel(
            order_id=order.order_id,
            customer_id=order.customer_id,
            status=order.status,
        )
        self.session.merge(order_record)

        for item in order.items:
            item_record = OrderItemModel(
                order_id=order.order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            self.session.add(item_record)

    def get_by_id(self, order_id: str) -> Order | None:
        from ...modulo01.infrastructure.database import (
            OrderItemModel,
            OrderModel,
        )

        order_record = (
            self.session.query(OrderModel)
            .filter(OrderModel.order_id == order_id)
            .first()
        )
        if order_record is None:
            return None

        item_records = (
            self.session.query(OrderItemModel)
            .filter(OrderItemModel.order_id == order_id)
            .all()
        )

        items = [
            OrderItem(
                product_id=str(rec.product_id),
                quantity=int(rec.quantity),
                unit_price=float(rec.unit_price),
            )
            for rec in item_records
        ]

        return Order(
            order_id=str(order_record.order_id),
            customer_id=str(order_record.customer_id),
            items=items,
            status=str(order_record.status),
        )
