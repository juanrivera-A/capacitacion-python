from pathlib import Path

import numpy as np
import pandas as pd


def create_sample_csv(file_path: Path = Path("data/dataset.csv")) -> None:
    """Genera un archivo CSV sintético si no existe."""
    if file_path.exists():
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    num_samples = 500

    amount = np.random.uniform(10.0, 5000.0, size=num_samples)
    transaction_count = np.random.randint(1, 50, size=num_samples)
    account_age_days = np.random.randint(30, 3650, size=num_samples)

    # Introducir algunos valores nulos para ejercitar la limpieza con Pandas
    amount[::20] = np.nan

    risk_score = (
        (np.nan_to_num(amount) / 5000.0) * 0.5
        + (transaction_count / 50.0) * 0.3
        - (account_age_days / 3650.0) * 0.2
    )
    is_high_risk = (risk_score > 0.4).astype(int)

    df = pd.DataFrame(
        {
            "amount": amount,
            "transaction_count": transaction_count,
            "account_age_days": account_age_days,
            "is_high_risk": is_high_risk,
        }
    )
    df.to_csv(file_path, index=False)


def load_and_clean_data(
    file_path: Path = Path("data/dataset.csv"),
) -> tuple[pd.DataFrame, pd.Series]:
    """Carga y limpia un dataset CSV usando Pandas."""
    if not file_path.exists():
        create_sample_csv(file_path)

    # 1. Cargar CSV en Pandas
    df = pd.read_csv(file_path)

    # 2. Limpieza de datos (eliminar filas con valores nulos o rellenar)
    df_clean = df.dropna().copy()

    # 3. Separar características (X) y variable objetivo (y)
    x_features = df_clean[["amount", "transaction_count", "account_age_days"]]
    y_target = df_clean["is_high_risk"]

    return x_features, y_target
