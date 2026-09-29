from typing import Generic, Protocol, TypeVar

from ...modulo01.application.dtos import OrderResponseDTO

T = TypeVar("T", covariant=True)


class OrderPresenterPort(Protocol, Generic[T]):
    """Puerto para transformar el resultado del caso de uso."""

    def present_order_created(self, dto: OrderResponseDTO) -> T: ...
