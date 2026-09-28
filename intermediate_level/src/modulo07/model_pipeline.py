from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.modulo07.data_processing import load_and_clean_data


def train_and_save_classifier(
    data_path: Path = Path("data/dataset.csv"),
    model_path: Path = Path("models/classifier.joblib"),
) -> float:
    """Carga datos limpios, entrena un clasificador y lo guarda con joblib."""
    x_data, y_data = load_and_clean_data(data_path)

    # Dividir en entrenamiento (80%) y prueba (20%)
    x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data, test_size=0.2, random_state=42
    )

    # Entrenar clasificador
    classifier = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=1)
    classifier.fit(x_train, y_train)

    # Evaluar desempeño
    y_pred = classifier.predict(x_test)
    accuracy = float(accuracy_score(y_test, y_pred))

    # Guardar modelo entrenado con joblib
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(classifier, model_path)

    return accuracy


if __name__ == "__main__":
    acc = train_and_save_classifier()
    print(f"Clasificador entrenado y guardado. Precisión: {acc:.4f}")
