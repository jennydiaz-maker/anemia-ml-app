import streamlit as st
from src.prediccion import cargar_paquete, predecir
st.title("Simulación de anemia")
st.info("Simulación educativa; no es un diagnóstico clínico.")

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

edad = st.number_input("Edad (meses)", min_value=0, max_value=59, value=12)
genero = st.selectbox("Género", ["F", "M"])
etnia = st.selectbox(
    "Etnia",
    ["Mestizo", "Kichwa", "Awajun", "Shawi", "Otras Pob. Indigenas", "Quechua"],
)
financiador = st.selectbox(
    "Financiador",
    ["S.I.S", "USUARIO", "OTROS", "EXONERADO", "ESSALUD", "SANIDAD PNP"],
)
provincia = st.selectbox(
    "Provincia",
    [
        "SAN MARTIN", "LAMAS", "RIOJA", "MOYOBAMBA", "TOCACHE",
        "EL DORADO", "MARISCAL CACERES", "BELLAVISTA", "PICOTA", "HUALLAGA",
    ],
)
anio = st.number_input("Año de atención", min_value=2016, max_value=2025, value=2024)
mes = st.selectbox("Mes de atención", list(range(1, 13)))
paquete = cargar_paquete()
st.success(f"Modelos cargados: {', '.join(paquete['modelos'].keys())}")

if st.button("Predecir severidad", type="primary"):
    valores = {
        "edad": edad,
        "genero": genero,
        "etnia": etnia,
        "financiador": financiador,
        "provincia": provincia,
        "anio": anio,
        "mes": mes,
    }

    resultado = predecir(paquete, modelo, valores)

    st.subheader("Resultado de la simulación")
    st.success(f"Clase predicha: {resultado}")
    st.caption("Simulación educativa; no es un diagnóstico clínico.")