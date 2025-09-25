import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Configuración de la app
st.set_page_config(page_title="Chat Básico con Gemini", layout="centered")
st.title("💬 Chat con Gemini")
st.markdown("Ingresa un tema o pregunta para obtener una respuesta generada por Gemini.")

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("KeyValueApi")

if not api_key:
    st.error("❌ No se encontró la variable KeyValueApi en el archivo .env")
else:
    genai.configure(api_key=api_key)

# Interfaz de usuario
prompt = st.text_input("Escribe tu pregunta o tema:", placeholder="Ej. Explica cómo funciona la IA en pocas palabras")
enviar = st.button("Generar Respuesta")

# Función corregida
def generar_respuesta(prompt):
    if not prompt:
        return "Por favor, ingresa un tema o pregunta."
    try:
        # Crear el modelo directamente
        model = genai.GenerativeModel("gemini-1.5-flash")  # 👈 usa la versión más estable
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Lógica principal
if enviar and prompt:
    with st.spinner("Generando respuesta..."):
        respuesta = generar_respuesta(prompt)
        st.subheader("Respuesta:")
        st.markdown(respuesta)
else:
    st.info("Escribe un tema o pregunta y haz clic en Generar Respuesta.")
