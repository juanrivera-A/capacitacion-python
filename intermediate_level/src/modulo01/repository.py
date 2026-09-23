from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Order, OrderItem, User


class UserRepository:
    """Repositorio para operaciones CRUD de la entidad User."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, username: str, email: str) -> User:
        """Crea y persiste un nuevo usuario."""
        user = User(username=username, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """Obtiene un usuario por su ID primario."""
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        """Obtiene un usuario filtrando por su nombre de usuario."""
        stmt = select(User).where(User.username == username)
        return self.db.scalars(stmt).first()

    def get_all(self) -> Sequence[User]:
        """Retorna todos los usuarios registrados."""
        stmt = select(User)
        return self.db.scalars(stmt).all()

    def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario por ID. Retorna True si existía y se eliminó."""
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True


class OrderRepository:
    """Repositorio para operaciones transaccionales de Order y OrderItem."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_order_with_items(
        self, user_id: int, items_data: list[tuple[str, int, Decimal]]
    ) -> Order:
        """
        Crea una orden junto con sus ítems en una sola transacción atómica.
        items_data es una lista de tuplas: (product_name, quantity, price)
        """
        # Creación de la orden principal
        order = Order(user_id=user_id, status="PENDING")

        # Asociación de ítems a la relación 1:N
        for product_name, quantity, price in items_data:
            item = OrderItem(
                product_name=product_name,
                quantity=quantity,
                price=price,
            )
            order.items.append(item)

        # Persistencia en base de datos
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_by_id(self, order_id: int) -> Order | None:
        """Obtiene una orden por su ID."""
        return self.db.get(Order, order_id)

    def update_order_status(self, order_id: int, new_status: str) -> Order | None:
        """Actualiza el estado de una orden existente."""
        order = self.get_order_by_id(order_id)
        if not order:
            return None
        order.status = new_status
        self.db.commit()
        self.db.refresh(order)
        return order
