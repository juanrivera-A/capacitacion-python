from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field


class RegistroAuditoria(BaseModel):
    evento: str
    usuario: str
    fecha_utc: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def obtener_fecha_local(
        self, zona_horaria: str = "America/Mexico_City"
    ) -> datetime:
        return self.fecha_utc.astimezone(ZoneInfo(zona_horaria))
