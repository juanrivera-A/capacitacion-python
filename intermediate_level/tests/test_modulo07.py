from pathlib import Path

import pandas as pd

from src.modulo07.data_processing import load_and_clean_data
from src.modulo07.inference import MinimumInferenceService
from src.modulo07.model_pipeline import train_and_save_classifier


def test_load_and_clean_data(tmp_path: Path):
    csv_path = tmp_path / "test_dataset.csv"
    x_features, y_target = load_and_clean_data(csv_path)

    assert isinstance(x_features, pd.DataFrame)
    assert isinstance(y_target, pd.Series)
    assert not x_features.isnull().values.any()
    assert len(x_features) == len(y_target)


def test_train_save_and_inference(tmp_path: Path):
    csv_path = tmp_path / "data.csv"
    model_path = tmp_path / "model.joblib"

    # 1. Entrenar y guardar con joblib
    acc = train_and_save_classifier(data_path=csv_path, model_path=model_path)
    assert acc >= 0.70
    assert model_path.exists()

    # 2. Probar inferencia mínima
    service = MinimumInferenceService(model_path=model_path)
    prediction = service.predict(
        amount=2500.0, transaction_count=30, account_age_days=180
    )
    assert prediction in (0, 1)
