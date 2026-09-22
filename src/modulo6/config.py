from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from src.modulo6.logger import configurar_logger

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

logger = configurar_logger(LOGS_DIR)


def cargar_configuracion(ruta_config: Path) -> dict[str, Any]:
    if not ruta_config.exists():
        logger.error("El archivo de configuración no existe: %s", ruta_config)
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_config}")

    logger.info("Cargando archivo de configuración desde: %s", ruta_config)
    with ruta_config.open(mode="r", encoding="utf-8") as f:
        config: dict[str, Any] = yaml.safe_load(f)
        return config
