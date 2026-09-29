from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Información general de la app
    app_name: str = "Order Service CLI"
    environment: str = "development"
    debug: bool = False

    # Base de datos (SQLite por defecto apuntando al directorio local)
    database_url: str = "sqlite:///./app.db"

    # API / Configuración sensible
    api_key: SecretStr | None = None

    # Configuración de Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Instancia global para importar en toda la aplicación
settings = Settings()
