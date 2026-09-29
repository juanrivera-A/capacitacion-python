import typer

from src.cli.commands import maintenance
from src.config import settings

app = typer.Typer(
    name="order-cli",
    help=f"CLI de administración para {settings.app_name}",
    add_completion=False,
)

# Registrar módulos de subcomandos
app.add_typer(maintenance.app, name="maintenance")


@app.callback()
def main() -> None:
    """Entrypoint principal de la interfaz de línea de comandos."""


if __name__ == "__main__":
    app()
