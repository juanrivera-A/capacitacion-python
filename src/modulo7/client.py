from typing import Any

import httpx


class APIClient:
    """Cliente para consumir servicios HTTP usando httpx."""

    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def get_data(self, endpoint: str) -> dict[str, Any]:
        """Realiza una petición GET sincrónica y retorna el JSON parsed."""
        timeout_config = httpx.Timeout(self.timeout)
        with httpx.Client(timeout=timeout_config) as client:
            response = client.get(
                f"{self.base_url}{endpoint}",
                timeout=timeout_config,  # Pasa el timeout explícitamente a la llamada GET
            )
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
