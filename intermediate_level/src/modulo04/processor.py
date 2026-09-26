# src/modulo04/processor.py
from concurrent.futures import ProcessPoolExecutor


def compute_heavy_task(n: int) -> int:
    """Cálculo CPU-bound intensivo (suma de cuadrados)."""
    return sum(i * i for i in range(n))


def run_cpu_tasks_parallel(numbers: list[int]) -> list[int]:
    """Ejecuta múltiples tareas CPU-bound en paralelo aprovechando ProcessPoolExecutor."""
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_heavy_task, numbers))
    return results
