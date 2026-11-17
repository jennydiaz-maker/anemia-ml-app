from pathlib import Path
import pandas as pd
import streamlit as st

st.title("Comparación de modelos")

ruta = Path(__file__).resolve().parents[1] / "artifacts" / "metricas_modelos.csv"
metricas = pd.read_csv(ruta)

st.dataframe(metricas)
st.subheader("F1-macro por modelo")
st.bar_chart(metricas.set_index("modelo")[["f1_macro"]])