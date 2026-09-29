import typer
from rich.console import Console
from rich.table import Table

from src.config import settings
from src.services.maintenance import check_system_health, purge_old_records

app = typer.Typer(help="Comandos de mantenimiento y automatización del sistema.")
console = Console()


@app.command("health")
def health_check() -> None:
    """Verifica la salud del sistema y la configuración activa."""
    health_data = check_system_health()

    table = Table(title=f"Estado del Sistema - {settings.app_name}")
    table.add_column("Componente", style="cyan", no_wrap=True)
    table.add_column("Estado", style="green")

    table.add_row("Entorno", settings.environment)
    table.add_row("Base de Datos", health_data["database"])
    table.add_row("Almacenamiento", health_data["storage"])
    table.add_row("Timestamp UTC", health_data["timestamp"])

    console.print(table)


@app.command("purge")
def purge(
    days: int = typer.Option(
        30, "--days", "-d", help="Días de antigüedad para purgar registros."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Simula la eliminación sin borrar datos."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Omite la confirmación del usuario."
    ),
) -> None:
    """Purgar registros obsoletos de la base de datos."""
    if not force and not dry_run:
        confirm = typer.confirm(
            f"¿Estás seguro de eliminar registros de más de {days} días?"
        )
        if not confirm:
            console.print("[yellow]Operación cancelada por el usuario.[/yellow]")
            raise typer.Exit(code=0)

    result = purge_old_records(days=days, dry_run=dry_run)

    if result["status"] == "dry_run":
        console.print(f"[bold yellow]{result['message']}[/bold yellow]")
    else:
        console.print(f"[bold green]✔ {result['message']}[/bold green]")
