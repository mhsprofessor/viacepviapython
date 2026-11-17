import csv
import os
from datetime import datetime


PASTA_DATA = "data"
ARQUIVO_HISTORICO = "historico.csv"

CAMPOS = [
    "data_hora",
    "cep",
    "logradouro",
    "complemento",
    "bairro",
    "localidade",
    "uf",
    "ibge",
    "ddd",
    "origem",
]


def garantir_pasta():
    if not os.path.exists(PASTA_DATA):
        os.makedirs(PASTA_DATA)


def caminho_historico():
    garantir_pasta()
    return os.path.join(PASTA_DATA, ARQUIVO_HISTORICO)


def registrar_consulta(dados, origem="cep"):
    """Acrescenta uma consulta bem-sucedida ao historico.csv (base historica)."""
    caminho = caminho_historico()
    arquivo_novo = not os.path.exists(caminho)

    linha = {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cep": dados.get("cep", ""),
        "logradouro": dados.get("logradouro", ""),
        "complemento": dados.get("complemento", ""),
        "bairro": dados.get("bairro", ""),
        "localidade": dados.get("localidade", ""),
        "uf": dados.get("uf", ""),
        "ibge": dados.get("ibge", ""),
        "ddd": dados.get("ddd", ""),
        "origem": origem,
    }

    with open(caminho, "a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        if arquivo_novo:
            escritor.writeheader()
        escritor.writerow(linha)

    return caminho


def historico_existe():
    return os.path.exists(caminho_historico())
