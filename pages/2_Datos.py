import streamlit as st
import pandas as pd
from src.data_frame import get_users_data


def app_with_filtered_table():
  # Llama a la función para obtener el DataFrame
    df = get_users_data()

   # Verifica si el DataFrame está vacío
    if df.empty:
        st.error("No se pudo cargar la información de los usuarios.")
        return  # Salir de la función si no hay datos

    st.title("Lista de Usuarios y Filtro")

    # Resto de tu código para el filtro y la tabla
    filter_active = st.sidebar.checkbox(
        "Mostrar solo usuarios activos", value=True)

    if filter_active:
        df_filtered = df[df['isActive'] == True].copy()
    else:
        df_filtered = df.copy()

    st.dataframe(df_filtered, use_container_width=True)


# Llama a la función principal para ejecutar la página
app_with_filtered_table()
