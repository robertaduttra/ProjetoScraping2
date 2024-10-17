#conectar com banco SQLITE
#para rodar streamlit run app.py dentro da pasta dashboard

import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('../transformacao/quotes1.db')

#carregar os dados da tabela ' mercadolivre1 ' em um df pandas

df = pd.read_sql_query("Select * from mercadolivre1", conn)

# fechar conexao com o banco de dados
conn.close()

#titulo da aplicacao
st.title('Pesquisa de Mercado - Tênis Espotivos no Mercado Livre')



#Melhorar o layout com colunas para KPIS principais indicadores
st.subheader('KPIs principais do Sistema')
#st.write(df) #printar no streamlit

col1, col2, col3 = st.columns(3)

#KPI 1: NUMERO TOTAL DE ITENS
#count
total_itens = df.shape[0]
col1.metric(label="Número Total de Itens", value = total_itens)

#KPI 2: NUMERO DE MARCAS UNICAS#como se fosse distinct
uniqued_brands= df['brand'].nunique()
col2.metric(label="Número de Marcos Únicas", value=uniqued_brands)

#KPI 3: PREÇO MEDIO NOVO(EM REAIS)#media mean()
avarege_new_price= df['new_price'].mean()
col3.metric(label="Preço Médio Novo (R$)", value=f"{avarege_new_price:.2f}")


#Quais marcas sao mais encontradas até a 10ª paginas
st.subheader('Quais as marcas mais encontradas até a 10ª página ')
col1, col2 = st.columns([4,2])
top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

#qual o preço medio por marca
st.subheader('Preço médio por marca')
col1, col2 = st.columns([4,2])
df_non_zero_prices = df[df['new_price'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

#satisfacao total por marca
st.subheader('Satisfação por marca')
col1,col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)
#col2.write(satisfaction_by_brand)
