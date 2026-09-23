# 1. Sintaxis, Identación, Varibales y Alcance

# En Python se utiliza la identación (4 espacios) como regla sintactica.

if True:
    print("Esto está dentro del bloque")

"""
Variables y Type Hints
Python es un lenguaje de tipado dinámico y fuerte: 
Dinamico: No necesitamo declarar el tipo de variable
Fuerte: No convierte tipos de datos automáticamente en operaciones incompatibles
"""

# Desde Python 3.5+, es una buena practica utilizar Type Hints (Pistas de tipo )

# Sintxis estándar con type hint
edad: int = 25
nombre: str = "Juan"
precio: float = 1999.99
activo: bool = True

""""
- Alcance de Variables(Scope - Regla LEGB)
- El alcande determina en qué parte del código una variable es accesible.
- Busca variables siguiendo el orden LEGB: 

L(Local): Variables creadas dentro de una función o método
E(Enclosing): Variables en funciones anidadas
G(Global): Variables declaradas en el nivel superior del archivo
B(Built-in): Nombres reservados nativos de Python (print, len, int)
"""

# Variable GLOBAL
CONFIG_PORT: int = 8000


def iniciar_servidor() -> None:
    # Variable LOCAL
    host: str = "localhost"
    print(f"Servidor en http://{host}:{CONFIG_PORT}")


# 2. Tipos básicos y colecciones(lit, dict, set, tuple)

"""
list | [1, 2, 3] | ORDENADA |MUTABLE| Secuencias dinámicas de elementos 
tuple| (1, 2, 3) | ORDENADA |NO MUTABLE| Datos inmutables, retornar mútiples valores
dict | {"k": "v"}| ORDENADA |MUTABLE| Estructura tipo JSON (Clave - Valor)
set  | {1, 2, 3} |NO ORDENADA|MUTABLE| Operaciones de conjuntos y eliminar duplicados|
"""

# LISTAS (list)
frutas: list[str] = ["manzana", "banana"]
frutas.append("cereza")
frutas[0] = "pera"

# TUPLA (tuple)
config_db: tuple[str, int] = ("localhost", 5432)
# config_db[0] = "127.0.0.1" # Erro: las tuplas son inmutables

# DICCIONARIO (dict)
usuario: dict[str, str | int] = {"nombre": "Juan", "edad": 25}

# CONJUNTOS (set)
lenguajes_a: set[str] = {"Python", "Java", "C++"}
lenguajes_b: set[str] = {"Python", "Docker"}
comunes: set[str] = lenguajes_a.intersection(lenguajes_b)

# 3 Control de flujo y Patter Matching
# Estándar(if, for, while)

# Bucle for con condicional
numeros: list[int] = [1, 2, 3, 4, 5]
pares: list[int] = []

for num in numeros:
    if num % 2 == 0:
        pares.append(num)

# Bucle while
contador: int = 3
while contador > 0:
    contador -= 1


# Patter Matching(match-case)
# Es el equivalente moderno a switch, pero mucho más potente porque permite evaluar estructuras de datos completas y validar tipos.


def procesar_respuesta(respuesta: dict) -> str:
    match respuesta:
        case {"status": 200, "data": contenido}:
            return f"Éxito: {contenido}"
        case {"status": 404}:
            return "Error: Recurso no encontrado"
        case {"status": int(codigo)} if codigo >= 500:
            return f"Error de servidor: {codigo}"
        case _:
            return "Respuesta no reconocida"


# 4. Control y gestión de excepciones (try-except)

"""
Para asegurar que un programa no falle catastróficamente, 
atrapamos excepciones específicas (ValueError, FileNotFoundError, etc.) en lugar de usar un except genérico.
"""


def dividir_numeros(a: str, b: str) -> None:
    try:
        num_a = float(a)
        num_b = float(b)
        resultado = num_a / num_b
    except ValueError:
        print("Erorr: Ambos valores deben ser números válidos.")
    except ZeroDivisionError:
        print("Error: No es posible dividir entre cero.")
    else:
        print(f"El resultado es: {resultado}")
    finally:
        print("Operación de división completada.")


# Bloque de ejecucución

if __name__ == "__main__":
    print("\n--- 1. Alcance ---")
    iniciar_servidor()

    print("\n--- 2. Colecciones ---")
    print(f"Frutas: {frutas}")
    print(f"DB Config: {config_db}")
    print(f"Usuario: {usuario}")
    print(f"Lenguajes en común: {comunes}")

    print("\n--- 3. Pattern Matching ---")
    print(procesar_respuesta({"status": 200, "data": "Conexión OK"}))
    print(procesar_respuesta({"status": 404}))

    print("\n--- 4. Excepciones ---")
    dividir_numeros("10", "2")
    dividir_numeros("10", "0")
