from dataclasses import dataclass, field
from decimal import Decimal

from pydantic import BaseModel, Field


# 1. DOMINIO: Dataclass + Dunder Method (__lt__)
@dataclass(frozen=True)
class Estudiante:
    matricula: str
    nombre: str
    calificacion_promedio: Decimal

    def __lt__(self, otro: "Estudiante") -> bool:
        if not isinstance(otro, Estudiante):
            return NotImplemented
        return self.calificacion_promedio < otro.calificacion_promedio


@dataclass
class Curso:
    nombre_curso: str
    estudiantes: list[Estudiante] = field(default_factory=list)

    @property
    def estudiante_top(self) -> Estudiante | None:
        return max(self.estudiantes) if self.estudiantes else None


# 2. ESQUEMAS: Pydantic para validación de entrada
class EstudianteIn(BaseModel):
    matricula: str = Field(..., min_length=4)
    nombre: str = Field(..., min_length=2)
    calificacion_promedio: Decimal = Field(..., ge=0, le=10)


class CursoIn(BaseModel):
    nombre_curso: str = Field(..., min_length=3)
    estudiantes: list[EstudianteIn]


# 3. EJECUCIÓN PRÁCTICA
if __name__ == "__main__":
    print("PRÁCTICA TEÓRICA: MÓDULO 4\n")

    raw_payload = {
        "nombre_curso": "Python Backend Avanzado",
        "estudiantes": [
            {
                "matricula": "EST-01",
                "nombre": "Juan",
                "calificacion_promedio": "8.5",
            },
            {
                "matricula": "EST-02",
                "nombre": "María",
                "calificacion_promedio": "9.8",
            },
        ],
    }

    # Validar entrada con Pydantic (método recomendado para diccionarios/JSON)
    dto_curso = CursoIn.model_validate(raw_payload)

    # Mapear a Entidad de Dominio
    curso = Curso(
        nombre_curso=dto_curso.nombre_curso,
        estudiantes=[
            Estudiante(e.matricula, e.nombre, e.calificacion_promedio)
            for e in dto_curso.estudiantes
        ],
    )

    top = curso.estudiante_top
    print(f"Curso creado: {curso.nombre_curso}")

    if top is not None:
        print(
            f"Estudiante destacado (usando __lt__): {top.nombre} ({top.calificacion_promedio})"
        )
    else:
        print("El curso no tiene estudiantes registrados.")
