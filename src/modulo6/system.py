import subprocess


def obtener_version_git() -> str:
    """Obtiene la versión de Git intalada en el sistema"""
    try:
        resultado = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar git: {e.stderr}"
