import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache
def load_data():
    # Carregar os dados
    data = pd.read_csv('Vendas.xlsx - Plan1.csv')
    
    # Converter a coluna Data
    data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')
    
    # Remover caracteres especiais e converter 'Valor Final' para numérico
    data['Valor Final'] = data['Valor Final'].replace('[^\d.]', '', regex=True).astype(float)
    
    return data



df = load_data()

# Título do Dashboard
st.title("Dashboard de Vendas")

# Filtro por loja
lojas = df['ID Loja'].unique()
filtro_loja = st.sidebar.multiselect("Selecione a(s) Loja(s):", lojas, default=lojas)

# Filtro por data
data_min = df['Data'].min()
data_max = df['Data'].max()
filtro_data = st.sidebar.date_input("Selecione o intervalo de datas:", [data_min, data_max])

# Aplicar filtros
df_filtrado = df[
    (df['ID Loja'].isin(filtro_loja)) & 
    (df['Data'].between(pd.to_datetime(filtro_data[0]), pd.to_datetime(filtro_data[1])))
]


# Gráficos
st.header("Resumo de Vendas")

# Gráfico de vendas por produto
vendas_produto = df_filtrado.groupby('Produto')['Valor Final'].sum().reset_index()
fig_produto = px.bar(vendas_produto, x='Produto', y='Valor Final', title="Vendas por Produto")
st.plotly_chart(fig_produto)

# Gráfico de vendas ao longo do tempo
vendas_tempo = df_filtrado.groupby('Data')['Valor Final'].sum().reset_index()
fig_tempo = px.line(vendas_tempo, x='Data', y='Valor Final', title="Vendas ao longo do Tempo")
st.plotly_chart(fig_tempo)

# Tabela com os dados filtrados
st.header("Tabela de Dados Filtrados")
st.dataframe(df_filtrado)

# Resumo numérico
st.header("Indicadores")
st.metric("Total de Vendas", f"R$ {df_filtrado['Valor Final'].sum():,.2f}")
st.metric("Quantidade de Vendas", len(df_filtrado))
