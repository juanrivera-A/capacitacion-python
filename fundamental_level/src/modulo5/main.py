from typing import Literal, Protocol, TypedDict

# 1. Typeddict y Literales (Estructuras y Estados)


class UsuarioResponseDict(TypedDict):
    """Estructura esperada al recibir un usuario de una API externa"""

    id: int
    username: str
    rol: Literal["ADMIN", "USER", "GUEST"]
    activo: bool


# 2. Protocol con duck typing estático


class RepositorioUsuario(Protocol):
    """Protocolo que define las operaciones de pesistencia/consulta."""

    def obtener_por_id(sel, usuario_id: int) -> UsuarioResponseDict | None: ...

    def guardar(self, usuario: UsuarioResponseDict) -> bool: ...


# 3. Implementación de repositorio (Sin herencia explicita)


class MemoriaUsuarioRepository:
    """Implementa RespositorioUsuario implícitamente por su firma."""

    def __init__(self) -> None:
        self._db: dict[int, UsuarioResponseDict] = {}

    def obtener_por_id(self, usuario_id: int) -> UsuarioResponseDict | None:
        return self._db.get(usuario_id)

    def guardar(self, usuario: UsuarioResponseDict) -> bool:
        self._db[usuario["id"]] = usuario
        return True


# 4. Servicio de negocio y manejo de tipo opcional


class ServicioUsuario:
    def __init__(self, repo: RepositorioUsuario) -> None:
        self.repo = repo

    def registrar_usuario(
        self, usuario_id: int, username: str, rol: Literal["ADMIN", "USER", "GUEST"]
    ) -> bool:
        nuevo_usuario: UsuarioResponseDict = {
            "id": usuario_id,
            "username": username,
            "rol": rol,
            "activo": True,
        }
        return self.repo.guardar(nuevo_usuario)

    def obtener_rol_normalizado(self, usuario_id: int) -> str:
        usuario = self.repo.obtener_por_id(usuario_id)

        # Manejo estricto de Opcional / None exigido pro mypy
        if usuario is None:
            return "DESCONOCIDO"
        return usuario["rol"].lower()


if __name__ == "__main__":
    print("LABORATORIO MÓDULO 5: TIPADO ESTATICO Y CALIDAD")

    repo = MemoriaUsuarioRepository()
    servicio = ServicioUsuario(repo)

    # 1.  Registro y consulta exitosos
    servicio.registrar_usuario(1, "jrivera", "ADMIN")
    rol = servicio.obtener_rol_normalizado(1)
    print(f"Usuario registrado correctamente. Rol normalizado: {rol}")

    # 2. Desmostración de dinamismo vs. mypy con type: ignore
    payload_dinamico: dict = {
        "id": 2,
        "username": "guest_user",
        "rol": "INVITADO",
        "activo": True,
    }

    # Documentamos la excepción explicitamente por que "INVITADO" no pertenece al Literal
    repo.guardar(payload_dinamico)  # type: ignore[arg-type]
    print("Obejto guardado forzando el tipo mediante bypass documentado.")
