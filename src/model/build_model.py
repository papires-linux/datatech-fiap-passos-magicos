import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.ensemble import RandomForestClassifier


# ==============================
# CONFIGURAÇÕES
# ==============================

BD_MODELO = os.getenv(
    "BD_MODELO",
    "parquet/refined/refined.parquet"
)

PATH_MODEL = os.getenv(
    "PATH_MODEL",
    "app/model/modelo_defasagem.joblib"
)

RANDOM_STATE = 42
TEST_SIZE = 0.2
THRESHOLD = 0.35


# ==============================
# CARREGAMENTO DOS DADOS
# ==============================

def carregar_dados(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    # Garantir que os valores estão no range esperado
    valores_validos = set(range(-4, 5))
    valores_encontrados = set(df["defasagem"].unique())

    if not valores_encontrados.issubset(valores_validos):
        raise ValueError(
            f"Valores inesperados encontrados em 'defasagem': {valores_encontrados - valores_validos}"
        )

    # Criar target binário: atraso = 0
    # df["defasagem_binaria"] = (df["defasagem"] > 0).astype(int)
    df["risco_defasagem"] = (df["defasagem"] <= 0).astype(int)
    
    return df

# ==============================
# PREPARAÇÃO DOS DADOS
# ==============================

def preparar_dados(df: pd.DataFrame):
    # X = df.drop(columns=["defasagem", "defasagem_binaria"])
    # y = df["defasagem_binaria"]
    X = df.drop(columns=["defasagem", "risco_defasagem"])
    y = df["risco_defasagem"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    return X, y, X_train, X_test, y_train, y_test


# ==============================
# TREINAMENTO
# ==============================

def treinar_modelo(X_train, y_train):

    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=RANDOM_STATE
    )
    
    model.fit(X_train, y_train)

    return model


# ==============================
# AVALIAÇÃO
# ==============================

def avaliar_modelo(model, X_test, y_test, X_full, y_full):

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= THRESHOLD).astype(int)

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    auc = roc_auc_score(y_test, y_proba)
    print("AUC:", auc)

    print("\n=== Cross Validation (ROC AUC) ===")
    scores = cross_val_score(
        model,
        X_full,
        y_full,
        cv=5,
        scoring="roc_auc"
    )

    print("AUC médio:", scores.mean())
    print("Desvio padrão:", scores.std())

    return auc


# ==============================
# SALVAR MODELO
# ==============================

def salvar_modelo(model, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Modelo salvo com sucesso em: {path}")



def avaliar_modelo_teste( coluna_target: str):
    caminho_modelo = PATH_MODEL
    caminho_csv = os.getenv("CAMINHO_CSV_TESTE", "tests/testes.csv")

    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        confusion_matrix,
        classification_report
    )
    """
    Avalia um modelo salvo em .joblib utilizando um CSV de teste.
    
    :param caminho_modelo: caminho do arquivo .joblib
    :param caminho_csv: caminho do CSV com dados de teste
    :param coluna_target: nome da coluna target no CSV
    :return: dicionário com métricas
    """
    
    # Carregar modelo
    print(f"Carregando modelo do caminho: {caminho_modelo}")
    model = joblib.load(caminho_modelo)
    
    # Carregar dados
    df = pd.read_csv(caminho_csv)
    print(f"Dados de teste carregados do caminho: {caminho_csv}")
    print(f"Número de linhas: {len(df)}")

    # Separar X e y
    df[coluna_target] = (df[coluna_target] <= 0).astype(int)
    X_test = df.drop(coluna_target, axis=1)
    y_test = df[coluna_target]

    print("\nDistribuição da variável alvo:")
    # print(df["defasagem_binaria"].value_counts(normalize=True))

    # Fazer previsões
    # y_pred = model.predict(X_test)

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
        y_pred = (y_proba >= THRESHOLD).astype(int)
        roc_auc = roc_auc_score(y_test, y_proba)
    else:
        y_pred = model.predict(X_test)
        roc_auc = None    
    
    print(f"Número de previsões: {len(y_pred)}")
    # Se o modelo tiver predict_proba
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_proba)
    else:
        y_proba = None
        roc_auc = None
    
    print(f"Previsões feitas. Avaliando métricas...")
    # Calcular métricas
    resultados = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc,
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }
    
    print("\n📊 RESULTADOS:")
    for k, v in resultados.items():
        print(f"{k}: {v}")
    
    print("\n📄 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return resultados

# ==============================
# MAIN
# ==============================

def main():
    print("Carregando dados...")
    df = carregar_dados(BD_MODELO)

    print("Preparando dados...")
    X, y, X_train, X_test, y_train, y_test = preparar_dados(df)

    print("Treinando modelo...")
    model = treinar_modelo(X_train, y_train)

    print("Avaliando modelo...")
    avaliar_modelo(model, X_test, y_test, X, y)

    print("Salvando modelo...")
    salvar_modelo(model, PATH_MODEL)

    print("Pipeline finalizado com sucesso 🚀")


if __name__ == "__main__":
    main()