from fastapi import APIRouter,status

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

router = APIRouter(
    prefix="/model",
    tags=["Modelagem de Dados"]
)

MODEL_PATH = os.path.join("app", "model", "modelo_defasagem.joblib")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Erro ao carregar modelo: {e}")

# --------------------------------------------------
# Endpoint de predição
# --------------------------------------------------

class AlunoInput(BaseModel):
    inde: float
    iaa: float
    ieg: float
    ips: float
    ida: float
    matematica: float
    portugues: float
    ipv: float
    ian: float
    ano_ingresso: int
    genero_feminino: int
    genero_masculino: int
    pedra_agata: int
    pedra_ametista: int
    pedra_quartzo: int
    pedra_topazio: int
    idade: int

@router.post("/deploy",
    summary="Faz o deploy do modelo e salva o modelo treinado",
    description="Executa o treinamento do modelo e salva o modelo treinado em disco.",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro durante a execução da etapa de treinamento do modelo. Verifica os dados de entrada e o processo de treinamento."}
    }
)
def build():
    # Aqui você pode implementar a lógica para treinar o modelo
    # e salvar o modelo treinado usando joblib.dump()
    from src.model import build_model

    try:
        build_model.main()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao treinar o modelo: {e}")

    return {"message": "Modelo treinado e salvo com sucesso!"}

@router.post("/predict",
    summary="Faz a predição com o modelo treinado",
    description="Executa a predição com o modelo treinado carregado do disco.",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro durante a execução da etapa de predição do modelo. Verifica os dados de entrada e o processo de predição."}
    }
)
def predict(aluno: AlunoInput):
    try:
        dados = np.array([[
            aluno.inde,
            aluno.iaa,
            aluno.ieg,
            aluno.ips,
            aluno.ida,
            aluno.matematica,
            aluno.portugues,
            aluno.ipv,
            aluno.ian,
            aluno.ano_ingresso,
            aluno.genero_feminino,
            aluno.genero_masculino,
            aluno.pedra_agata,
            aluno.pedra_ametista,
            aluno.pedra_quartzo,
            aluno.pedra_topazio,
            aluno.idade
        ]])

        # Probabilidade da classe 1 (risco)
        prob = model.predict_proba(dados)[0][1]

        # Classificação com threshold 0.5
        classificacao = 1 if prob >= 0.5 else 0

        return {
            "probabilidade_risco": float(round(prob, 4)),
            "classificacao": "Risco" if classificacao == 1 else "Sem Risco"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/avaliacao",
    summary="Faz a avaliacao do modelo treinado",
    description="Executa a avaliacao com o modelo treinado carregado do disco.",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro durante a execução da etapa de predição do modelo. Verifica os dados de entrada e o processo de predição."}
    }
)
def avaliacao():
    from src.model.build_model import avaliar_modelo_teste
    try:
        resultados = avaliar_modelo_teste(coluna_target="target")
        return resultados
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



