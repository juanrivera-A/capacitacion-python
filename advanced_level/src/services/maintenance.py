import time
from datetime import UTC, datetime


def purge_old_records(days: int, dry_run: bool = False) -> dict[str, int | str]:
    """Simula la purga de registros antiguos en la base de datos."""
    # En un escenario real, aquí se ejecutaría una consulta SQL de eliminación
    if dry_run:
        return {
            "status": "dry_run",
            "purged_count": 0,
            "message": f"[DRY-RUN] Se habrían eliminado registros de más de {days} días.",
        }

    # Simulación de procesamiento
    time.sleep(1)
    purged_count = 42  # Valor de prueba simulado

    return {
        "status": "success",
        "purged_count": purged_count,
        "message": f"Se eliminaron {purged_count} registros antiguos ({days} días).",
    }


def check_system_health() -> dict[str, str]:
    """Verifica el estado de los componentes del sistema."""
    return {
        "database": "OK",
        "storage": "OK",
        "timestamp": datetime.now(UTC).isoformat(),
    }
