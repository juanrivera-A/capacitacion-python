from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ....modulo08.application.order_ports import OrderRepositoryPort
from ....modulo08.domain.order import Order, OrderItem, OrderStatus


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    status = Column(String, nullable=False)


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)


class SQLAlchemyOrderRepositoryAdapter(OrderRepositoryPort):
    """Adaptador de infraestructura: Base de datos SQL vía SQLAlchemy."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def save(self, order: Order) -> None:
        with self.session_factory() as session:
            # Insertar o actualizar la orden principal
            order_record = OrderModel(
                order_id=order.order_id,
                customer_id=order.customer_id,
                status=order.status.value,
            )
            session.merge(order_record)

            # Insertar los ítems asociados
            for item in order.items:
                item_record = OrderItemModel(
                    order_id=order.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                session.add(item_record)

            session.commit()

    def get_by_id(self, order_id: str) -> Order | None:
        with self.session_factory() as session:
            order_record = (
                session.query(OrderModel)
                .filter(OrderModel.order_id == order_id)
                .first()
            )
            if order_record is None:
                return None

            item_records = (
                session.query(OrderItemModel)
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
                status=OrderStatus(str(order_record.status)),
            )
