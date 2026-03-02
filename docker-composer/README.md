# Datathon – Pipeline CI/CD com Apache Airflow

Este projeto configura um ambiente Apache Airflow utilizando Docker Compose para orquestração de um pipeline de ingestão, processamento e deploy de modelo preditivo.
📁 Estrutura do Projeto
```bash 
docker-composer/
│
├── docker-compose.yaml      # Orquestração dos containers
├── .env                     # Variáveis de ambiente
├── dags/                    # DAGs do Airflow
│   └── dag_cicd_deploy_modelo.py
├── config/
│   └── airflow.cfg          # Configuração do Airflow
├── logs/                    # Logs das execuções
└── plugins/                 # Plugins customizados (se houver)

```
### 🧰 Pré-requisitos
Antes de iniciar, você precisa ter instalado:

- ✅ Docker
- ✅ Docker Compose (v2+ recomendado)
- ✅ Permissão sudo (Linux/Mac)

Verifique:
```bash
docker --version
docker compose version
```

### ⚙️ Configuração Inicial
#### 1️⃣ Acessar a pasta do projeto
```bash
cd docker-composer
```

#### 2️⃣ Ajustar permissões (Linux/Mac)
Necessário para evitar erros de permissão nos volumes do Airflow:
```bash 
sudo chmod -R 777 ./config
sudo chmod -R 777 ./logs
sudo chmod -R 777 ./dags
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

#### 3️⃣ Fazer deploy da api modelo
Execute esse comando na raiz do projeto que você fez o download do git:
```bash 
docker build -t api-datathon:v2.0.0 . 
```

Validar se o nome e a versão da imagem estão certo no `docker-compose.yaml`
```
  api-datathon:
    image: api-datathon:v2.0.0
    container_name: api-datathon
```

#### 4️⃣ Inicializar o banco do Airflow
Esse comando cria as tabelas internas:
```bash 
docker compose up airflow-init
```

#### ▶️ Subindo o Ambiente
Após a inicialização:
```bash 
docker compose up -d
```

Para verificar os containers:
```bash 
docker ps
````

### 🌐 Acessando o Airflow
Após subir os containers, acesse:
```browser
http://localhost:8080/
```

🔐 Credenciais padrão:
Usuário: airflow
Senha: airflow

#### 📊 DAG Principal
A DAG principal está em:

```bash
dags/dag_cicd_deploy_modelo.py
```

Ela executa:
- Ingestão RAW
- Ingestão TRUSTED
- Ingestão REFINED
- Deploy do Modelo
- Avaliação/Teeste do Modelo

### 🧪 Comandos Úteis
#### Listar configurações do Airflow
```bash
docker compose run airflow-cli airflow config list
```

#### Ver logs do container da API (caso exista)
```bash
docker logs api-datathon -f
```

#### Ver logs do Airflow
```bash
docker compose logs -f
````

#### Reiniciar ambiente
```bash 
docker compose down
docker compose up -d
```

#### Parar o ambiente
```bash
docker compose down
```

#### Remover containers + volumes (reset completo)
⚠️ Isso apaga banco e histórico de execuções
``` bash 
docker compose down --volumes --remove-orphans
```

### 🔁 Executar DAG Manualmente

1. Acesse o Airflow
2. Ative a DAG
3. Clique em Trigger DAG


### 📂 Logs das Execuções
Os logs ficam armazenados em:
```bash
logs/dag_id=dag_cicd_deploy_modelo/
```

### 🛠 Desenvolvimento
Sempre que alterar a DAG:

1. Salve o arquivo em dags/
2. O Airflow detectará automaticamente
3. Caso necessário:
```bash 
docker compose restart
```

### 🔥 Reset Completo do Ambiente
Caso algo quebre:
```bash
docker compose down --volumes --remove-orphans
sudo rm -rf logs/*
sudo rm -rf config/*
docker compose up airflow-init
docker compose up -d
```

### 📌 Observações Importantes
- A pasta logs/ cresce rapidamente.
- Nunca commitar logs no Git.
- Verifique permissões caso ocorram erros de escrita.
- Certifique-se que a porta 8080 não esteja sendo usada.

### 🧠 Arquitetura Simplificada

```mathematica
Docker Compose
    ↓
Postgres (metadata)
    ↓
Airflow Scheduler
    ↓
Airflow Webserver
    ↓
DAG CI/CD
    ↓
Deploy Modelo
```