import pytest

from src.modulo7.client import APIClient
from src.modulo7.resiliency import execute_safe_request
from src.modulo7.smocker_client import SmockerClient


@pytest.fixture(autouse=True)
def setup_smocker() -> SmockerClient:
    """Fixture que reinicia Smocker antes de cada prueba."""
    client = SmockerClient()
    client.reset()
    return client


def test_get_user_success(setup_smocker: SmockerClient) -> None:
    # 1. Registrar el mock en Smocker
    setup_smocker.add_mock(
        [
            {
                "request": {"method": "GET", "path": "/api/v1/users/1"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"id": 1, "name": "Juan Rivera"}',
                },
            }
        ]
    )

    # 2. Ejecutar la llamada usando nuestro APIClient
    api_client = APIClient(base_url="http://localhost:8080")
    response = api_client.get_data("/api/v1/users/1")

    # 3. Assertions
    assert response is not None
    assert response["id"] == 1
    assert response["name"] == "Juan Rivera"


def test_timeout_handling(setup_smocker: SmockerClient) -> None:
    # 1. Smocker tardará 5 segundos en responder
    setup_smocker.add_mock(
        [
            {
                "request": {"method": "GET", "path": "/api/v1/slow"},
                "response": {
                    "status": 200,
                    "body": '{"status": "ok"}',
                },
                "context": {
                    "delay": "3000ms",
                },
            }
        ]
    )

    # 2. Cliente con timeout súper estricto de 0.5 segundos
    api_client = APIClient(base_url="http://10.255.255.1:8080", timeout=0.5)
    result = execute_safe_request(lambda: api_client.get_data("/api/v1/slow"))

    assert result is None
