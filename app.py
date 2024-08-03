import streamlit as st
import pandas as pd
import requests
import json
from streamlit_chat import message


API_KEY = "3324eee6d97745e8b66adbdd96ada61f"
url = f"https://newsapi.org/v2/everything?q=cybersecurity&from=2024-14-6&tags=hack&sortBy=publishedAt&apiKey={API_KEY}"
response = requests.get(url)
news_content = response.content

news = json.loads(news_content)
df = pd.DataFrame(news['articles'])

# Borrando columnas que no estamos usando
df.drop(columns=['urlToImage', 'url'], inplace=True)

# Convertir columnas de tipo object a string
df['description'] = df['description'].astype(str)
df['content'] = df['content'].astype(str)

prueba = pd.DataFrame({
    'fechas': pd.to_datetime(df['publishedAt'], errors='coerce'),
})

st.title('App de prueba')

st.write("""
         #App de prueba
         """)

st.line_chart(prueba)

message('Mi mensaje')
message('Hola',is_user=True)





