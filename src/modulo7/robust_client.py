import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

import httpx

T = TypeVar("T")


class RobustHTTPClient:
    """Cliente HTTP con reintentos exponenciales, timeouts y soporte para streaming."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = httpx.Timeout(timeout)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _execute_with_retry(self, action: Callable[[], T]) -> T:
        """Ejecuta una acción con reintentos y backoff exponencial para errores 5xx y de red."""
        last_exception: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return action()
            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                last_exception = exc

                # Si es un error HTTP de cliente (4xx), no reintentamos (son errores permanente)
                if (
                    isinstance(exc, httpx.HTTPStatusError)
                    and exc.response.status_code < 500
                ):
                    raise

                if attempt == self.max_retries:
                    break

                sleep_time = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(sleep_time)

        if last_exception:
            raise last_exception
        raise RuntimeError("Error inesperado e reintentos")

    def get_json(self, endpoint: str) -> dict[str, Any]:
        """Realiza una petición GET con reintentos y retorna el JSON parsed."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        def _request() -> dict[str, Any]:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

        return self._execute_with_retry(_request)

    def download_file(
        self, endpoint: str, destination_path: Path, chunck_size: int = 8192
    ) -> Path:
        """ "Descarga un archivo por streaming en bloques (chunks) directamente a disco."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        def _download() -> Path:
            with (
                httpx.Client(timeout=self.timeout) as client,
                client.stream("GET", url) as response,
            ):
                response.raise_for_status()
                destination_path.parent.mkdir(parents=True, exist_ok=True)
                with destination_path.open("wb") as file:
                    for chunk in response.iter_bytes(chunk_size=chunck_size):
                        file.write(chunk)

            return destination_path

        return self._execute_with_retry(_download)
