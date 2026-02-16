from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/model",
    tags=["Modelagem de Dados"]
)


