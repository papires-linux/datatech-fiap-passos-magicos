from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    response = client.post("/predict", json={
        "inde": 6.5,
        "iaa": 7.0,
        "ieg": 6.8,
        "ips": 6.2,
        "ida": 6.9,
        "matematica": 7.5,
        "portugues": 6.8,
        "ipv": 6.0,
        "ian": 6.4,
        "ano_ingresso": 2022,
        "genero_feminino": 1,
        "genero_masculino": 0,
        "pedra_agata": 1,
        "pedra_ametista": 0,
        "pedra_quartzo": 0,
        "pedra_topazio": 0,
        "idade": 13
    })

    assert response.status_code == 200
    assert "probabilidade_risco" in response.json()
