# src/modulo05/service.py
import uuid

from ..modulo05.contracts import UserDTO, UserRepositoryProtocol
from ..modulo05.repositories import InMemoryUserRepository, SQLiteUserRepository


class UserService:
    """Servicio de dominio de usuarios.

    Aplica DIP al depender únicamente del contrato UserRepositoryProtocol.
    Aplica SRP encargándose exclusivamente de la lógica de negocio de usuarios.
    """

    def __init__(self, repository: UserRepositoryProtocol) -> None:
        self.repository = repository

    def register_user(self, email: str, name: str) -> UserDTO:
        if "@" not in email or "." not in email:
            raise ValueError("Formato de email inválido")

        if not name.strip():
            raise ValueError("El nombre no puede estar vacío")

        existing_user = self.repository.find_by_email(email)
        if existing_user is not None:
            raise ValueError(f"El usuario con email '{email}' ya existe")

        user_id = str(uuid.uuid4())
        return self.repository.save(user_id=user_id, email=email, name=name)

    def get_user_by_id(self, user_id: str) -> UserDTO:
        user = self.repository.find_by_id(user_id)
        if user is None:
            raise KeyError(f"Usuario con ID '{user_id}' no encontrado")
        return user


class UserServiceFactory:
    """Factoría para la construcción de UserService con sus dependencias."""

    @staticmethod
    def create_for_testing() -> UserService:
        repository = InMemoryUserRepository()
        return UserService(repository=repository)

    @staticmethod
    def create_for_production(db_path: str = "app.db") -> UserService:
        repository = SQLiteUserRepository(db_path=db_path)
        return UserService(repository=repository)
