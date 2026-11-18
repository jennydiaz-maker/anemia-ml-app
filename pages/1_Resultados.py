from pathlib import Path

import pandas as pd
import streamlit as st


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
        font-size: 1.45rem;
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
st.caption("Revisa el desempeño y el tiempo de ejecución de los modelos evaluados.")

ruta = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "metricas_modelos.csv"
)

if not ruta.exists():
    st.error(f"No se encontró el archivo de métricas: {ruta.name}")
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
        mejor_modelo = metricas.loc[indice_mejor, "modelo"]
        mejor_f1 = f1.loc[indice_mejor]

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

    porcentajes = [
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

    tiempos = [
        columna
        for columna in ["entrenamiento_s", "prediccion_s"]
        if columna in metricas_mostrar.columns
    ]

    formatos = {columna: "{:.1%}" for columna in porcentajes}
    formatos.update({columna: "{:.2f} s" for columna in tiempos})

    estilo = metricas_mostrar.style.format(formatos, na_rep="—")

    if "f1_macro" in metricas_mostrar.columns:
        estilo = estilo.background_gradient(
            cmap="Greens",
            subset=["f1_macro"],
        )

    st.dataframe(
        estilo,
        use_container_width=True,
        hide_index=True,
    )

if "f1_macro" in metricas.columns and "modelo" in metricas.columns:
    st.subheader("F1-macro por modelo")
    st.caption(
        "Un valor más alto indica un mejor equilibrio entre precisión "
        "y cobertura de las clases."
    )

    with st.container(border=True):
        grafico = metricas[["modelo", "f1_macro"]].copy()
        grafico["f1_macro"] = pd.to_numeric(
            grafico["f1_macro"],
            errors="coerce",
        )
        grafico = grafico.dropna(subset=["f1_macro"])
        grafico = grafico.sort_values("f1_macro")

        st.bar_chart(
            grafico.set_index("modelo"),
            color="#21804d",
            horizontal=True,
            x_label="F1-macro",
        )