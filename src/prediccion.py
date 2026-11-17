from pathlib import Path
import joblib
import pandas as pd

def cargar_paquete():
    ruta = (
        Path(__file__).resolve().parents[1]
        / "artifacts"
        / "modelos_anemia.joblib"
    )
    return joblib.load(ruta)


def preparar_entrada(paquete, valores):
    columnas = paquete["columnas"]
    fila = pd.DataFrame(0, index=[0], columns=columnas)

    # Campos numéricos
    campos_numericos = {
        "EDAD_MESES": valores["edad"],
        "ANIO_ATENCION": valores["anio"],
        "MES_ATENCION": valores["mes"],
    }

    for columna, valor in campos_numericos.items():
        if columna in fila.columns:
            fila.loc[0, columna] = valor

    # Campos categóricos convertidos a columnas indicadoras
    campos_categoricos = {
        "GENERO": valores["genero"],
        "ETNIA": valores["etnia"],
        "DESCRIPCION_FINANCIADOR": valores["financiador"],
        "PROVINCIA": valores["provincia"],
    }

    for campo, valor in campos_categoricos.items():
        prefijo = f"{campo}_"
        columna_indicadora = f"{prefijo}{valor}"

        if columna_indicadora in fila.columns:
            fila.loc[0, columna_indicadora] = 1

    return fila


def predecir(paquete, nombre_modelo, valores):
    entrada = preparar_entrada(paquete, valores)
    modelo = paquete["modelos"][nombre_modelo]

    if nombre_modelo == "Regresión Logística":
        entrada_escalada = paquete["escalador"].transform(entrada)
        entrada = pd.DataFrame(
            entrada_escalada,
            columns=paquete["columnas"],
            index=entrada.index,
        )

    codigo = int(modelo.predict(entrada)[0])

    clases = {
        0: "Leve",
        1: "Moderada",
        2: "Severa",
    }

    return clases.get(codigo, f"Clase {codigo}")