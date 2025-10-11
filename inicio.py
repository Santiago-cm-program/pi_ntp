import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Datos con Python en Streamlit",
    page_icon="🌾",
    layout="wide"
)

# Estilo CSS para imagen de fondo y tamaños de fuente aumentados
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .main-header {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            font-size: 2.5em; /* Tamaño aumentado para el título */
        }
        .main-header h1 {
            font-size: 1.5em; /* Ajuste relativo si es necesario */
        }
        .main-body {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            text-align: justify;
            font-size: 1 em; /* Tamaño aumentado para el cuerpo */
        }
        .item-description {
            margin-top: 10px;
            font-style: italic;
            color: #555;
            font-size: 1 em; /* Tamaño aumentado para descripciones */
        }
        .main-body p, .main-body ul {
            font-size: 1.3em;
        }
        .main-body li {
            font-size: 1.3em;
            margin-bottom: 15px;
        }
        .main-body strong {
            font-size: 1.4em;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-header"><h1>Bienvenido al análisis de datos con Python en el entorno de Streamlit</h1></div>', unsafe_allow_html=True)

# Contenido del cuerpo
st.markdown("""
    <div class="main-body">
        <p>En este proyecto encontrarás lo siguiente:</p>
        <ul>
            <li><strong>Análisis de datos del proyecto de campo digital</strong><div class="item-description">Podremos analizar los datos de los productos del proyecto integrador de campo digital. En esto tendremos los siguientes manejos: informe de inventario, informe de ventas, ciudades que se distribuyen y cantidad de clientes por ciudad.</div></li>
            <li><strong>Análisis de datos de productos agrícolas en el municipio de Caldas en el año 2024</strong><div class="item-description">Exploraremos los datos de producción y comercialización de productos agrícolas en el municipio de Caldas durante el 2024, incluyendo tendencias de volúmenes, precios y factores influyentes en el sector.</div></li>
            <li><strong>Chat interactivo de inteligencia artificial enfocado en la consulta de información de productos agropecuarios</strong><div class="item-description">Interactúa con un chatbot impulsado por IA para obtener información detallada y respuestas rápidas sobre diversos productos agropecuarios, desde cultivos y manejo hasta mercados y recomendaciones.</div></li>
        </ul>
    </div>
""", unsafe_allow_html=True)
