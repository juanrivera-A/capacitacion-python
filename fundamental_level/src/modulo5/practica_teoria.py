from typing import Literal, Protocol, TypedDict

# 1. Typeddict: Estructura de diccionario tipada


class ConfigServicio(TypedDict):
    """Estructura fija de configuración para el procesador de pagos."""

    ambiente: Literal["DESARROLLO", "PRUEBAS", "PRODUCCIÓN"]
    timeout_segundos: int
    reintentos_maximos: int


# 2. Literal: Tipos restringidos a valores exactos

EstadoTransaccion = Literal["SUCCESS", "FAILED", "PENDING"]

# 3. Protocol: Subtipado Estructural


class ProcesadorPago(Protocol):
    """Protocolo que define la interfaz esperada para procesar pagos.

    Cualquier clase que implemente el método `procesar` con esta firma
    exacta cumplirá el protocolo dinámicamente sin heredar.
    """

    def procesar(self, monto: float) -> EstadoTransaccion: ...


# 4. Implementaciones (Sin heredar explícitamente de ProcesadorPago)


class PasarelaStripe:
    """Implementa ProcesadorPago implícitamente por su estructura."""

    def __init__(self, config: ConfigServicio) -> None:
        self.config = config

    def procesar(self, monto: float) -> EstadoTransaccion:
        print(
            f"Procesando ${monto:.2f} vía Stripe en ambiente [{self.config['ambiente']}]..."
        )
        return "SUCCESS"


class PasarelaPaypal:
    """Otra implementación independiente que cumple con el Protocolo."""

    def procesar(self, monto: float) -> EstadoTransaccion:
        print(f"Procesando ${monto:.2f} vía Paypal...")
        return "SUCCESS"


# 5. Lógica de negocio que consume el protocolo


def ejecutar_cobor(procesador: ProcesadorPago, monto: float) -> None:
    """Función desaclopada que recibe cualquier objeto alineado con ProcesadorPago."""
    resultado: EstadoTransaccion = procesador.procesar(monto)
    print(f"Resultados del cobro: {resultado}\n")


if __name__ == "__main__":
    print("PRÁCTICA TEÓRIA MÓDULO 5: TYPING AVANZADO")

    # Configuración basada en TypedDict
    config: ConfigServicio = {
        "ambiente": "DESARROLLO",
        "timeout_segundos": 30,
        "reintentos_maximos": 3,
    }

    stripe = PasarelaStripe(config)
    paypal = PasarelaPaypal()

    ejecutar_cobor(stripe, 150.00)
    ejecutar_cobor(paypal, 89.90)
