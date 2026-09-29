from typing import Protocol, Self

from src.modulo01.adapters.repositories import OrderRepositoryPort


class UnitOfWorkPort(Protocol):
    """Interfaz para gestionar la transacción atómica (Unit of Work)."""

    orders: OrderRepositoryPort

    def __enter__(self) -> Self: ...

    def __exit__(
        self, exc_type: type | None, exc_val: Exception | None, traceback: object
    ) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
