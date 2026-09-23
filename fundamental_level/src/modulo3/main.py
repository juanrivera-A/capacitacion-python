import random
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps

# 1. Decorador de reintentos con backoff exponencial


def reintento_con_backoff(
    max_reintentos: int = 3, tiempo_base: float = 1.0
) -> Callable:
    """Decorador con argumentos que reintenta la ejecución tras una excepción.

    Aplica backoff exponencial: espera base * (2 ** intento) segundos.
    """

    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(max_reintentos):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    ultima_excepcion = e
                    espera = tiempo_base * (2**intento)
                    print(
                        f"Error en '{func.__name__}': {e}. Reintento {intento + 1}/{max_reintentos} en {espera:.1f}s..."
                    )
                    time.sleep(espera)

            # Último intento para lanzar la excepción si falla definitivamente
            print(f"Excedio el número máximo de reintentos en '{func.__name__}.")
            if ultima_excepcion:
                raise ultima_excepcion

        return wrapper

    return decorador


# 2. Generador por lotes (batch generator)


def generador_por_lotes(datos: list[dict], tamano_lote: int) -> Generator[list[dict]]:
    """Procesa sublistas de datos de un tamaño fijo para evitar cargas pesadas en memoria."""
    for i in range(0, len(datos), tamano_lote):
        yield datos[i : i + tamano_lote]


# 3. Context manager de temporización


@contextmanager
def temporizador(etiqueta: str):
    "Context manager para medir el tiempo transcurrido en un bloque ``whit."
    inicio = time.perf_counter()
    print(f"[Inicio: {etiqueta}]")
    try:
        yield
    finally:
        fin = time.perf_counter()
        print(f"[Fin]: {etiqueta}] Tiempo total: {fin - inicio:.4f} segundos\n")


# Simulación de API Reintentable
@reintento_con_backoff(max_reintentos=3, tiempo_base=0.2)
def enviar_lote_api(lote: list[dict]) -> bool:
    """Simula el enviío de un lote a un servicio web inestable."""
    if random.random() < 0.6:  # 60% de probabilidad de fallo simulado
        raise ConnectionError("Fallo de red al conectar con el servidor. ")
    print(f"Lote de {len(lote)} elementos procesado correctamente. ")
    return True


# Bloque de ejecución

if __name__ == "__main__":
    # Generar datos de prueba
    registros_simulados = [{"id": i, "data": f"payload_{i}"} for i in range(1, 11)]

    print("=== INICIANDO LABORATORIO DEL MÓDULO 3 ===\n")

    with temporizador("Procesamiento completo de lotes con API"):
        for num_lote, lote in enumerate(
            generador_por_lotes(registros_simulados, tamano_lote=3), start=1
        ):
            print(f"--- Procesando Lote #{num_lote} ({len(lote)} elementos) ---")
            try:
                enviar_lote_api(lote)
            except ConnectionError:
                print(f"Se descartó el Lote #{num_lote} tras agotar reintentos.\n")
