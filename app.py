import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config(
    page_title="Acidentes de Trânsito no Brasil",
    page_icon="",
    layout="wide"
)



@st.cache_data
def carregar_dados():
    df = pd.read_csv(
        "dados/simulacao_acidentes_transito_brasil_tema27.csv"
    )

    df["data"] = pd.to_datetime(df["data"])

    return df

df = carregar_dados()



st.title("Análise de Acidentes de Trânsito no Brasil")

st.markdown("""
Este dashboard apresenta uma análise exploratória dos acidentes de trânsito registrados no Brasil.

O objetivo é identificar padrões, regiões mais afetadas, fatores relacionados à gravidade dos acidentes e indicadores relevantes para apoio à tomada de decisão.
""")



st.sidebar.header("Filtros")

anos = sorted(df["ano"].unique())

ano = st.sidebar.multiselect(
    "Ano",
    anos,
    default=anos
)

regioes = st.sidebar.multiselect(
    "Região",
    sorted(df["regiao"].unique()),
    default=sorted(df["regiao"].unique())
)

ufs = st.sidebar.multiselect(
    "UF",
    sorted(df["uf"].unique()),
    default=sorted(df["uf"].unique())
)

tipos = st.sidebar.multiselect(
    "Tipo de Acidente",
    sorted(df["tipo_acidente"].unique()),
    default=sorted(df["tipo_acidente"].unique())
)



df_filtrado = df[
    (df["ano"].isin(ano))
    &
    (df["regiao"].isin(regioes))
    &
    (df["uf"].isin(ufs))
    &
    (df["tipo_acidente"].isin(tipos))
]



st.header("📊 Indicadores Principais")

total_acidentes = int(df_filtrado["acidentes"].sum())
total_feridos = int(df_filtrado["feridos"].sum())
total_mortes = int(df_filtrado["mortes"].sum())

media_veiculos = round(
    df_filtrado["veiculos_envolvidos"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Acidentes",
    f"{total_acidentes:,}"
)

col2.metric(
    "Feridos",
    f"{total_feridos:,}"
)

col3.metric(
    "Mortes",
    f"{total_mortes:,}"
)

col4.metric(
    "Média Veículos",
    media_veiculos
)



st.header("Dados Filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)



st.header("Acidentes por Região")

fig, ax = plt.subplots(figsize=(8, 4))

dados_regiao = (
    df_filtrado
    .groupby("regiao")["acidentes"]
    .sum()
    .sort_values(ascending=False)
)

sns.barplot(
    x=dados_regiao.index,
    y=dados_regiao.values,
    ax=ax
)

ax.set_xlabel("Região")
ax.set_ylabel("Acidentes")

st.pyplot(fig)


st.header("Evolução Temporal dos Acidentes")

fig, ax = plt.subplots(figsize=(8, 4))

dados_ano = (
    df_filtrado
    .groupby("ano")["acidentes"]
    .sum()
)

sns.lineplot(
    x=dados_ano.index,
    y=dados_ano.values,
    marker="o",
    ax=ax
)

ax.set_xlabel("Ano")
ax.set_ylabel("Acidentes")

st.pyplot(fig)

st.header("Mortes por Tipo de Acidente")

fig, ax = plt.subplots(figsize=(10, 6))

dados_tipo = (
    df_filtrado
    .groupby("tipo_acidente")["mortes"]
    .sum()
    .sort_values(ascending=False)
)

sns.barplot(
    x=dados_tipo.values,
    y=dados_tipo.index,
    ax=ax
)

ax.set_xlabel("Quantidade de Mortes")
ax.set_ylabel("Tipo de Acidente")

st.pyplot(fig)



st.header("Acidentes por Período do Dia")

fig, ax = plt.subplots(figsize=(8, 4))

sns.countplot(
    data=df_filtrado,
    x="periodo_dia",
    ax=ax
)

ax.set_xlabel("Período do Dia")
ax.set_ylabel("Quantidade")

st.pyplot(fig)



st.header("🚦 Distribuição da Gravidade")

fig, ax = plt.subplots(figsize=(8, 4))

sns.countplot(
    data=df_filtrado,
    x="nivel_gravidade",
    ax=ax
)

ax.set_xlabel("Nível de Gravidade")
ax.set_ylabel("Quantidade")

st.pyplot(fig)



st.header("Correlação Estatística")

colunas = [
    "acidentes",
    "feridos",
    "mortes",
    "chuva_mm",
    "veiculos_envolvidos"
]

corr = df_filtrado[colunas].corr()

fig, ax = plt.subplots(figsize=(8, 5))

sns.heatmap(
    corr,
    annot=True,
    cmap="Blues",
    ax=ax
)

st.pyplot(fig)



st.header("Interpretação dos Resultados")

st.markdown(f"""
### Principais Indicadores

- Total de acidentes analisados: **{total_acidentes:,}**
- Total de feridos: **{total_feridos:,}**
- Total de mortes: **{total_mortes:,}**
- Média de veículos envolvidos: **{media_veiculos}**

A análise demonstra padrões distintos entre regiões e tipos de acidente.

Os gráficos permitem observar a evolução temporal dos acidentes, os períodos do dia com maior incidência e os níveis de gravidade mais frequentes.

O mapa de correlação auxilia na identificação de relações entre acidentes, vítimas, chuva e quantidade de veículos envolvidos.
""")


st.header("Conclusão")

st.success("""
Os dados analisados demonstram que os acidentes de trânsito apresentam comportamentos distintos conforme região, período do dia e tipo de ocorrência.

A utilização de análise exploratória, indicadores de desempenho (KPIs) e visualizações interativas possibilita compreender melhor os fatores associados aos acidentes e apoiar ações voltadas à segurança viária.
""")