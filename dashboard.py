"""Dashboard interativo do historico de consultas ViaCEP.

Executar com:  streamlit run dashboard.py
"""

import json
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.historico import caminho_historico, historico_existe
from services.visualizacao import carregar_historico


PASTA_DATA = "data"
ARQUIVO_GEOJSON = os.path.join("assets", "brazil-states.geojson")

st.set_page_config(page_title="Dashboard ViaCEP", page_icon="📍", layout="wide")
st.title("📍 Dashboard de Consultas ViaCEP")
st.caption("Visualizacao do historico salvo em `data/historico.csv`")


def carregar_geojson():
    if not os.path.exists(ARQUIVO_GEOJSON):
        return None
    with open(ARQUIVO_GEOJSON, "r", encoding="utf-8") as f:
        return json.load(f)


df = carregar_historico()

if df is None or df.empty:
    st.warning(
        "Nenhuma consulta registrada ainda. "
        "Execute `python main.py`, faca algumas consultas e volte aqui."
    )
    st.stop()

# ---- Filtros laterais ----
st.sidebar.header("Filtros")
ufs = sorted(df["uf"].replace("", pd.NA).dropna().unique())
uf_sel = st.sidebar.multiselect("UF", ufs, default=ufs)

cidades = sorted(
    df.loc[df["uf"].isin(uf_sel), "localidade"]
    .replace("", pd.NA)
    .dropna()
    .unique()
) if uf_sel else []
cidade_sel = st.sidebar.multiselect("Cidade", cidades, default=cidades)

df_filtro = df[df["uf"].isin(uf_sel) & df["localidade"].isin(cidade_sel)]
if df_filtro.empty:
    st.info("Nenhum dado para os filtros selecionados.")
    st.stop()

# ---- Metricas ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de consultas", len(df_filtro))
col2.metric("UFs distintas", df_filtro["uf"].nunique())
col3.metric("Cidades distintas", df_filtro["localidade"].nunique())
col4.metric("Bairros distintos", df_filtro["bairro"].replace("", pd.NA).dropna().nunique())

st.divider()

# ---- Graficos de barras ----
st.subheader("Consultas por UF")
contagem_uf = df_filtro["uf"].value_counts().sort_index()
st.bar_chart(contagem_uf, height=300)

col_map, col_cidade = st.columns(2)

with col_map:
    st.subheader("Mapa de distribuicao por UF")
    geojson = carregar_geojson()
    if geojson:
        mapa_df = (
            df_filtro["uf"].value_counts().rename_axis("uf").reset_index(name="consultas")
        )
        fig = go.Figure(
            go.Choropleth(
                geojson=geojson,
                locations=mapa_df["uf"],
                z=mapa_df["consultas"],
                featureidkey="properties.sigla",
                colorscale="Blues",
                colorbar_title="Consultas",
                hovertemplate="%{location}<br>Consultas: %{z}<extra></extra>",
            )
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, width="stretch")
    else:
        st.info(f"GeoJSON nao encontrado em `{ARQUIVO_GEOJSON}`.")

with col_cidade:
    st.subheader("Top cidades")
    top_cidades = df_filtro["localidade"].value_counts().head(15).sort_values()
    st.bar_chart(top_cidades, height=420)

# ---- Tabela de dados ----
st.divider()
st.subheader("Ultimas consultas")
st.dataframe(
    df_filtro[["data_hora", "cep", "logradouro", "bairro", "localidade", "uf", "ddd"]],
    width="stretch",
    hide_index=True,
)
