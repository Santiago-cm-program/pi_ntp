import streamlit as st
import pandas as pd
import src.data_frame as df
import altair as alt

# -----------------------
# 🧹 LIMPIEZA DE DATOS
# -----------------------

st.title("📊 Análisis de Datos Agrícolas")

# Cargar DataFrame desde tu módulo
df_filtrado = df.data_frame_filtrado.copy()

# Limpiar columna de producción
if "PRODUCCION(t)" in df_filtrado.columns:
    # Convertir a texto y limpiar caracteres
    df_filtrado["PRODUCCION(t)"] = (
        df_filtrado["PRODUCCION(t)"]
        .astype(str)
        .str.replace(r"[^\d,.\-]", "", regex=True)  # quita texto o símbolos
    )

    # Detectar formato de número (latino vs inglés)
    muestra = df_filtrado["PRODUCCION(t)"].dropna().iloc[0]
    if "," in muestra and "." in muestra and muestra.find(",") > muestra.find("."):
        # Formato latino (1.234,56)
        df_filtrado["PRODUCCION(t)"] = (
            df_filtrado["PRODUCCION(t)"]
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
    else:
        # Formato inglés o mixto (1,234.56 o 1234.56)
        df_filtrado["PRODUCCION(t)"] = df_filtrado["PRODUCCION(t)"].str.replace(
            ",", "", regex=False)

    # Convertir finalmente a float
    df_filtrado["PRODUCCION(t)"] = pd.to_numeric(
        df_filtrado["PRODUCCION(t)"], errors="coerce")

# Mostrar DataFrame limpio
st.dataframe(df_filtrado, use_container_width=True, height=600)

# -----------------------
# 🌾 GRÁFICO AGRÍCOLA
# -----------------------

st.title("🌾 Cantidad producida por grupo de cultivo")

columnas = ["CULTIVO", "GRUPO CULTIVO", "PRODUCCION(t)", "AÑO"]

if all(col in df_filtrado.columns for col in columnas):

    # Crear lista de grupos
    grupos = sorted(df_filtrado["GRUPO CULTIVO"].dropna().unique())

    # Selector de grupo
    option = st.selectbox(
        "Seleccione un grupo de cultivo para ver su información", grupos)

    # Filtrar por grupo
    filtro_grupo = df_filtrado[df_filtrado["GRUPO CULTIVO"] == option]

    st.write(f"### Consultaste el grupo de: **{option}**")

    # Agrupar por cultivo y año
    totales_cultivo_anio = (
        filtro_grupo.groupby(["CULTIVO", "AÑO"], as_index=False)[
            "PRODUCCION(t)"].sum()
    )

    st.subheader("📊 Producción total por cultivo y año")

    # Gráfico de barras horizontales agrupadas por año
    barras = (
        alt.Chart(totales_cultivo_anio)
        .mark_bar()
        .encode(
            y=alt.Y("CULTIVO:N", sort="-x", title="Cultivo"),
            x=alt.X("PRODUCCION(t):Q", title="Producción (t)"),
            color=alt.Color("AÑO:N", legend=alt.Legend(title="Año")),
            tooltip=["CULTIVO", "AÑO", "PRODUCCION(t)"]
        )
        .properties(height=500)
    )

    # Combinar gráfico final
    chart = barras
    st.altair_chart(chart, use_container_width=True)

else:
    st.error("⚠️ El DataFrame no contiene las columnas esperadas.")

    # Producto mas Producido por Año

# --- Gráfico: Cultivo más producido por grupo ---
st.title("🌾 Cultivo más producido por año (por grupo)")

df_filtrado = df.data_frame_filtrado

# Verificamos que existan las columnas esperadas
columnas = ["CULTIVO", "GRUPO CULTIVO", "PRODUCCION(t)", "AÑO"]
if all(col in df_filtrado.columns for col in columnas):

    # Seleccionar grupo de cultivo
    grupos = sorted(df_filtrado["GRUPO CULTIVO"].dropna().unique())
    option = st.selectbox(
        "Seleccione un grupo de cultivo", grupos
    )

    # Filtrar por grupo
    filtro_grupo = df_filtrado[df_filtrado["GRUPO CULTIVO"] == option]

    # Agrupar por cultivo y año, sumando la producción
    totales = (
        filtro_grupo.groupby(["AÑO", "CULTIVO"], as_index=False)[
            "PRODUCCION(t)"]
        .sum()
    )

    # Obtener el cultivo más producido por año
    maximos_por_anio = totales.loc[
        totales.groupby("AÑO")["PRODUCCION(t)"].idxmax()
    ].reset_index(drop=True)

    st.subheader(f"🏆 Cultivo más producido por año en el grupo: **{option}**")

    # --- Gráfico de barras ---
    chart = (
        alt.Chart(maximos_por_anio)
        .mark_bar(size=50)
        .encode(
            x=alt.X("AÑO:N", title="Año"),
            y=alt.Y("PRODUCCION(t):Q", title="Producción (t)"),
            color=alt.Color("CULTIVO:N", legend=alt.Legend(
                title="Cultivo más producido")),
            tooltip=["AÑO", "CULTIVO", "PRODUCCION(t)"]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

else:
    st.error("⚠️ El DataFrame no contiene las columnas esperadas.")


# === Título ===
st.title("🥧 Distribución de producción agrícola por cultivo")

# Cargar dataframe limpio
df_filtrado = df.data_frame_filtrado

# Verificar columnas necesarias
columnas = ["CULTIVO", "GRUPO CULTIVO", "AÑO", "PRODUCCION(t)"]
if not all(col in df_filtrado.columns for col in columnas):
    st.error("⚠️ El DataFrame no contiene las columnas esperadas.")
else:
    # === Selectbox 1: Grupo de cultivo ===
    grupos = sorted(df_filtrado["GRUPO CULTIVO"].dropna().unique())
    grupo_sel = st.selectbox(
        "Seleccione un grupo de cultivo",
        grupos,
        key="select_grupo_cultivo"  # ✅ clave única
    )

    # Filtrar por grupo
    df_grupo = df_filtrado[df_filtrado["GRUPO CULTIVO"] == grupo_sel]

    # === Selectbox 2: Año ===
    años = sorted(df_grupo["AÑO"].dropna().unique())
    año_sel = st.selectbox(
        "Seleccione un año",
        años,
        key="select_año"  # ✅ clave única
    )

    # Filtrar por año
    df_final = df_grupo[df_grupo["AÑO"] == año_sel]

    # Agrupar por cultivo y sumar producción
    totales = (
        df_final.groupby("CULTIVO", as_index=False)["PRODUCCION(t)"]
        .sum()
        .sort_values("PRODUCCION(t)", ascending=False)
    )

    # === Gráfico de torta ===
    chart = (
        alt.Chart(totales)
        .mark_arc(innerRadius=50)  # tipo "dona"
        .encode(
            theta=alt.Theta("PRODUCCION(t):Q", title="Producción (t)"),
            color=alt.Color("CULTIVO:N", legend=alt.Legend(title="Cultivo")),
            tooltip=[
                alt.Tooltip("CULTIVO:N", title="Cultivo"),
                alt.Tooltip("PRODUCCION(t):Q",
                            title="Producción (t)", format=",.0f"),
            ],
        )
        .properties(
            title=f"Distribución de producción por cultivo - {grupo_sel} ({año_sel})",
            height=500,
        )
    )

    st.altair_chart(chart, use_container_width=True)
