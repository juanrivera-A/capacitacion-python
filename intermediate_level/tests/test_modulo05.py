# tests/test_modulo05.py
import pytest
from src.modulo05.repositories import InMemoryUserRepository, SQLiteUserRepository
from src.modulo05.service import UserService, UserServiceFactory


@pytest.fixture(
    params=[
        InMemoryUserRepository,
        lambda: SQLiteUserRepository(":memory:"),
    ]
)
def repository_instance(request):
    """Fixture parametrizada que retorna ambas implementaciones de repositorio.

    Permite comprobar de forma automatizada que ambas respetan LSP.
    """
    factory = request.param
    return factory()


def test_lsp_repository_implementations_behavior(repository_instance):
    """Verifica el cumplimiento de LSP: ambas implementaciones responden igual."""
    service = UserService(repository=repository_instance)

    # 1. Registro exitoso
    user = service.register_user("juan@example.com", "Juan Rivera")
    assert user["email"] == "juan@example.com"
    assert user["name"] == "Juan Rivera"
    assert "user_id" in user

    # 2. Búsqueda por ID
    found_user = service.get_user_by_id(user["user_id"])
    assert found_user == user

    # 3. Prevenir duplicados por email
    with pytest.raises(ValueError, match="ya existe"):
        service.register_user("juan@example.com", "Otro Nombre")


def test_register_user_invalid_email():
    service = UserServiceFactory.create_for_testing()
    with pytest.raises(ValueError, match="Formato de email inválido"):
        service.register_user("invalid-email", "Juan")


def test_register_user_empty_name():
    service = UserServiceFactory.create_for_testing()
    with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
        service.register_user("juan@example.com", "   ")


def test_get_user_by_id_not_found():
    service = UserServiceFactory.create_for_testing()
    with pytest.raises(KeyError, match="no encontrado"):
        service.get_user_by_id("non-existent-id")


def test_user_service_factory_production(tmp_path):
    db_file = str(tmp_path / "test_prod.db")
    service = UserServiceFactory.create_for_production(db_path=db_file)
    user = service.register_user("prod@example.com", "Prod User")
    assert user["email"] == "prod@example.com"
