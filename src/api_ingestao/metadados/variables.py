SHEET_ID = "1td91KoeSgXrUrCVOUkLmONG9Go3LVcXpcNEw_XrL2R0"

PATH_RAW = f"parquet/raw"
PATH_TRUSTED = f"parquet/trusted"
PATH_REFINED = f"parquet/refined"

COLUNAS_TRUSTED_TYPE = {
    'data_nascimento'   : 'string',
    'genero'            : 'string',
    'pedra'             : 'string',
    'inde'              : 'string',
    'iaa'               : 'string',
    'ieg'               : 'string',
    'ips'               : 'string',
    'ida'               : 'string',
    'matematica'        : 'string',
    'portugues'         : 'string',
    'ipv'               : 'string',
    'ian'               : 'string',
    'defasagem'         : 'int64'
}

ABAS_GS = [
    {
        "ano" : 2022,
        "gid" : 90992733,
        "colunas_trusted" : [
            # 'idade_22',
            'ano_nasc',
            'genero',
            'pedra_22',
            'inde_22',
            'iaa',
            'ieg',
            'ips',
            'ida',
            'matem',
            'portug',
            'ipv',
            'ian',
            'defas'
        ]
    },{
        "ano" : 2023,
        "gid" : 555005642,
        "colunas_trusted" : [
            # 'idade',
            'data_de_nasc',
            'genero',
            'pedra_2023',
            'inde_2023',
            'iaa',
            'ieg',
            'ips',
            'ida',
            'mat',
            'por',
            'ipv',
            'ian',
            'defasagem'
        ]
    },{
        "ano" : 2024,
        "gid" : 215885893,
        "colunas_trusted" : [
            # 'idade',
            'data_de_nasc',
            'genero',
            'pedra_2024',
            'inde_2024',
            'iaa',
            'ieg',
            'ips',
            'ida',
            'mat',
            'por',
            'ipv',
            'ian',
            'defasagem'
        ]
    }
]

MAPA_COLUNAS_RAW = {
    "nome_anonimizado": "nome",
    "fase": "fase",
    "ano_nasc": "data_nascimento",
    "data_de_nasc": "data_nascimento",
    "inde_22": "inde",
    "inde_2023": "inde",
    "inde_2024": "inde",
    "idade_22": "idade",
    "pedra_22": "pedra",
    "pedra_2023": "pedra",
    "pedra_2024": "pedra",
    "mat": "matematica",
    "matem": "matematica",
    "por": "portugues",
    "portug": "portugues",
    "ing": "ingles",
    "ingles": "ingles",
    "defas": "defasagem",
    "instituicao_de_ensino": "instituicao_ensino",
    "ativo_inativo": "status_ativo",
}



