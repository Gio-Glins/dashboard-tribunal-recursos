import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Configuração inicial do app
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Carregar imagem do logo
image = Image.open('logo_semas.png')

# Espaço antes da imagem
st.markdown("<div style='padding-top: 30px;'></div>", unsafe_allow_html=True)

# Centralização com colunas
col1, col2, col3 = st.columns([1, 2, 1])
image = Image.open('logo_semas.png')


with col2:
    st.image(image, use_column_width=True)
col11, col12, col13 = st.columns([1, 2, 1])
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Planilha Tribunal de Recursos Administrativos</h1></center>"""
with col12:
    st.markdown(html_title, unsafe_allow_html=True)
    
# Carregar dados
df = pd.read_excel("PROCESSOS_TRA_LIMPA (1).xlsx")
df["valor_da_multa"] = pd.to_numeric(df["valor_da_multa"], errors="coerce")

# Garantir que está em datetime
df["data_plenaria"] = pd.to_datetime(df["data_plenaria"], errors="coerce", dayfirst=True)

# Criar coluna no formato "Month Year"
df["data_plenaria_formatada"] = df["data_plenaria"].dt.strftime("%b %Y")

# Ordenar pelo valor real da data
df = df.sort_values("data_plenaria")

# ======================= GRÁFICOS =======================

col4, col5 = st.columns([0.50, 0.50])

# 1. Total de Processos por Data da Plenária
with col4:
    result_data = df.groupby("data_plenaria_formatada").size().reset_index(name="Total de Processos")
    fig = px.bar(result_data, x="data_plenaria", y="Total de Processos",
                 title="Total de Processos por Data da Plenária", template="gridon", height=500)
    fig.update_xaxes(title="Data da Plenária")
    st.plotly_chart(fig, use_container_width=True)

# 2. Valor Arrecadado por Plenária
with col5:
    result_valores = df.groupby("data_plenaria_formatada")["valor_da_multa"].sum().reset_index()
    fig1 = px.line(result_valores, x="data_plenaria", y="valor_da_multa",
                   title="Valor Arrecadado por Data da Plenária (R$)", template="gridon")
    fig1.update_xaxes(title="Data da Plenária")    
    fig1.update_layout(
    yaxis_tickprefix="R$ ",
    yaxis_tickformat=",.2f")
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
