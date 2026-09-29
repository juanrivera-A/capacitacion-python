from fastapi import FastAPI

from .application.event_bus import EventBus
from .infrastructure.api import create_order_router
from .infrastructure.database import (
    Base,
    engine,
    sessionmaker_factory,
)
from .infrastructure.uow_impl import SQLAlchemyUnitOfWork

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Management System")

# Instanciar UoW e Inyección de Dependencias
uow = SQLAlchemyUnitOfWork(session_factory=sessionmaker_factory)
event_bus = EventBus()

app.include_router(create_order_router(uow=uow, event_bus=event_bus))


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
