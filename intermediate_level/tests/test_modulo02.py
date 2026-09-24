from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.modulo01.database import Base
from src.modulo01.models import User
from src.modulo02.dependencies import get_db
from src.modulo02.main import app
from src.modulo02.security import get_password_hash

# Motor SQLite en memoria aislado para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session]:
    """Crea las tablas en la BD en memoria antes de cada test y las elimina al finalizar."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient]:
    """Cliente HTTP de prueba que reemplaza la sesión de BD de producción por la de prueba."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_check(client: TestClient):
    """Verifica que el endpoint de salud devuelva 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_and_create_order_flow(client: TestClient, db_session: Session):
    """Prueba el flujo completo: Crear usuario -> Login JWT -> Crear Orden Protegida."""
    # 1. Crear un usuario de prueba directamente en la BD temporal
    hashed_password_val = get_password_hash("password123")
    test_user = User(
        username="juan_tester",
        email="juan@example.com",
        hashed_password=hashed_password_val,
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # 2. Hacer Login para obtener el Token JWT
    login_data = {"username": "juan_tester", "password": "password123"}
    login_response = client.post("/api/v1/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token is not None

    # 3. Intentar crear una orden SIN token (debe retornar 401 Unauthorized)
    order_payload = {
        "user_id": test_user.id,
        "items": [{"product_name": "Teclado Mecánico", "quantity": 1, "price": 120.50}],
    }
    unauthorized_response = client.post("/api/v1/orders/", json=order_payload)
    assert unauthorized_response.status_code == 401

    # 4. Crear la orden CON el token Bearer
    headers = {"Authorization": f"Bearer {token}"}
    authorized_response = client.post(
        "/api/v1/orders/", json=order_payload, headers=headers
    )
    assert authorized_response.status_code == 201
    created_order = authorized_response.json()
    assert created_order["user_id"] == test_user.id
    assert created_order["status"] == "PENDING"
    assert len(created_order["items"]) == 1

    # 5. Consultar la orden creada por ID
    order_id = created_order["id"]
    get_response = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == order_id
