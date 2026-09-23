from typing import Any

import httpx


class SmockerClient:
    """Cliente auxiliar para interactuar con la Admin API de Smocker."""

    def __init__(
        self, admin_url: str = "http://localhost:8081", session_id: str = "default"
    ) -> None:
        self.admin_url = admin_url
        self.session_id = session_id

    def reset(self) -> None:
        """Limpia todos los mocks e historial registrados en Smocker."""
        with httpx.Client(timeout=5.0) as client:
            client.post(
                f"{self.admin_url}/sessions/reset",
                params={"session_id": self.session_id},
            )

    def add_mock(self, mock_definition: list[dict[str, Any]]) -> None:
        """Registra una lista de definiciones de mocks en Smocker."""
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                f"{self.admin_url}/mocks",
                params={"session_id": self.session_id},
                json=mock_definition,
            )
            if response.status_code >= 400:
                print(f"\n[Smocker Error Payload]: {response.text}")
            response.raise_for_status()
