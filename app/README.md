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

📊 Avaliação do Modelo

O modelo de predição de risco de defasagem apresentou desempenho elevado no conjunto de teste (200 amostras), com as seguintes métricas:
```json
{
    "accuracy": 0.805,
    "precision": 0.7194244604316546,
    "recall": 1.0,
    "f1_score": 0.8368200836820083,
    "roc_auc": 0.9891,
    "confusion_matrix": [
        [
            61,
            39
        ],
        [
            0,
            100
        ]
    ]
}
```

## 📊 Resultados do Modelo – Risco de Defasagem Escolar

O modelo de classificação binária para previsão de risco de defasagem escolar apresentou os seguintes resultados no conjunto de teste:

🔢 Métricas Gerais
Accuracy: 80,5%
Precision: 71,94%
Recall: 100%
F1-Score: 83,68%
ROC AUC: 0,9891

## 📌 Interpretação das Métricas
### ✅ Recall = 100%

O modelo identificou todos os estudantes com risco de defasagem.
Não houve nenhum falso negativo.

Isso é extremamente importante em contexto educacional, pois evita deixar de identificar alunos em risco.

### ⚠️ Precision = 71,94%

Entre os alunos classificados como "em risco", aproximadamente 72% realmente estavam em risco.

Isso indica a presença de falsos positivos, o que significa que alguns alunos foram sinalizados como risco sem realmente estarem em defasagem.

### 🎯 F1-Score = 83,68%

O F1-score mostra um bom equilíbrio entre precisão e recall, com maior peso para a alta sensibilidade do modelo.

### 📈 ROC AUC = 0,9891

Indica excelente capacidade de separação entre as classes.
O modelo distingue muito bem alunos com e sem risco.

### 📊 Matriz de Confusão
	Predito: Sem Risco	Predito: Com Risco
Real: Sem Risco	61	39
Real: Com Risco	0	100
🔎 Análise

100 alunos em risco foram corretamente identificados

0 falsos negativos

39 falsos positivos

61 verdadeiros negativos

🏫 Interpretação de Negócio

O modelo foi ajustado para priorizar sensibilidade (recall máximo), garantindo que nenhum aluno em risco deixe de ser identificado.

Essa abordagem é adequada para políticas educacionais preventivas, onde é preferível:

✔ Identificar todos os alunos em risco
✔ Mesmo que alguns alunos sejam sinalizados preventivamente

### 🚀 Conclusão

O modelo demonstra:

Excelente capacidade discriminativa (AUC ≈ 0,99)

Sensibilidade máxima (Recall = 1.0)

Bom equilíbrio geral (F1 > 0.83)

Ele está adequado para uso como ferramenta de apoio à tomada de decisão em programas de intervenção educacional.

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

🎯 O que isso significa na prática?
Situação	Interpretação
DEFASAGEM = 0	Aluno está no nível adequado
DEFASAGEM > 0	Aluno está atrasado (defasagem positiva)
DEFASAGEM < 0	Aluno pode estar adiantado

Com isso:
DEFASAGEM > 0 → risco de defasagem
DEFASAGEM = 0 → sem risco


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
    "probabilidade_risco": 0.0006,
    "classificacao": "Sem Risco"
}
```
Outro exemplo:
```json
{
  "inde": 8.7,
  "iaa": 9.2,
  "ieg": 9.2,
  "ips": 7.5,
  "ida": 8.5,
  "matematica": 7.5,
  "portugues": 8.0,
  "ipv": 8.1,
  "ian": 10.0,
  "ano_ingresso": 2024,
  "genero_feminino": 1,
  "genero_masculino": 0,
  "pedra_agata": 0,
  "pedra_ametista": 0,
  "pedra_quartzo": 0,
  "pedra_topazio": 1,
  "idade": 12
}
````

Resposta: 
```json
{
    "probabilidade_risco": 0.9445,
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
├── README.md
├── main.py
├── model/
│   └── modelo_defasagem.joblib
├── docs
│   └── figuras
│       ├── doc_api.jpg
│       └── figura_airflow.jpg
└── routers
    ├── ingestao_router.py
    └── model_router.py
```

# 👨‍💻 Desenvolvido para

Datathon FIAP – Passos Mágicos

