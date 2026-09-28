import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modulo08.application.create_order_use_case import CreateOrderUseCase
from src.modulo08.application.order_dtos import CreateOrderDTO, OrderItemDTO
from src.modulo08.application.order_ports import OrderRepositoryPort
from src.modulo08.domain.order import InvalidOrderError, Order, OrderItem
from src.modulo08.infrastructure.adapters.http_notifier import (
    MockHTTPNotifierAdapter,
)
from src.modulo08.infrastructure.adapters.order_in_memory_db import (
    InMemoryOrderRepositoryAdapter,
)
from src.modulo08.infrastructure.adapters.order_sqlalchemy_db import (
    Base,
    SQLAlchemyOrderRepositoryAdapter,
)

# Fixtures para los Adaptadores Intercambiables


@pytest.fixture
def in_memory_repo() -> InMemoryOrderRepositoryAdapter:
    return InMemoryOrderRepositoryAdapter()


@pytest.fixture
def sqlalchemy_repo() -> SQLAlchemyOrderRepositoryAdapter:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return SQLAlchemyOrderRepositoryAdapter(session_factory=session_factory)


@pytest.fixture
def mock_notifier() -> MockHTTPNotifierAdapter:
    return MockHTTPNotifierAdapter()


# 1. PRUEBAS DE DOMINIO (Reglas de Negocio en la Entidad Order)


def test_order_creation_and_total_calculation():
    items = [
        OrderItem(product_id="P100", quantity=2, unit_price=25.0),
        OrderItem(product_id="P200", quantity=1, unit_price=50.0),
    ]
    order = Order.create(customer_id="CUST-01", items=items)

    assert order.customer_id == "CUST-01"
    assert order.total_amount == 100.0


def test_invalid_order_empty_items_raises_error():
    with pytest.raises(InvalidOrderError):
        Order.create(customer_id="CUST-01", items=[])


def test_invalid_item_quantity_raises_error():
    with pytest.raises(InvalidOrderError):
        OrderItem(product_id="P100", quantity=0, unit_price=10.0)


# 2. PRUEBAS DE CONTRATO (Garantiza Intercambiabilidad de Repositorios)


@pytest.mark.parametrize("repo_fixture", ["in_memory_repo", "sqlalchemy_repo"])
def test_order_repository_contract(repo_fixture, request):
    repo: OrderRepositoryPort = request.getfixturevalue(repo_fixture)

    items = [OrderItem(product_id="P1", quantity=3, unit_price=10.0)]
    order = Order.create(customer_id="CUST-99", items=items)

    # 1. Guardar mediante el puerto
    repo.save(order)

    # 2. Recuperar mediante el puerto
    retrieved = repo.get_by_id(order.order_id)
    assert retrieved is not None
    assert retrieved.order_id == order.order_id
    assert retrieved.customer_id == "CUST-99"
    assert retrieved.total_amount == 30.0
    assert len(retrieved.items) == 1


# 3. PRUEBA INTEGRADA DEL CASO DE USO (CreateOrder)


def test_create_order_use_case_execution(in_memory_repo, mock_notifier):
    use_case = CreateOrderUseCase(repository=in_memory_repo, notifier=mock_notifier)

    dto = CreateOrderDTO(
        customer_id="CUST-123",
        items=[
            OrderItemDTO(product_id="PROD-A", quantity=2, unit_price=15.0),
            OrderItemDTO(product_id="PROD-B", quantity=1, unit_price=20.0),
        ],
    )

    response = use_case.execute(dto)

    assert response.order_id is not None
    assert response.customer_id == "CUST-123"
    assert response.total_amount == 50.0
    assert response.status == "CREATED"

    # Verificar que el puerto HTTP simulado recibió la notificación
    assert len(mock_notifier.requests_log) == 1
    assert mock_notifier.requests_log[0]["customer_id"] == "CUST-123"
    assert mock_notifier.requests_log[0]["total_amount"] == 50.0
