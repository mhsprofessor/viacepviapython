import os

import matplotlib

matplotlib.use("Agg")  # backend sem interface grafica, so gera arquivos PNG

import matplotlib.pyplot as plt
import pandas as pd

from services.historico import caminho_historico, historico_existe


PASTA_GRAFICOS = os.path.join("data", "graficos")
TOP_N = 15


def carregar_historico():
    """Le o historico.csv e retorna um DataFrame. Retorna None se nao houver dados."""
    if not historico_existe():
        return None
    return pd.read_csv(caminho_historico(), encoding="utf-8")


def _contagens(df, coluna):
    return df[coluna].replace("", pd.NA).dropna().value_counts().head(TOP_N)


def _salvar_grafico_barras(df, coluna, titulo, caminho):
    contagens = _contagens(df, coluna)

    if contagens.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    contagens.sort_values().plot(kind="barh", ax=ax, color="#4C72B0")
    ax.set_title(titulo, fontsize=14)
    ax.set_xlabel("Quantidade de consultas")
    ax.set_ylabel(coluna.capitalize())
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho


def gerar_graficos():
    """Gera graficos de barras (PNG) em data/graficos/. Retorna lista de arquivos criados."""
    df = carregar_historico()
    if df is None or df.empty:
        return []

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)

    graficos = [
        ("uf", "Consultas por UF", "consultas_por_uf.png"),
        ("localidade", "Top cidades consultadas", "consultas_por_cidade.png"),
        ("bairro", "Top bairros consultados", "consultas_por_bairro.png"),
        ("ddd", "Consultas por DDD", "consultas_por_ddd.png"),
    ]

    criados = []
    for coluna, titulo, nome in graficos:
        caminho = os.path.join(PASTA_GRAFICOS, nome)
        if _salvar_grafico_barras(df, coluna, titulo, caminho):
            criados.append(caminho)

    return criados


def resumo_historico():
    """Resumo textual do historico para exibicao no terminal."""
    df = carregar_historico()
    if df is None or df.empty:
        return "Nenhuma consulta registrada ainda."

    total = len(df)
    ufs = df["uf"].replace("", pd.NA).dropna().nunique()
    cidades = df["localidade"].replace("", pd.NA).dropna().nunique()
    top_uf = df["uf"].replace("", pd.NA).dropna().value_counts().head(1)
    top_cidade = df["localidade"].replace("", pd.NA).dropna().value_counts().head(1)

    linhas = [
        f"Total de consultas: {total}",
        f"UFs distintas: {ufs} | Cidades distintas: {cidades}",
        f"Primeira consulta: {df['data_hora'].iloc[0]} | Ultima: {df['data_hora'].iloc[-1]}",
    ]
    if not top_uf.empty:
        linhas.append(f"UF mais consultada: {top_uf.index[0]} ({top_uf.iloc[0]}x)")
    if not top_cidade.empty:
        linhas.append(f"Cidade mais consultada: {top_cidade.index[0]} ({top_cidade.iloc[0]}x)")
    return "\n".join(linhas)
