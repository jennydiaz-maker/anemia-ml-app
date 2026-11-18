from pathlib import Path

import pandas as pd
import streamlit as st


# Estilo visual
st.markdown(
    """
    <style>
    .stApp {
        background: #f1f8f3;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #174a35;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #d7e9dc;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 105px;
        box-shadow: 0 6px 18px rgba(25, 80, 50, 0.06);
    }

    .metric-label {
        color: #60796a;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    .metric-value {
        color: #17643e;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 8px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #d7e9dc;
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Comparación de modelos")
st.caption(
    "Revisa las métricas y los tiempos de ejecución de los modelos evaluados."
)

# Leer el archivo de métricas
ruta = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "metricas_modelos.csv"
)

if not ruta.exists():
    st.error("No se encontró el archivo artifacts/metricas_modelos.csv.")
    st.stop()

metricas = pd.read_csv(ruta)

if metricas.empty:
    st.warning("El archivo de métricas no contiene resultados.")
    st.stop()

# Tarjetas de resumen
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Modelos comparados</div>
            <div class="metric-value">{len(metricas)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if "f1_macro" in metricas.columns:
    f1 = pd.to_numeric(metricas["f1_macro"], errors="coerce")

    if f1.notna().any():
        indice_mejor = f1.idxmax()
        mejor_f1 = f1.loc[indice_mejor]

        if "modelo" in metricas.columns:
            mejor_modelo = metricas.loc[indice_mejor, "modelo"]
        else:
            mejor_modelo = "No disponible"

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Mayor F1-macro</div>
                    <div class="metric-value">{mejor_f1:.1%}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Modelo con mayor F1-macro</div>
                    <div class="metric-value">{mejor_modelo}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.subheader("Métricas por modelo")

with st.container(border=True):
    metricas_mostrar = metricas.copy()

    columnas_porcentaje = [
        columna
        for columna in [
            "accuracy",
            "f1_macro",
            "recall_LEV",
            "recall_MOD",
            "recall_SEV",
        ]
        if columna in metricas_mostrar.columns
    ]

    columnas_tiempo = [
        columna
        for columna in ["entrenamiento_s", "prediccion_s"]
        if columna in metricas_mostrar.columns
    ]

    formatos = {
        columna: "{:.1%}"
        for columna in columnas_porcentaje
    }
    formatos.update({
        columna: "{:.2f} s"
        for columna in columnas_tiempo
    })

    estilo = metricas_mostrar.style.format(
        formatos,
        na_rep="—",
    )

    st.dataframe(
        estilo,
        use_container_width=True,
        hide_index=True,
    )

# Gráfico de F1-macro
if "modelo" in metricas.columns and "f1_macro" in metricas.columns:
    st.subheader("F1-macro por modelo")
    st.caption(
        "Un valor más alto indica un mejor equilibrio entre las clases."
    )

    grafico = metricas[["modelo", "f1_macro"]].copy()
    grafico["f1_macro"] = pd.to_numeric(
        grafico["f1_macro"],
        errors="coerce",
    )
    grafico = grafico.dropna(subset=["f1_macro"])
    grafico = grafico.sort_values("f1_macro")

    with st.container(border=True):
        st.bar_chart(
            grafico.set_index("modelo"),
            color="#21804d",
            horizontal=True,
            x_label="F1-macro",
        )