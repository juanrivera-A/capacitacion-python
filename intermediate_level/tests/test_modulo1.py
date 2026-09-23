from collections.abc import Generator
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.modulo01.database import Base
from src.modulo01.repository import OrderRepository, UserRepository


@pytest.fixture
def db_session() -> Generator[Session]:
    """Crea una base de datos SQLite en memoria limpia para cada prueba."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_create_and_get_user(db_session: Session) -> None:
    """Verifica la creación y recuperación de un usuario."""
    repo = UserRepository(db_session)
    user = repo.create_user(username="juan_dev", email="juan@example.com")

    assert user.id is not None
    assert user.username == "juan_dev"

    fetched_user = repo.get_by_username("juan_dev")
    assert fetched_user is not None
    assert fetched_user.id == user.id


def test_create_order_with_items_transaction(db_session: Session) -> None:
    """Verifica la creación transaccional de una orden con sus ítems."""
    user_repo = UserRepository(db_session)
    order_repo = OrderRepository(db_session)

    user = user_repo.create_user(username="cliente1", email="cliente1@example.com")

    items_data = [
        ("Teclado Mecánico", 1, Decimal("1500.00")),
        ("Mouse Inalámbrico", 2, Decimal("450.50")),
    ]

    order = order_repo.create_order_with_items(user_id=user.id, items_data=items_data)

    assert order.id is not None
    assert order.user_id == user.id
    assert order.status == "PENDING"
    assert len(order.items) == 2
    assert order.items[0].product_name == "Teclado Mecánico"


def test_delete_user_cascade(db_session: Session) -> None:
    """Verifica la eliminación de un usuario y la eliminación en cascada."""
    user_repo = UserRepository(db_session)
    user = user_repo.create_user(username="delete_me", email="del@example.com")

    deleted = user_repo.delete_user(user.id)
    assert deleted is True

    assert user_repo.get_by_id(user.id) is None
