from pathlib import Path

import pytest

from src.modulo7.robust_client import RobustHTTPClient
from src.modulo7.smocker_client import SmockerClient


@pytest.fixture(autouse=True)
def setup_smocker() -> SmockerClient:
    """Fixture que reinicia el servidor Smocker antes de cada test."""
    client = SmockerClient()
    client.reset()
    return client


def test_get_json_with_retry_success(setup_smocker: SmockerClient) -> None:
    # 1. Smocker responderá primero con 503 (1 vez) y luego con 200 OK
    # Smocker consume los mocks de forma secuencial
    setup_smocker.add_mock(
        [
            {
                "request": {"method": "GET", "path": "/api/v1/retry-test"},
                "response": {
                    "status": 503,
                    "body": '{"error": "Service Temporarily Unavailable"}',
                },
            },
            {
                "request": {"method": "GET", "path": "/api/v1/retry-test"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"status": "recovered", "attempt": 2}',
                },
            },
        ]
    )

    # 2. Cliente con backoff factor muy pequeño para no ralentizar los tests
    client = RobustHTTPClient(
        base_url="http://localhost:8080",
        max_retries=3,
        backoff_factor=0.01,
    )

    # 3. La petición debe tener éxito en el segundo intento
    data = client.get_json("/api/v1/retry-test")
    assert data["status"] == "recovered"
    assert data["attempt"] == 2


def test_download_file_streaming(setup_smocker: SmockerClient, tmp_path: Path) -> None:
    expected_content = "Contenido de archivo pesado en bloques para streaming."

    # 1. Registrar mock del archivo a descargar
    setup_smocker.add_mock(
        [
            {
                "request": {"method": "GET", "path": "/files/report.txt"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "text/plain"},
                    "body": expected_content,
                },
            }
        ]
    )

    # 2. Configurar cliente y ruta de destino usando el fixture tmp_path de pytest
    client = RobustHTTPClient(base_url="http://localhost:8080")
    destination_file = tmp_path / "downloads" / "downloaded_report.txt"

    # 3. Descargar por streaming
    saved_path = client.download_file("/files/report.txt", destination_file)

    # 4. Validar que el archivo existe en disco y su contenido es exacto
    assert saved_path.exists()
    assert saved_path.read_text(encoding="utf-8") == expected_content
