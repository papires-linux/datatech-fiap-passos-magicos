# 🎓 Datathon FIAP – Passos Mágicos
## 📊 API de Ingestão e Predição de Defasagem Escolar

Este projeto implementa:

- 🟤 Pipeline de ingestão de dados (RAW → TRUSTED → REFINED)
- 🧠 Modelo de Machine Learning para prever risco de defasagem escolar
- 🌐 API REST para servir previsões
- 🐳 Containerização com Docker

---

# 🎯 Objetivo do Projeto

Desenvolver uma solução capaz de:

1. Processar dados educacionais em múltiplas camadas.
2. Treinar um modelo de Machine Learning.
3. Disponibilizar previsões via API REST.
4. Permitir execução via container Docker.

---

# 🧠 Modelo de Machine Learning

## 📌 Problema

Previsão binária de risco de defasagem escolar:

- `0` → Sem risco
- `1` → Em risco

## 📊 Variáveis Utilizadas

- Indicadores educacionais: `inde`, `ian`, `ieg`, `ida`, `ips`, `ipv`
- Notas: `matematica`, `portugues`
- Dados demográficos: `idade`, `ano_ingresso`
- Gênero (one-hot)
- Classificação pedagógica (`pedra_*`)

## 🤖 Algoritmo

Gradient Boosting Classifier

## 📈 Métricas Obtidas

- Accuracy: 85%
- Recall (classe risco): 84%
- Precision: 91%
- AUC: 0.91

O modelo apresenta alta capacidade de identificar alunos em risco.

---

# 🏗️ Arquitetura
- RAW → Ingestão inicial
- TRUSTED → Dados tratados
- REFINED → Dados prontos para modelagem
- MODEL → Treinamento e serialização (.joblib)
- API → Endpoint /predict

---

# 🐳 Executando com Docker

## 🔹 Pré-requisitos

Docker instalado:

```bash
docker --version
````

🔹 Build da Imagem
```bash 
docker build -t api-datathon:v1.0.0 .
```

🔹 Executar o Container
```bash 
docker run -p 8008:8000 -d api-datathon:v1.0.0
```

🔹 Verificar se o Container Subiu
```bash 
docker ps | grep -i api-datathon
```

Ou acessar:
```bash 
http://localhost:8008/health
```

📦 Ingestão Manual de Dados
```bash
🟤 RAW
curl --location --request POST 'http://127.0.0.1:8008/ingestao/raw' --data ''
```

🟡 TRUSTED
```bash
curl --location --request POST 'http://127.0.0.1:8008/ingestao/trusted' --data ''
```

🟢 REFINED
```bash
curl --location --request POST 'http://127.0.0.1:8008/ingestao/refined' --data ''
```

# 🔮 Endpoint de Predição
📌 POST /predict

Recebe dados do aluno e retorna probabilidade de risco.

Exemplo de Request:
```json
{
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
}
```

Exemplo de Response:
```json
{
  "probabilidade_risco": 0.8721,
  "classificacao": "Risco"
}
```

🔍 Endpoints Disponíveis
```table
Endpoint	Método	Descrição
/health	GET	Verifica se a API está ativa
/ingestao/raw	POST	Executa ingestão camada RAW
/ingestao/trusted	POST	Processa camada TRUSTED
/ingestao/refined	POST	Processa camada REFINED
/predict	POST	Retorna previsão do modelo
```

🛑 Parar o Container
```bash 
docker stop <container_id>
docker rm <container_id>
```
# 📦 Estrutura do Projeto
```css
app/
│
├── main.py
├── model/
│   └── modelo_defasagem.joblib
│
├── ingestao/
├── pipeline/
└── requirements.txt
```

# 👨‍💻 Desenvolvido para

Datathon FIAP – Passos Mágicos

