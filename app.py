import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Dicionário de nomes dos meses em português com acentos
nomes_meses_pt = {
    1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
    5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
    9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
}

# Configuração inicial do app
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Carregar imagem do logo
image = Image.open('logo-semas.jpg')

# Título com logo
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=20)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Planilha: Tribunal de Recursos Administrativo</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# Carregar dados
df = pd.read_excel("PROCESSOS_TRA_LIMPA.xlsx")

# Criar coluna formatada com nome de mês em português
df["dia"] = df["data_plenaria"].dt.day
df["mes"] = df["data_plenaria"].dt.month
df["ano"] = df["data_plenaria"].dt.year
df["data_plenaria_formatada"] = df["dia"].astype(str) + " " + df["mes"].map(nomes_meses_pt) + " " + df["ano"].astype(str)

# ======================= GRÁFICOS =======================

col4, col5 = st.columns([0.50, 0.50])

# 1. Total de Processos por Data da Plenária
with col4:
    result_data = df.groupby("data_plenaria_formatada").size().reset_index(name="Total de Processos")
    fig = px.bar(result_data, x="data_plenaria_formatada", y="Total de Processos",
                 title="Total de Processos por Data da Plenária", template="gridon", height=500)
    fig.update_xaxes(title="Data da Plenária")
    st.plotly_chart(fig, use_container_width=True)

# 2. Valor Arrecadado por Plenária
with col5:
    result_valores = df.groupby("data_plenaria_formatada")["valor_da_multa"].sum().reset_index()
    fig1 = px.line(result_valores, x="data_plenaria_formatada", y="valor_da_multa",
                   title="Valor Arrecadado por Data da Plenária (R$)", template="gridon")
    fig1.update_xaxes(title="Data da Plenária")
    st.plotly_chart(fig1, use_container_width=True)

# Visualizar dados
st.divider()
col_v1, col_d1 = st.columns([0.5, 0.5])
with col_v1:
    expander = st.expander("Dados de Processos por Data")
    expander.write(result_data)
with col_d1:
    st.download_button("Baixar Dados", data=result_data.to_csv().encode("utf-8"),
                       file_name="Processos_por_Data.csv", mime="text/csv")

# 3. Total de Processos por Situação
st.divider()
situacao_data = df["situacao"].value_counts().reset_index()
situacao_data.columns = ["Situação", "Total de Processos"]
fig2 = px.pie(situacao_data, names="Situação", values="Total de Processos",
              title="Distribuição de Processos por Situação")
st.plotly_chart(fig2, use_container_width=True)

# 4. Treemap por Situação e Atividade
st.divider()
treemap_data = df.groupby(["situacao", "atividade1"]).size().reset_index(name="Total de Processos")
fig3 = px.treemap(treemap_data, path=["situacao", "atividade1"], values="Total de Processos",
                  title="Treemap: Processos por Situação e Atividade")
fig3.update_traces(textinfo="label+value")
st.plotly_chart(fig3, use_container_width=True)

# Raw data
st.divider()
expander = st.expander("Ver Dados Brutos")
expander.write(df)
st.download_button("Baixar Dados Brutos", data=df.to_csv(index=False).encode("utf-8"),
                   file_name="Dados_Completos_Tribunal.csv", mime="text/csv")
