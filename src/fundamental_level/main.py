import json
import re
from pathlib import Path


def procesar_usuarios(ruta_relativa: str) -> list[dict]:
    path = Path(ruta_relativa)

    patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    usuarios_validos = []

    try:
        with open(path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for registro in datos:
            match registro:
                case {
                    "id": int(user_id),
                    "nombre": str(nombre),
                    "email": str(email),
                    "activo": True,
                }:
                    # Expresión Regular: Validar sintaxis del email
                    if re.match(patron_email, email):
                        usuarios_validos.append(
                            {
                                "id": user_id,
                                "nombre": nombre.strip().title(),
                                "email": email,
                            }
                        )
                case _:
                    continue

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_relativa}'.")
    except json.JSONDecodeError:
        print(f"Error: El archivo '{ruta_relativa}' no contiene un JSON válido.")
    except OSError as e:
        print(f"Error inesperado al procesar el archivo: {e}")

    return usuarios_validos


if __name__ == "__main__":
    resultado = procesar_usuarios("usuarios.json")
    print(f"Usuarios procesados con éxito ({len(resultado)}):")
    print(resultado)
