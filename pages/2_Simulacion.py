import streamlit as st
from src.prediccion import cargar_paquete, predecir


st.markdown(
    """
    <style>
    .stApp {
        background: #f1f8f3;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #174a35;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.92);
        border-color: #d7e9dc;
        border-radius: 18px;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    .stButton > button[kind="primary"] {
        background: #21804d;
        border: 0;
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
    }

    .stButton > button[kind="primary"]:hover {
        background: #17643e;
        border: 0;
    }

    .result-card {
        background: #e7f5eb;
        border: 1px solid #c7e5d0;
        border-radius: 16px;
        padding: 22px 24px;
        margin-top: 12px;
    }

    .result-label {
        color: #547361;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .result-value {
        color: #17643e;
        font-size: 1.8rem;
        font-weight: 750;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def cargar_paquete_en_cache():
    return cargar_paquete()


st.title("Simulación de anemia")
st.info("Simulación educativa; no es un diagnóstico clínico.")

with st.container(border=True):
    st.subheader("Datos para la simulación")

    modelo = st.selectbox(
        "Selecciona el modelo",
        [
            "Regresión Logística",
            "Árbol de Decisión",
            "Random Forest",
            "Gradient Boosting",
            "Random Forest optimizado",
        ],
    )

    izquierda, derecha = st.columns(2)

    with izquierda:
        edad = st.number_input(
            "Edad (meses)",
            min_value=0,
            max_value=59,
            value=12,
        )
        etnia = st.selectbox(
            "Etnia",
            [
                "Mestizo",
                "Kichwa",
                "Awajun",
                "Shawi",
                "Otras Pob. Indigenas",
                "Quechua",
            ],
        )
        provincia = st.selectbox(
            "Provincia",
            [
                "SAN MARTIN",
                "LAMAS",
                "RIOJA",
                "MOYOBAMBA",
                "TOCACHE",
                "EL DORADO",
                "MARISCAL CACERES",
                "BELLAVISTA",
                "PICOTA",
                "HUALLAGA",
            ],
        )
        mes = st.selectbox("Mes de atención", list(range(1, 13)))

    with derecha:
        genero = st.selectbox("Género", ["F", "M"])
        financiador = st.selectbox(
            "Financiador",
            [
                "S.I.S",
                "USUARIO",
                "OTROS",
                "EXONERADO",
                "ESSALUD",
                "SANIDAD PNP",
            ],
        )
        anio = st.number_input(
            "Año de atención",
            min_value=2016,
            max_value=2025,
            value=2024,
        )

    st.caption("Los modelos se cargan cuando solicitas una predicción.")

    predecir_boton = st.button(
        "Predecir severidad",
        type="primary",
        use_container_width=True,
    )

if predecir_boton:
    valores = {
        "edad": edad,
        "genero": genero,
        "etnia": etnia,
        "financiador": financiador,
        "provincia": provincia,
        "anio": anio,
        "mes": mes,
    }

    try:
        with st.spinner("Cargando el modelo y calculando la predicción..."):
            paquete = cargar_paquete_en_cache()
            resultado = predecir(paquete, modelo, valores)

        st.subheader("Resultado de la simulación")
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Grado estimado</div>
                <div class="result-value">{resultado}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Simulación educativa; el resultado no reemplaza una evaluación "
            "profesional de salud."
        )

    except Exception as error:
        st.error("No se pudo calcular la predicción.")
        st.exception(error)