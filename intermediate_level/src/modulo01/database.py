from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# URL para desarrollo / pruebas locales con SQLite
DATABASE_URL = "sqlite:///./app.db"

# Engine de SQLAlchemy 2.0
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver el SQL generado durante depuración
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Clase Base Declarativa para los modelos ORM
class Base(DeclarativeBase):
    pass


# Generador / Inyector de sesiones
def get_db() -> Generator[Session]:
    """Provee una sesión de base de datos dentro de un bloque de contexto."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
