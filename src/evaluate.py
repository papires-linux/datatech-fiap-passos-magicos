import joblib
import pandas as pd
import json
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# ==============================
# CONFIGURAÇÕES
# ==============================

MODEL_PATH = "../app/model/modelo_defasagem.joblib"
TEST_DATA_PATH = "../tests/testes.csv"
TARGET_COLUMN = "target"  # altere se necessário


def load_model(path):
    """
    Carrega modelo salvo via joblib
    """
    artefato = joblib.load(path)

    # Caso tenha salvo apenas o modelo
    if isinstance(artefato, dict):
        model = artefato["model"]
        threshold = artefato.get("threshold", 0.5)
    else:
        model = artefato
        threshold = 0.5

    return model, threshold


def evaluate():
    print("🔎 Carregando modelo...")
    model, threshold = load_model(MODEL_PATH)

    print("📊 Carregando dados de teste...")
    df = pd.read_csv(TEST_DATA_PATH)

    X_test = df.drop(columns=[TARGET_COLUMN])
    y_test = df[TARGET_COLUMN]

    print("📈 Gerando probabilidades...")
    y_proba = model.predict_proba(X_test)[:, 1]

    print(f"⚙ Aplicando threshold: {threshold}")
    y_pred = (y_proba >= threshold).astype(int)

    # ==============================
    # MÉTRICAS
    # ==============================

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    conf_matrix = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print("\n===== RESULTADOS =====")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")
    print(f"ROC AUC  : {roc_auc:.4f}")

    print("\n===== MATRIZ DE CONFUSÃO =====")
    print(conf_matrix)

    print("\n===== CLASSIFICATION REPORT =====")
    print(report)

    # ==============================
    # SALVAR MÉTRICAS EM JSON
    # ==============================

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": conf_matrix.tolist()
    }

    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print("\n✅ Métricas salvas em metrics.json")


if __name__ == "__main__":
    evaluate()
