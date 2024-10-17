#importar o que precisamos
import pandas as pd
import sqlite3
from datetime import datetime

caminho_arquivo = 'data1.jsonl'

#definir caminho p arquivo jsonl
#python main.py rodar dentro da pasta transformacao
#ler dados do arquivo

df = pd.read_json(caminho_arquivo, lines = True)
#print(df)

#setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

#adicionar a coluna_source com um valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

#adicionar a coluna data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()

#print(df)

#tratar valores nulos para colunas numericas e de texto
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)


#remover os parenteses das colunas 'review_amount'
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)



#juntar colunas de preço criando uma nova e tratar os preços como float e calcular os valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] /100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] /100



#remover colunas antigas de preços

newdf=df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais','new_price_centavos'])

print(newdf)

#conectar com banco de dados sqllite(ou criar um novo)
conn = sqlite3.connect('quotes1.db')

#salvar dataframe no banco
newdf.to_sql('mercadolivre1', conn, if_exists='replace', index= False)

# fechar a conexao
conn.close()

print(df.head())

