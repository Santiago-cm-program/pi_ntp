import pandas as pd

# === Cargar archivo CSV ===
data_frame_cvs = pd.read_csv(
    "src/EVALUACIONES_AGRÍCOLAS__DEL_DEPARTAMENTO_DE_CALDAS_20251010.csv",
    encoding="utf-8",
    on_bad_lines="skip",   # evita errores por filas mal formadas
)

# === Seleccionar columnas relevantes ===
columnas_filtradas = [
    "DEPARTAMENTO",
    "MUNICIPIO",
    "CULTIVO",
    "CICLO DE CULTIVO",
    "GRUPO CULTIVO",
    "SUBGRUPO",
    "AÑO",
    "PERIODO",
    "PRODUCCION(t)",
    "Área Sembrada(ha)",
    "ÁREA COSECHADA(ha)"
]

data_frame_filtrado = data_frame_cvs[columnas_filtradas].copy()

# === Limpieza general ===

# 1️⃣ Eliminar filas completamente vacías
data_frame_filtrado.dropna(how="all", inplace=True)

# 2️⃣ Quitar espacios extra en nombres de columnas y valores de texto
data_frame_filtrado.columns = data_frame_filtrado.columns.str.strip()
for col in ["DEPARTAMENTO", "MUNICIPIO", "CULTIVO", "CICLO DE CULTIVO", "GRUPO CULTIVO", "SUBGRUPO", "PERIODO"]:
    data_frame_filtrado[col] = (
        data_frame_filtrado[col]
        .astype(str)
        .str.strip()
        .str.title()  # Pone mayúscula inicial
    )

# 3️⃣ Convertir valores numéricos
num_cols = ["PRODUCCION(t)", "Área Sembrada(ha)", "ÁREA COSECHADA(ha)"]
for col in num_cols:
    data_frame_filtrado[col] = (
        data_frame_filtrado[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
    )
    data_frame_filtrado[col] = pd.to_numeric(data_frame_filtrado[col], errors="coerce")

# 4️⃣ Convertir año a número entero
data_frame_filtrado["AÑO"] = pd.to_numeric(data_frame_filtrado["AÑO"], errors="coerce").astype("Int64")

# 5️⃣ Eliminar filas sin producción o año
data_frame_filtrado = data_frame_filtrado.dropna(subset=["PRODUCCION(t)", "AÑO"])

# 6️⃣ Eliminar duplicados
data_frame_filtrado.drop_duplicates(inplace=True)

# 7️⃣ Ordenar por año y grupo
data_frame_filtrado.sort_values(by=["GRUPO CULTIVO", "AÑO"], inplace=True)
