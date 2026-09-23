from src.modulo6.config import (
    BASE_DIR,
    DATA_DIR,
    LOGS_DIR,
    cargar_configuracion,
    configurar_logger,
)
from src.modulo6.models import RegistroAuditoria
from src.modulo6.parsers import guardar_json
from src.modulo6.system import obtener_version_git

logger = configurar_logger(LOGS_DIR)


def ejecutar_flujo() -> None:
    logger.info("Iniciando ejecución del módulo 06...")

    # 1. Cargar archivo YAML de configuración
    ruta_yaml = BASE_DIR / "config" / "config.yaml"
    if ruta_yaml.exists():
        app_config = cargar_configuracion(ruta_yaml)
        logger.info("Configuración cargada: %s", app_config.get("app"))

    # 2. Obtener la versión de Git (system / subprocess)
    version = obtener_version_git()
    logger.info("Versión de Git: %s", version)

    # 3. Crear registro de auditoría (models / datetime + zoneinfo)
    registro = RegistroAuditoria(evento="INICIO_PROCESO", usuario="juan_dev")
    logger.info(
        "Registro generado (Local): %s",
        registro.obtener_fecha_local().isoformat(),
    )

    # 4. Guardar en JSON (parsers / pathlib)
    ruta_salida = DATA_DIR / "auditoria.json"
    guardar_json(datos=registro.model_dump(mode="json"), ruta=ruta_salida)


if __name__ == "__main__":
    ejecutar_flujo()
