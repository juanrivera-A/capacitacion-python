from typing import Any

from src.modulo6.config import DATA_DIR, LOGS_DIR, configurar_logger
from src.modulo6.parsers import guardar_json, leer_csv

logger = configurar_logger(LOGS_DIR)


def procesar_laboratorio() -> None:
    logger.info("Iniciando ejecución del laboratorio 06...")

    # 1. Manipulación segura de rutas con pathlin
    ruta_cvs = DATA_DIR / "ventas.csv"
    ruta_json_metricas = DATA_DIR / "metricas_ventas.json"

    if not ruta_cvs.exists():
        logger.error("El archivo de entrada no existe: %s", ruta_cvs)
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_cvs}")

    # 2. Ingesta de CSV
    logger.debug("Leyendo archivo CSV desde %s", ruta_cvs)
    registros = leer_csv(ruta_cvs)
    logger.info("Se cargaron %d registros desde el CSV.", len(registros))

    # 3. Procesamiento de métricas y logging con distintos niveles
    total_ventas = 0.0
    productos_procesados = 0
    anomalias_detectadas = 0

    for fila in registros:
        try:
            cantidad = int(fila.get("cantidad", 0))
            precio = float(fila.get("precio_unitario", 0.0))
            producto = fila.get("producto", "Desconocido")

            # Logging nivel WARNING para casos anómalos/no procesables comercialmente
            if cantidad <= 0:
                logger.warning(
                    "Registro anómalo ignorado (cantidad <= 0) -> Producto: %s | Cantidad: %d",
                    producto,
                    cantidad,
                )
                anomalias_detectadas += 1
                continue

            subtotal = cantidad * precio
            total_ventas += subtotal
            productos_procesados += 1

            logger.debug(
                "Procesado: %s | Cantidad: %d | Subtotal: $%.2f",
                producto,
                cantidad,
                subtotal,
            )

        except ValueError as err:
            logger.error("Error al convertir tipos de datos en fila %s: %s", fila, err)

    ticket_promedio = (
        total_ventas / productos_procesados if productos_procesados > 0 else 0.0
    )

    metricas: dict[str, Any] = {
        "total_registros_csv": len(registros),
        "registros_validos": productos_procesados,
        "registros_anomalos": anomalias_detectadas,
        "monto_total_ventas": round(total_ventas, 2),
        "ticket_promedio": round(ticket_promedio, 2),
    }

    logger.info("Métricas calculadas con éxito: %s", metricas)

    # 5. Exportación a JSON
    guardar_json(datos=metricas, ruta=ruta_json_metricas)
    logger.info("Exportación finalizada a %s", ruta_json_metricas)


if __name__ == "__main__":
    procesar_laboratorio()
