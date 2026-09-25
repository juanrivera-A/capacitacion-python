# src/modulo05/contracts.py
from typing import Protocol, TypedDict


class UserDTO(TypedDict):
    """Representación fuertemente tipada de un usuario."""

    user_id: str
    email: str
    name: str


class UserRepositoryProtocol(Protocol):
    """Puerto / Interfaz que abstrae la persistencia de usuarios.

    Cualquier repositorio concreto DEBE implementar estos métodos
    respetando exactamente los tipos de entrada y retorno (LSP).
    """

    def save(self, user_id: str, email: str, name: str) -> UserDTO: ...

    def find_by_id(self, user_id: str) -> UserDTO | None: ...

    def find_by_email(self, email: str) -> UserDTO | None: ...
