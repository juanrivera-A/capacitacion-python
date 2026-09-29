from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from src.modulo01.application.unit_of_work import UnitOfWorkPort
from src.modulo01.infrastructure.repository_impl import (
    SQLAlchemyOrderRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWorkPort):
    """Implementación de Unit of Work que coordina transacciones con SQLAlchemy."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> Self:
        self.session = self.session_factory()
        self.orders = SQLAlchemyOrderRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        traceback: object,
    ) -> None:
        if exc_type is not None:
            self.rollback()
        if self.session is not None:
            self.session.close()

    def commit(self) -> None:
        if self.session is not None:
            self.session.commit()

    def rollback(self) -> None:
        if self.session is not None:
            self.session.rollback()
