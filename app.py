import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Generación de datos de ejemplo
dates = pd.date_range(start="2023-01-01", periods=100)
data = np.random.randn(100).cumsum()
df = pd.DataFrame({"Fecha": dates, "Valores": data})

# Dividir la página en dos columnas
col1, col2 = st.columns(2)

# Primera columna: Gráfico de línea de tiempo
with col1:
    st.header("Gráfico de Línea de Tiempo")
    fig = px.line(df, x="Fecha", y="Valores", title="Valores en el Tiempo")
    st.plotly_chart(fig)

# Segunda columna: Selector de datos y botón de calcular
with col2:
    st.header("Selector de Datos y Cálculo")
    
    # Selector de datos
    options = st.multiselect(
        "Selecciona una o más fechas por favor", 
        df["Fecha"].dt.strftime('%Y-%m-%d').tolist()
    )
    
    # Botón de calcular
    if st.button("Calcular"):
        if options:
            selected_dates = pd.to_datetime(options)
            selected_values = df[df["Fecha"].isin(selected_dates)]["Valores"]
            suma = selected_values.sum()
            st.write(f"La suma de los valores seleccionados es: {suma}")
        else:
            st.write("Por favor, selecciona al menos una fecha.")


