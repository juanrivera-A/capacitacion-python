# src/modulo04/benchmark.py
import asyncio
import time

from src.modulo04.async_fetcher import fetch_all_async
from src.modulo04.processor import run_cpu_tasks_parallel

# Usamos URLs públicas que simulan latencia controlada (delay de 1 segundo por petición)
URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(5)]
CPU_NUMBERS = [10_000_000, 12_000_000, 15_000_000]


def run_benchmark():
    print("INICIANDO BENCHMARK DEL MÓDULO 04\n")

    # 1. Prueba Síncrona (I/O-bound)
    print(f"1. Descargando {len(URLS)} URLs secuencialmente (Síncrono)...")
    start_sync = time.perf_counter()
    fetch_all_async(URLS)
    duration_sync = time.perf_counter() - start_sync
    print(f"   -> Tiempo Síncrono: {duration_sync:.2f} segundos\n")

    # 2. Prueba Asíncrona (I/O-bound con Semáforo max_concurrent=5)
    print(f"2. Descargando {len(URLS)} URLs concurrentemente (AsyncIO)...")
    start_async = time.perf_counter()
    asyncio.run(fetch_all_async(URLS, max_concurrent=5))
    duration_async = time.perf_counter() - start_async
    print(f"   -> Tiempo Asíncrono: {duration_async:.2f} segundos\n")

    # Mejora I/O
    speedup_io = duration_sync / duration_async if duration_async > 0 else 0
    print(f" [I/O-bound] Mejora de rendimiento: {speedup_io:.2f}x más rápido\n")

    # 3. Prueba CPU-bound (ProcessPoolExecutor)
    print("3. Ejecutando tareas intensivas de CPU en paralelo...")
    start_cpu = time.perf_counter()
    cpu_results = run_cpu_tasks_parallel(CPU_NUMBERS)
    duration_cpu = time.perf_counter() - start_cpu
    print(f"   -> Tiempo de procesamiento CPU (Paralelo): {duration_cpu:.2f} segundos")
    print(f"   -> Resultados obtenidos: {len(cpu_results)} tareas completadas.\n")

    print("ENCHMARK FINALIZADO EN CONCURRENCIA")


if __name__ == "__main__":
    run_benchmark()
