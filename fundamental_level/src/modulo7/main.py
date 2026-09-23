from src.modulo7.client import APIClient
from src.modulo7.resiliency import execute_safe_request


def run() -> None:
    # Usaremos JSONPlaceholder como API pública de pruebas
    client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    print("--- 1. Petición GET sincrónica básica ---")
    data = execute_safe_request(lambda: client.get_data("/posts/1"))
    if data:
        print("Título del post:", data.get("title"))

    print("\n--- 2. Manejo de error (Endpoint inexistente) ---")
    execute_safe_request(lambda: client.get_data("/invalid-endpoint-404"))


if __name__ == "__main__":
    run()
