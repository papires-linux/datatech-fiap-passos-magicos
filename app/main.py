from fastapi import FastAPI

from app.routers.model_router    import router as model_router
from app.routers.ingestao_router import router as ingestao_router
# from logging_config import setup_logger
import logging

# logger = setup_logger()

VERSION_API = "2.0.0"

app = FastAPI(
    title="API para ingestão e modelo",
    description="Esta é uma API para captura dados do portal Passos Mágicos e executa os modelos de previsão.",
    version=VERSION_API,
    docs_url="/docs", 
    redoc_url="/redoc"
)

@app.get("/health")
def get_version():
    # logger.info("get_version")
    return {
        "VERSAO" : VERSION_API,
        "STATUS" : "OK"
    }


# Incluindo as rotas dos módulos
app.include_router(ingestao_router)
app.include_router(model_router)
