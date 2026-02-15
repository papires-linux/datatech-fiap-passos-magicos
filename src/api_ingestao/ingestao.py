import ssl
import re
import os
import certifi
import pandas as pd
import unicodedata
from src.api_ingestao.metadados import variables
from datetime import date

today = date.today().isoformat()

directory_path_raw = f"{variables.PATH_RAW}/{today}"
directory_path_trusted = f"{variables.PATH_TRUSTED}/"
directory_path_refined = f"{variables.PATH_REFINED}/"

SHEET_ID        = variables.SHEET_ID
MAPA_COLUNAS    = variables.MAPA_COLUNAS_RAW
ABAS_GS         = variables.ABAS_GS

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    cols = []
    for c in df.columns:
        c = c.strip().lower()                   # deixar letras minusculas
        c = unicodedata.normalize("NFKD", c)    # remove acentos
        c = c.encode("ascii", "ignore").decode("utf-8")  # remove caracteres especiais
        c = re.sub(r"[ /]", "_", c)             # substitui separadores
        c = re.sub(r"[^a-z0-9_]", "", c)        # remove caracteres estranhos        
        c = re.sub(r"_+", "_", c)               # remove _ duplicado
        #c = re.sub(r"_\d+$", "", c)             # remove sufixo .1, .2 do pandas
        cols.append(c)
    df.columns = cols
    return df

#-- Ingestão de dados raw
def ingestao_dados_raw(SHEET_ID,ABAS_GS,MAPA_COLUNAS,directory_path_raw):
    for aba in ABAS_GS:
        aba_gid = aba.get("gid")
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={aba_gid}"
        df = pd.read_csv(url)

        df = normalizar_colunas(df)
        os.makedirs(directory_path_raw, exist_ok=True)
        df.to_parquet(f"{directory_path_raw}/sheet_{aba_gid}.parquet")
        # print(df.columns)

#-- Ingestão de dados trusted
def ajuste_idade(df: pd.DataFrame) -> pd.DataFrame:
    # garantir que data_nascimento seja datetime
    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])

    # calcular idade
    df['idade'] = df['ano_ingresso'] - df['data_nascimento'].dt.year
    return df

def converter_para_float(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """
    Converte uma coluna string para float64 de forma segura.
    Trata vírgula decimal, espaços e valores inválidos.
    """
    # remove espaços
    df[coluna] = df[coluna].astype(str).str.strip()
    
    # troca vírgula por ponto
    df[coluna] = df[coluna].str.replace(",", ".", regex=False)
    
    # converte para float (valores inválidos viram NaN)
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    print(f"Valores após conversão da coluna '{coluna}': {df[coluna].value_counts(dropna=False)}")
    
    return df

def tratamento_coluna_genero(df: pd.DataFrame) -> pd.DataFrame:
    df['genero'] = df['genero'].str.lower().str.strip()

    print(df['genero'].value_counts())


    df['genero'] = df['genero'].replace({
        'menino': 'masculino',
        'menina': 'feminino'
    })
    df = pd.get_dummies(df, columns=['genero'])

    return df

def tratamento_coluna_pedra(df: pd.DataFrame) -> pd.DataFrame:    
    # Padronização
    df['pedra'] = df['pedra'].str.lower().str.strip()

    # Remover valores inválidos
    df = df[~df['pedra'].isin(['#div/0!', 'incluir'])]

    # Padronizar acentos (caso existam variações)
    df['pedra'] = df['pedra'].replace({
        'ágata': 'agata',
        'topázio': 'topazio',
        'quartzo': 'quartzo',
        'ametista': 'ametista',
    })

    print(df['pedra'].value_counts())

    # One-hot encoding
    df = pd.get_dummies(df, columns=['pedra'])

    return df

def adicionar_idade(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Converter tudo para string
    df['data_nascimento'] = df['data_nascimento'].astype(str).str.strip()
    
    # Função para tratar cada valor
    def parse_data(valor):
        
        # Se for só ano (ex: "2020")
        if valor.isdigit() and len(valor) == 4:
            return pd.to_datetime(valor, format="%Y", errors="coerce")
        
        # Tentar converter assumindo formato americano
        return pd.to_datetime(valor, errors="coerce")
    
    df['data_nascimento'] = df['data_nascimento'].apply(parse_data)
    
    return df

def ingestao_dados_trusted(ABAS_GS,directory_path_raw,directory_path_trusted):
    for aba in ABAS_GS:
        COLUNAS_TRUSTED = aba.get("colunas_trusted")
        aba_gid = aba.get("gid")
        ano_ingresso = aba.get("ano")
        print(f"Iniciando ingestão trusted da aba {aba_gid}...")
        
        df = pd.read_parquet(f"{directory_path_raw}/sheet_{aba_gid}.parquet")
        # print(f"Colunas antes de selecionar: {df.columns.tolist()}")
        df = df[COLUNAS_TRUSTED]
        df['ano_ingresso'] = ano_ingresso
        # print(f"Colunas antes de renomear: {df.columns.tolist()}")
        df_selecionado = df.rename(columns=lambda c: MAPA_COLUNAS.get(c, c))
       

        df_selecionado = df_selecionado.astype(
            variables.COLUNAS_TRUSTED_TYPE
        )
        print(f"Tipos de dados após ajuste: {df_selecionado.dtypes}")

        df_selecionado = converter_para_float(df_selecionado, "inde")
        df_selecionado = converter_para_float(df_selecionado, "iaa")
        df_selecionado = converter_para_float(df_selecionado, "ieg")
        df_selecionado = converter_para_float(df_selecionado, "ips")
        df_selecionado = converter_para_float(df_selecionado, "ida")
        df_selecionado = converter_para_float(df_selecionado, "matematica")
        df_selecionado = converter_para_float(df_selecionado, "portugues")
        df_selecionado = converter_para_float(df_selecionado, "ipv")
        df_selecionado = converter_para_float(df_selecionado, "ian")

        df_selecionado = tratamento_coluna_genero(df_selecionado)
        df_selecionado = tratamento_coluna_pedra(df_selecionado)
        df_selecionado = adicionar_idade(df_selecionado)

        df_selecionado = ajuste_idade(df_selecionado)

        os.makedirs(directory_path_trusted, exist_ok=True)
        df_selecionado.to_parquet(f"{directory_path_trusted}/sheet_{aba_gid}.parquet")
        print(f"Ingestão trusted da aba {aba_gid} concluída.")

#-- Ingestão de dados refined
def limpeza_refined(df: pd.DataFrame) -> pd.DataFrame:
    colunas = [
        'inde', 'iaa', 'ieg', 'ips', 'ida', 'matematica', 'portugues', 'ipv'
    ]
    df = df.dropna(subset=colunas)

    return df

def ingestao_dados_refined(ABAS_GS,directory_path_trusted,directory_path_refined):
    arquivos = []
    for aba in ABAS_GS:
        aba_gid = aba.get("gid")
        df = pd.read_parquet(f"{directory_path_trusted}/sheet_{aba_gid}.parquet")
        arquivos.append(f"{directory_path_trusted}/sheet_{aba_gid}.parquet")

    df_union = pd.concat(
        [pd.read_parquet(arq) for arq in arquivos],
        ignore_index=True
    )

    df_union = df_union.drop(columns=['data_nascimento'])
    df_union = limpeza_refined(df_union)

    print(f"Colunas após limpeza: {df_union.columns.tolist()}")
    print(f"Valores nulos por coluna:\n{df_union.isnull().sum()}")

    os.makedirs(directory_path_refined, exist_ok=True)
    df_union.to_parquet(f"{directory_path_refined}/refined.parquet")

def executar_raw():
    ingestao_dados_raw(SHEET_ID,ABAS_GS,MAPA_COLUNAS,directory_path_raw)
    print("Ingestão raw concluída.")
    
def executar_trusted():
    ingestao_dados_trusted(ABAS_GS,directory_path_raw,directory_path_trusted)
    print("Ingestão trusted concluída.")

def executar_refined():
    ingestao_dados_refined(ABAS_GS,directory_path_trusted,directory_path_refined)
    print("Ingestão refined concluída.")

def main():
    print("Iniciando processo de ingestão de dados...")
    executar_raw()
    executar_trusted()
    executar_refined()

if __name__ == "__main__":
    main()