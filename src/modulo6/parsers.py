import csv
import json
from pathlib import Path
from typing import Any

from src.modulo6.logger import configurar_logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
logger = configurar_logger(LOGS_DIR)


def guardar_json(datos: dict[str, Any], ruta: Path) -> None:
    """Guarda un diccionario en un archivo JSON"""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Guardando archivo JSON en: %s", ruta)
    with ruta.open(mode="w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    """Lee un archivo CSV y retorna una lista de diccionarios"""
    if not ruta.exists():
        logger.error("El archivo CSV no existe: %s", ruta)
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    logger.info("Leyendo archivo CSV desde %s", ruta)
    with ruta.open(mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        registros = list(reader)

    return registros
