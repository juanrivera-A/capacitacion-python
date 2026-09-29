from typer.testing import CliRunner

from src.cli.main import app

runner = CliRunner()


def test_cli_health_check() -> None:
    """Verifica que el comando health responda con código 0 y muestre el estado."""
    result = runner.invoke(app, ["maintenance", "health"])
    assert result.exit_code == 0
    assert "Estado del Sistema" in result.stdout
    assert "development" in result.stdout


def test_cli_purge_dry_run() -> None:
    """Verifica la ejecución del comando purge en modo dry-run."""
    result = runner.invoke(app, ["maintenance", "purge", "--days", "15", "--dry-run"])
    assert result.exit_code == 0
    assert "[DRY-RUN]" in result.stdout
    assert "15 días" in result.stdout


def test_cli_purge_cancel_without_force() -> None:
    """Verifica que la purga sin --force pida confirmación y se cancele si se responde 'n'."""
    result = runner.invoke(app, ["maintenance", "purge", "--days", "10"], input="n\n")
    assert result.exit_code == 0
    assert "Operación cancelada" in result.stdout
