from pathlib import Path
import base64
import streamlit as st

st.set_page_config(
    page_title="Proyecto de anemia | San Martín",
    page_icon="🌿",
    layout="wide",
)

ruta_imagen = Path(__file__).parent / "assets" / "fondo_anemia.png"
imagen = base64.b64encode(ruta_imagen.read_bytes()).decode("utf-8")

css = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f4faf5 0%, #edf6ef 100%);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    min-height: 430px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3rem;
    border-radius: 26px;
    color: white;
    background-image:
        linear-gradient(90deg, rgba(5, 48, 34, 0.94) 0%,
                               rgba(5, 48, 34, 0.78) 57%,
                               rgba(5, 48, 34, 0.08) 100%),
        url("data:image/png;base64,__IMAGEN__");
    background-size: cover;
    background-position: center;
    box-shadow: 0 16px 40px rgba(19, 75, 48, 0.18);
}

.hero-kicker {
    color: #c7e7d1;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero h1 {
    max-width: 780px;
    color: white;
    font-size: clamp(2rem, 4vw, 3.15rem);
    line-height: 1.12;
    margin: 0;
}

.hero p {
    max-width: 680px;
    color: #e4f1e8;
    font-size: 1.08rem;
    margin-top: 1.3rem;
}

.section-title {
    color: #174b34;
    margin-top: 2rem;
}

.info-card, .stat-card {
    height: 100%;
    padding: 1.35rem;
    border: 1px solid #dcebe0;
    border-radius: 18px;
    background: white;
    box-shadow: 0 8px 22px rgba(31, 75, 49, 0.07);
}

.info-card h3 {
    color: #1b6240;
    margin-top: 0;
}

.info-card p, .info-card li {
    color: #3e5145;
    line-height: 1.65;
}

.stat-label {
    color: #557060;
    font-size: 0.95rem;
    font-weight: 650;
}

.stat-number {
    color: #17613d;
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0.4rem 0;
}

.stat-note {
    color: #697b70;
    font-size: 0.9rem;
}

.source-note {
    color: #627569;
    font-size: 0.85rem;
    padding: 1rem 0;
}
</style>
"""

st.markdown(css.replace("__IMAGEN__", imagen), unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
        <div class="hero-kicker">Applied Machine Learning · Región San Martín</div>
        <h1>Simulación del grado de severidad de anemia en niños menores de 5 años de la región San Martín mediante técnicas de Machine Learning</h1>
        <p>Exploración de los registros de anemia infantil y comparación de modelos de clasificación.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h2 class="section-title">Problema y contexto</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <h3>¿Qué problema aborda?</h3>
            <p>El proyecto estudia cómo anticipar el grado de severidad de anemia
            —leve, moderada o severa— a partir de características demográficas,
            geográficas y de atención.</p>
            <p>El documento señala que en Perú la anemia afectó al 43.1% de los
            niños de 6 a 35 meses en 2023, con mayor incidencia en zonas rurales.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <h3>¿De dónde vienen los datos?</h3>
            <p>El dataset proviene del reporte del Gobierno Regional de San Martín
            publicado en la Plataforma Nacional de Datos Abiertos del Perú.</p>
            <p>Contiene registros de atenciones entre enero de 2016 y abril de 2025,
            con información demográfica, geográfica y administrativa.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<h2 class="section-title">Análisis exploratorio</h2>', unsafe_allow_html=True)
st.markdown(
    "El dataset original contiene **59,225 registros y 22 atributos**. "
    "La distribución de severidad muestra un fuerte desbalance entre las clases:"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">LEVE</div>
            <div class="stat-number">78.41%</div>
            <div class="stat-note">46,441 registros</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">MODERADA</div>
            <div class="stat-number">21.14%</div>
            <div class="stat-note">12,523 registros</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">SEVERA</div>
            <div class="stat-number">0.42%</div>
            <div class="stat-note">246 registros</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown(
        """
        <div class="info-card">
            <h3>Evolución de las atenciones</h3>
            <ul>
                <li>El documento identifica un pico de más de 1,200 atenciones
                mensuales entre 2018 y 2019.</li>
                <li>En 2020 se observa una caída, que el informe atribuye a la pandemia.</li>
                <li>Desde 2021, las atenciones se estabilizan alrededor de 500 al mes.</li>
                <li>La proporción de casos moderados pasó de 12.9% en 2016 a
                26.4% en 2024.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="info-card">
            <h3>Diferencias observadas</h3>
            <ul>
                <li>Tocache presenta 26.5% de casos moderados y San Martín 25.1%.</li>
                <li>Bellavista registra 12.4% y Huallaga 14.3%.</li>
                <li>La proporción moderada es 22.1% en varones y 20.1% en mujeres.</li>
                <li>La etnia Shawi presenta 30.5%; el documento advierte que corresponde
                a solo 249 registros.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="source-note">
        Fuente de los datos y hallazgos: ProyectoAML.pdf, secciones 1.2, 1.3,
        2.1 y 2.4. La cifra nacional de 2023 se cita en el documento como
        INEI–ENDES 2023.
    </div>
    """,
    unsafe_allow_html=True,
)