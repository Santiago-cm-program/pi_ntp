import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Configuración de la app
st.set_page_config(
    page_title="Información de Productos Agropecuarios con IA", layout="wide")

# Inyectar CSS para el fondo y los contenedores de respuesta
background_css = """
<style>
.stApp {
    background-image: url("https://images.pexels.com/photos/440731/pexels-photo-440731.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.stApp::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3); /* Semi-transparent overlay for better readability */
    z-index: -1;
}
/* Estilo para los contenedores de respuesta */
div[data-testid="stMarkdownContainer"] {
    background-color: white;
    color: black;
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
/* Estilo para los subheaders */
h3 {
    color: black !important;
    background-color: white;
    padding: 10px;
    border-radius: 5px;
    display: inline-block;
}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

st.title("🌾 Información de Productos Agropecuarios con IA")
st.markdown(
    "Expande una categoría para seleccionar un ítem predefinido y obtener información detallada generada por Gemini.")

# Cargar variables de entorno
# load_dotenv()
api_key = st.secrets["key_value_api"]  # Cambia al nombre real de tu variable

if not api_key:
    st.error("❌ No se encontró la variable KEY_VALUE_API en el archivo .env")
    st.stop()

# Configurar Gemini
genai.configure(api_key=api_key)

# Función para generar respuesta


def generar_respuesta(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    if not prompt:
        return "Por favor, selecciona un ítem."
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Ítems predefinidos por categoría
categorias_items = {
    "Herramientas": ["Pala", "Azada", "Rastrillo", "Hoz", "Pico", "Machete", "Tijeras de podar", "Escardilla"],
    "Semillas": ["Maíz", "Frijol", "Arroz", "Trigo", "Soya", "Tomate"],
    "Abonos": ["Compost", "Estiércol", "Urea", "Sulfato de amonio", "NPK Complejo", "Guano"]
}

# Crear columnas para los tres expanders
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("🛠️ Herramientas", expanded=False):
        selected_item = st.selectbox(
            "Selecciona una herramienta:", categorias_items["Herramientas"], key="herramienta")
        if selected_item:
            prompt = f"Proporciona información detallada sobre la {selected_item} en agricultura: cómo se usa en el campo, precauciones, mantenimiento y otros tips relevantes."
            if st.button("Generar Información", key="btn_herramientas"):
                with st.spinner("Generando información..."):
                    respuesta = generar_respuesta(prompt)
                    st.subheader(f"Información sobre {selected_item}:")
                    st.markdown(respuesta)

with col2:
    with st.expander("🌱 Semillas", expanded=False):
        selected_item = st.selectbox(
            "Selecciona una semilla:", categorias_items["Semillas"], key="semilla")
        if selected_item:
            prompt = f"Proporciona información detallada sobre la semilla de {selected_item} en agricultura: variedades comunes, cómo sembrar, cuidados, precauciones y otros tips relevantes."
            if st.button("Generar Información", key="btn_semillas"):
                with st.spinner("Generando información..."):
                    respuesta = generar_respuesta(prompt)
                    st.subheader(
                        f"Información sobre semilla de {selected_item}:")
                    st.markdown(respuesta)

with col3:
    with st.expander("🧪 Abonos", expanded=False):
        selected_item = st.selectbox(
            "Selecciona un abono:", categorias_items["Abonos"], key="abono")
        if selected_item:
            prompt = f"Proporciona información detallada sobre el {selected_item} en agricultura: composición, cómo aplicar, dosis recomendadas, precauciones y otros tips relevantes."
            if st.button("Generar Información", key="btn_abonos"):
                with st.spinner("Generando información..."):
                    respuesta = generar_respuesta(prompt)
                    st.subheader(f"Información sobre {selected_item}:")
                    st.markdown(respuesta)
