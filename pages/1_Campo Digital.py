import streamlit as st
import pandas as pd
import requests as rq
from requests.auth import HTTPBasicAuth
import altair as alt

# ==========================================================
# 🔐 CONFIGURACIÓN DESDE SECRETS
# ==========================================================
api_base_render = st.secrets["api"]["API_CAMPODIGITAL_RENDER"]
api_base_swagger = st.secrets["api"]["API_CAMPODIGITAL_SWAGGER"]
api_user = st.secrets["api"]["user"]
api_pass = st.secrets["api"]["pass"]

# ==========================================================
# 🌐 ENDPOINTS PRINCIPALES
# ==========================================================
api_url_sales_render = f"{api_base_render}/api/v1/sales/GET/all"
api_url_sales_swagger = f"{api_base_swagger}/api/v1/sales/GET/all"

api_url_salesdetails_render = f"{api_base_render}/api/v1/salesdetails/all"
api_url_salesdetails_swagger = f"{api_base_swagger}/api/v1/salesdetails/all"

api_url_products_render = f"{api_base_render}/api/v1/products/GET/active"
api_url_products_swagger = f"{api_base_swagger}/api/v1/products/GET/active"

api_url_users_render = f"{api_base_render}/v1/api/Users/GET"
api_url_users_swagger = f"{api_base_swagger}/v1/api/Users/GET"

# ==========================================================
# 🧠 FUNCIÓN PARA OBTENER DATOS DE API CON BASIC AUTH
# ==========================================================


def obtener_datos_api(url):
    try:
        response = rq.get(url, auth=HTTPBasicAuth(
            api_user, api_pass), timeout=1000)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"⚠️ Error {response.status_code} al consultar: {url}")
            return None
    except Exception as e:
        st.warning(f"⚠️ Error de conexión en {url}: {e}")
        return None


# ==========================================================
# 🏷️ TÍTULO PRINCIPAL
# ==========================================================
st.title("📊 Panel de Consumo de API (Ventas, Detalles, Productos y Usuarios)")

# ==========================================================
# 1️⃣ CONSULTAR DATOS DE SALES
# ==========================================================
data_sales = obtener_datos_api(api_url_sales_render)
if not data_sales:
    st.info("Intentando obtener ventas desde el segundo endpoint (Swagger)...")
    data_sales = obtener_datos_api(api_url_sales_swagger)

# ==========================================================
# 2️⃣ CONSULTAR DATOS DE SALES DETAILS
# ==========================================================
data_details = obtener_datos_api(api_url_salesdetails_render)
if not data_details:
    st.info(
        "Intentando obtener detalles de ventas desde el segundo endpoint (Swagger)...")
    data_details = obtener_datos_api(api_url_salesdetails_swagger)

# ==========================================================
# 3️⃣ CONSULTAR PRODUCTOS ACTIVOS
# ==========================================================
data_products = obtener_datos_api(api_url_products_render)
if not data_products:
    st.info(
        "Intentando obtener productos activos desde el segundo endpoint (Swagger)...")
    data_products = obtener_datos_api(api_url_products_swagger)

# ==========================================================
# 4️⃣ CONSULTAR USUARIOS
# ==========================================================
data_users = obtener_datos_api(api_url_users_render)
if not data_users:
    st.info("Intentando obtener usuarios desde el segundo endpoint (Swagger)...")
    data_users = obtener_datos_api(api_url_users_swagger)

# ==========================================================
# 5️⃣ MOSTRAR TABLAS
# ==========================================================
if data_sales:
    st.subheader("🧾 Ventas (Sales)")
    df_sales = pd.DataFrame(data_sales if isinstance(
        data_sales, list) else data_sales.get("result", []))

    # Mostrar solo columnas relevantes
    columnas = ["idVenta", "usuario", "fecha", "total"]
    df_sales = df_sales[[col for col in columnas if col in df_sales.columns]]

    st.dataframe(df_sales, use_container_width=True)
else:
    st.error("❌ No se pudieron obtener los datos de ventas.")

if data_details:
    st.subheader("📦 Detalles de Venta (SalesDetails)")
    df_details = pd.DataFrame(data_details if isinstance(
        data_details, list) else data_details.get("result", []))
    st.dataframe(df_details, use_container_width=True)
else:
    st.error("❌ No se pudieron obtener los detalles de venta.")

if data_products:
    st.subheader("🟩 Productos Activos")
    df_products = pd.DataFrame(data_products if isinstance(
        data_products, list) else data_products.get("result", []))
    st.dataframe(df_products, use_container_width=True)
else:
    st.error("❌ No se pudieron obtener los productos activos.")

if data_users:
    st.subheader("👤 Usuarios")
    df_users = pd.DataFrame(data_users if isinstance(
        data_users, list) else data_users.get("result", []))
    st.dataframe(df_users, use_container_width=True)
else:
    st.error("❌ No se pudieron obtener los usuarios.")

# ==========================================================
# 6️⃣ GRÁFICOS DE ANÁLISIS
# ==========================================================
if not data_sales or df_sales.empty:
    st.stop()

# Gráfico de ventas por usuario
st.subheader("🏆 Total de Ventas por Usuario")
df_group = df_sales.groupby("usuario")["total"].sum().reset_index()
df_group = df_group.sort_values(by="total", ascending=False)
st.bar_chart(df_group.set_index("usuario"))

# Gráfico de distribución de productos
if data_details:
    st.subheader("🥧 Distribución de Cantidades por Producto")
    df_prod = df_details.groupby("product")["cantidad"].sum().reset_index()
    df_prod = df_prod.sort_values(by="cantidad", ascending=False)

    chart = (
        alt.Chart(df_prod)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(field="cantidad", type="quantitative"),
            color=alt.Color(field="product", type="nominal",
                            legend=alt.Legend(title="Producto")),
            tooltip=[
                alt.Tooltip("product", title="Producto"),
                alt.Tooltip("cantidad", title="Total Cantidad", format=","),
            ],
        )
        .properties(width=500, height=400)
    )
    st.altair_chart(chart, use_container_width=True)

# ==========================================================
# 📈 GRÁFICO INTERACTIVO: TOTAL DE VENTAS POR MES (con slider)
# ==========================================================
if data_sales and not df_sales.empty and "fecha" in df_sales.columns:
    st.subheader("📆 Ventas Totales por Mes (con Filtro de Fechas)")

    # Convertir columna de fecha a datetime
    df_sales["fecha"] = pd.to_datetime(df_sales["fecha"], errors="coerce")

    # Agrupar por mes y sumar totales
    df_ventas_mes = (
        df_sales.groupby(df_sales["fecha"].dt.to_period("M"))["total"]
        .sum()
        .reset_index()
    )
    df_ventas_mes["fecha"] = df_ventas_mes["fecha"].dt.to_timestamp()

    # Crear rango de fechas dinámico para el slider
    fecha_min = df_ventas_mes["fecha"].min()
    fecha_max = df_ventas_mes["fecha"].max()

    if pd.isna(fecha_min) or pd.isna(fecha_max):
        st.warning("⚠️ No hay datos válidos de fechas para graficar.")
    else:
        # Slider para seleccionar el rango de fechas
        rango_fechas = st.slider(
            "Selecciona el rango de fechas:",
            min_value=fecha_min.to_pydatetime(),
            max_value=fecha_max.to_pydatetime(),
            value=(fecha_min.to_pydatetime(), fecha_max.to_pydatetime()),
            format="YYYY-MM",
        )

        # Filtrar por rango seleccionado
        fecha_inicio, fecha_fin = rango_fechas
        df_filtrado = df_ventas_mes[
            (df_ventas_mes["fecha"] >= fecha_inicio)
            & (df_ventas_mes["fecha"] <= fecha_fin)
        ]

        # Mostrar resumen
        st.markdown(
            f"📅 Mostrando ventas desde **{fecha_inicio.strftime('%Y-%m')}** hasta **{fecha_fin.strftime('%Y-%m')}**"
        )

        # Gráfico de línea
        st.line_chart(
            data=df_filtrado.set_index("fecha")["total"],
            use_container_width=True,
            height=400,
        )

        # Mostrar total acumulado del rango
        total_periodo = df_filtrado["total"].sum()
        st.metric("💰 Total de ventas en el rango seleccionado",
                  f"${total_periodo:,.0f}")
