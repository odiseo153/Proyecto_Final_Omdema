import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

# Presentación
st.title("Odiseo Esmerlin Rincón Sancher")
st.subheader("Desarrollador de Software")
st.write("""
¡Hola! Soy Odiseo Esmerlin Rincón Sancher, un desarrollador apasionado por la creación de soluciones tecnológicas. 
Me especializo en desarrollo web y aplicaciones interactivas, utilizando diversas tecnologías para hacer realidad las ideas.
""")

# Zona de juego: Interacción con gráficos y botones
st.header("Zona de Juego")

# Selección de tipo de gráfico
tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Gráfico de Líneas", "Gráfico de Barras"])

# Parámetros del gráfico
numero_puntos = st.slider("Número de puntos", 10, 100, 30)

# Generación de datos aleatorios
x = np.arange(0, numero_puntos)
y = np.random.randn(numero_puntos).cumsum()

# Creación de gráficos basados en la selección del usuario
if tipo_grafico == "Gráfico de Líneas":
    fig = px.line(x=x, y=y, title="Gráfico de Líneas", labels={'x': 'Índice', 'y': 'Valores Acumulados'})
else:
    fig = px.bar(x=x, y=y, title="Gráfico de Barras", labels={'x': 'Índice', 'y': 'Valores Acumulados'})

# Mostrar el gráfico
st.plotly_chart(fig)

# Botón de reiniciar
if st.button("Reiniciar Datos"):
    st.experimental_rerun()

# Instrucciones para ejecutar la aplicación:
# 1. Guarda este código en un archivo llamado `app.py`.
# 2. Abre una terminal y navega al directorio donde se encuentra `app.py`.
# 3. Ejecuta `streamlit run app.py`.
