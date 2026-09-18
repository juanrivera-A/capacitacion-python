import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps

# 1. Argumentos posicionales, nombrados, *args y *kwargs


def registrar_evento(
    nivel: str, *mensajes: str, notificar: bool = False, **detalles: str | int
) -> None:
    # *mensajes (tuple): Atrapa cualquier cantidad de argumentos posicionales extra
    # **detalles (dict): Atrapa cualquier cantidad de argumentos nombrados (llave = valor)

    texto_mensaje = " | ".join(mensajes)
    meta = ", ".join(f"{k}={v}" for k, v in detalles.items())
    print(
        f"[{nivel.upper()}]{texto_mensaje} -> Opciones: [{meta}] (Notificar: {notificar})"
    )


# 2. Lamdas, closures y decoradores


def multiplicador(x: int, y: int) -> int:
    return x * y


# Clousure: Función que recuerda el estado de su entorno exterior (enclosing scope)
def crear_sumador(factor: int) -> Callable[[int], int]:
    def sumar(numero: int) -> int:
        return numero + factor

    return sumar


# Decorator profesional con @wraps
def medir_tiempo(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"[{func.__name__}] tiempo de ejecución: {fin - inicio:.4f}s")
        return resultado

    return wrapper


@medir_tiempo
def computar_potencias(limite: int) -> list[int]:
    return [i**2 for i in range(limite)]


# 3. Iteradores, generadores y comprensiones


def generador_lotes(datos: list[int], tamaño_lote: int) -> Generator[list[int]]:
    """ " Generador que rinde (yield) elementos por bloques sin saturar memoria."""
    for i in range(0, len(datos), tamaño_lote):
        yield datos[i : i + tamaño_lote]


# 4. Context managers (Sintaxis `whit`)


@contextmanager
def gestor_bloque_log(titulo: str):
    """Context manager simple para delimitar bloques de código."""
    print(f"\n--- INICIO: {titulo} ---")
    try:
        yield
    finally:
        print(f"--- FIN: {titulo} ---\n")


# Bloque de ejecución

if __name__ == "__main__":
    with gestor_bloque_log("1. Argumentos y Flexibilidad"):
        registrar_evento(
            "info",
            "Conexión BD",
            "Puerto 5432",
            notificar=True,
            host="localhost",
            reintentos=3,
        )

    with gestor_bloque_log("2. Lambdas, Closures y Decoradores"):
        print(f"Lambda multiplicador: 5 * 4 = {multiplicador(5, 4)}")
        sumar_diez = crear_sumador(10)
        print(f"Closure sumar_diez(15): {sumar_diez(15)}")
        potencias = computar_potencias(100_000)

    with gestor_bloque_log("3. Generadores y Comprensiones"):
        # List comprehension vs Generator Expression
        lista = [x for x in range(10) if x % 2 == 0]
        print(f"List comprehension (memoria inmediata): {lista}")

        elementos = list(range(1, 10))
        print(f"Procesando lotes de 3 desde {elementos}:")
        for lote in generador_lotes(elementos, 3):
            print(f"  -> Lote procesado: {lote}")
