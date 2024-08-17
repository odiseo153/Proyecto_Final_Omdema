import subprocess
import sys
import os

def install_requirements():
    if os.path.exists('requirements.txt'):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        st.error("El archivo requirements.txt no se encontró. Por favor, asegúrate de que el archivo exista en el directorio.")

# Intentar instalar las dependencias desde el archivo requirements.txt
try:
    install_requirements()
except Exception as e:
    st.error(f"Hubo un error al intentar instalar las dependencias: {e}")

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from wordcloud import WordCloud
from collections import Counter
import re
from nltk.corpus import stopwords
import nltk
import json
from dotenv import load_dotenv

st.set_page_config(page_title="Analisis Exploratorio", page_icon=":chart_with_upwards_trend:")

# Cargar variables de entorno
load_dotenv()

# Descargar recursos necesarios de NLTK
nltk.download('stopwords')

# Clave API de NewsAPI
API_KEY = os.getenv('NEWSAPI_ORG_KEY')

# Si no hay clave API en el archivo .env, pide al usuario que la ingrese
if API_KEY is None:
    st.warning("La clave API para NewsAPI no está disponible en el archivo .env. Por favor, ingrésala aquí:")
    API_KEY = st.text_input("Clave API de NewsAPI", type="password")
    if not API_KEY:
        st.stop()  # Detiene la ejecución si la clave API no se proporciona

# Configuración de la página de Streamlit

# Título de la aplicación
st.title("Sistema de Análisis de Noticias sobre Seguridad Informática")

# Descripción del objetivo general
st.markdown("""
## Objetivo general
Indagar sobre las noticias relacionadas a la seguridad informática con el fin de conocer los ataques cibernéticos más comunes que vulneran la seguridad de las empresas para el departamento de ciberseguridad de Sanitas.
""")

st.markdown("""
## Personas que hicieron el análisis
<div style="display: flex; align-items: center;">
    <img src="https://lh3.googleusercontent.com/a/ACg8ocJTVy3LIralUTzBtJlaan8YGTSewOkU2hQtH9xKVKMOCpwbncuF=s360-c-no" width="50" height="50" style="border-radius: 50%; margin-right: 10px;" />
    <a href="https://www.linkedin.com/in/odiseo-esmerlin-rincon-sanchez-48053524b/">Odiseo Esmerlin Rincon Sanchez</a>
</div>
<hr>
<div style="display: flex; align-items: center;">
    <img src="https://lh3.googleusercontent.com/a-/ALV-UjXSQdSNNXsVofGZipHKdm-3BuLMqxBIdp32n3gRuBfFGJD_y4Rt=s72-p-k-rw-no" width="50" height="50" style="border-radius: 50%; margin-right: 10px;" />
    <a href="https://www.linkedin.com/in/emerson-echavarr%C3%ADa-gonz%C3%A1lez-80974a265/">Emerson Echavarría González</a>
</div>
<hr>
<div style="display: flex; align-items: center;">
    <img src="https://lh3.googleusercontent.com/a-/ALV-UjUCIvir-2ORPV6WAxR9UvPtPQBpdILdefvaifhNm70cCDKuExSX=s72-p-k-rw-no" width="50" height="50" style="border-radius: 50%; margin-right: 10px;" />
    <span>Isabel Cardona</span>
</div>
<hr>
""", unsafe_allow_html=True)


# Mostrar spinner mientras se traen los datos
with st.spinner('Cargando datos...'):
    # Petición de datos
    url = f"https://newsapi.org/v2/everything?q=cybersecurity&from=2024-14-6&tags=hack&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    news_content = response.content


    # Cargar los datos en un DataFrame
    news = json.loads(news_content)
    print(news)
    news_df = pd.DataFrame(news['articles'])

# Transformación de datos
news_df['description'] = news_df['description'].astype(str)
news_df['content'] = news_df['content'].astype(str)
news_df['publishedAt'] = pd.to_datetime(news_df['publishedAt'], errors='coerce')
news_df['source'] = news_df['source'].apply(lambda x: x['name'] if isinstance(x, dict) and 'name' in x else None)

# Mostrar información general del DataFrame
st.write("### Información general del DataFrame")
st.write(news_df.head())

# Graficar autores más frecuentes
st.write("### Autores más frecuentes")
author_counts = news_df['author'].value_counts()
top_10_author = author_counts.head(10).index
news_df_top_10_author = news_df[news_df['author'].isin(top_10_author)]

plt.figure(figsize=(10, 6))
sns.countplot(data=news_df_top_10_author, x='author', order=top_10_author)
plt.xticks(rotation=80)
st.pyplot(plt.gcf())

# Graficar fuentes más frecuentes
st.write("### Fuentes más frecuentes")
source_counts = news_df['source'].value_counts()
top_10_source = source_counts.head(10).index
news_df_top_10_source = news_df[news_df['source'].isin(top_10_source)]

plt.figure(figsize=(10, 6))
sns.countplot(data=news_df_top_10_source, x='source', order=top_10_source)
plt.xticks(rotation=90)
st.pyplot(plt.gcf())

# Frecuencia de noticias por fecha
st.write("### Frecuencia de Noticias por Fecha")
date_counts = news_df['publishedAt'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
sns.lineplot(x=date_counts.index, y=date_counts.values)
plt.title('Frecuencia de Noticias por Fecha', fontsize=16)
plt.xlabel('Fecha', fontsize=14)
plt.ylabel('Número de Noticias', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt.gcf())

# Nube de palabras para el contenido
st.write("### Nube de Palabras del Contenido")
content = ' '.join(news_df['content'])
content = re.sub(r'[^\w\s]', '', content.lower())
words = [word for word in content.split() if word not in stopwords.words('english')]
wordcloud = WordCloud(width=800, height=400, max_words=100).generate(' '.join(words))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt.gcf())

st.write("### Cantidad de veces que las primeras 10 palabras aparecen")

# Unir todas las descripciones de noticias en una sola cadena de texto
text = ' '.join(news_df['description'])

# Eliminar signos de puntuación y convertir el texto a minúsculas
text = re.sub(r'[^\w\s]', '', text.lower())

# Dividir el texto en palabras individuales
words = text.split()

# Obtener la lista de palabras vacías (stop words) en inglés
stop_words = set(stopwords.words('english'))

# Filtrar las palabras eliminando las stop words
filtered_words = [word for word in words if word not in stop_words]

# Contar la frecuencia de cada palabra
word_counts = Counter(filtered_words)

# Obtener las 10 palabras más comunes
most_common_words = word_counts.most_common(10)

# Crear un DataFrame para las palabras más comunes
common_words_df = pd.DataFrame(most_common_words, columns=['Palabra', 'Frecuencia'])

# Graficar las palabras más comunes y sus frecuencias
plt.figure(figsize=(10, 6))
sns.barplot(x='Frecuencia', y='Palabra', data=common_words_df, palette='viridis')
plt.title('Top 10 palabras más comunes en las descripciones')
plt.xlabel('Frecuencia')
plt.ylabel('Palabra')
st.pyplot(plt.gcf())

# Nube de palabras para las descripciones
st.write("### Nube de Palabras de las Descripciones")
description = ' '.join(news_df['description'])
description = re.sub(r'[^\w\s]', '', description.lower())
words = [word for word in description.split() if word not in stopwords.words('english')]
wordcloud = WordCloud(width=800, height=400, max_words=100).generate(' '.join(words))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt.gcf())

st.write("""
### Mensaje de Despedida

Queremos expresar nuestro más sincero agradecimiento por tomarte el tiempo de revisar nuestro trabajo. Hemos dedicado muchas horas y esfuerzo para llevar a cabo este análisis de manera minuciosa y detallada. El interés y atención significan mucho para nosotros.

Esperamos que la información presentada le haya sido útil y te haya brindado una visión clara sobre las noticias relacionadas con la seguridad informática. Si tienes alguna pregunta, comentario o sugerencia, no dudes en ponerte en contacto con nosotros.

Nos encantaría tener la oportunidad de colaborar contigo nuevamente en el futuro. Seguiremos trabajando con la misma dedicación y compromiso para seguir ofreciendo análisis y soluciones que añadan valor.

¡Gracias nuevamente por tu tiempo y confianza!

Atentamente,  
El equipo 3
""")
