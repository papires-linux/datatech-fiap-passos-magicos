from fastapi import APIRouter, status
from pydantic import BaseModel
from src.api_ingestao import ingestao

router = APIRouter(
    prefix="/ingestao",
    tags=["Ingestão de Dados"]
)


# Modelo padrão de resposta
class IngestaoResponse(BaseModel):
    etapa: str
    status: str
    detalhe: str | None = None


# ---------------- RAW ---------------- #
@router.post(
    "/raw",
    summary="Executa ingestão RAW",
    description="Executa a etapa de extração e grava os dados na camada RAW.",
    response_model=IngestaoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro durante a execução da etapa RAW"}
    }
)
def ingestao_raw():
    try:
        ingestao.executar_raw()

        return IngestaoResponse(
            etapa="RAW",
            status="SUCESSO"
        )

    except Exception as e:
        return IngestaoResponse(
            etapa="RAW",
            status="ERRO",
            detalhe=str(e)
        )


# ---------------- TRUSTED ---------------- #
@router.post(
    "/trusted",
    summary="Executa ingestão TRUSTED",
    description="Executa transformação e tratamento dos dados na camada TRUSTED.",
    response_model=IngestaoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro durante a execução da etapa TRUSTED"}
    }
)
def ingestao_trusted():
    try:
        ingestao.executar_trusted()

        return IngestaoResponse(
            etapa="TRUSTED",
            status="SUCESSO"
        )

    except Exception as e:
        return IngestaoResponse(
            etapa="TRUSTED",
            status="ERRO",
            detalhe=str(e)
        )


# ---------------- REFINED ---------------- #
@router.post(
    "/refined",
    summary="Executa ingestão REFINED",
    description="Executa agregações e modelagem final na camada REFINED.",
    response_model=IngestaoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro durante a execução da etapa REFINED"}
    }
)

def ingestao_refined():
    try:
        ingestao.executar_refined()

        return IngestaoResponse(
            etapa="REFINED",
            status="SUCESSO"
        )

    except Exception as e:
        return IngestaoResponse(
            etapa="REFINED",
            status="ERRO",
            detalhe=str(e)
        )
