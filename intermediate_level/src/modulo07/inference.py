from pathlib import Path
from typing import Any

import joblib
import pandas as pd


class MinimumInferenceService:
    """Servicio para cargar un modelo guardado y ejecutar inferencias sobre datos de entrada."""

    def __init__(self, model_path: Path = Path("models/classifier.joblib")):
        self.model_path = model_path
        self._model: Any = None

    def load_model(self) -> None:
        """Carga el clasificador serializado (.joblib)."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en la ruta: {self.model_path}"
            )
        self._model = joblib.load(self.model_path)

    def predict(
        self, amount: float, transaction_count: int, account_age_days: int
    ) -> int:
        """Realiza la inferencia utilizando un DataFrame de Pandas de una sola fila."""
        if self._model is None:
            self.load_model()

        if self._model is None:
            raise RuntimeError("Error al cargar el modelo de inferencia.")

        input_df = pd.DataFrame(
            [
                {
                    "amount": amount,
                    "transaction_count": transaction_count,
                    "account_age_days": account_age_days,
                }
            ]
        )
        prediction = self._model.predict(input_df)[0]
        return int(prediction)
