import pandas as pd
import tempfile
import os


def leer_excel(archivo):
    """
    Lee un archivo Excel y retorna un DataFrame (primera hoja por defecto).
    """
    try:
        return pd.read_excel(archivo)
    except Exception as e:
        raise ValueError(f"No se pudo leer el archivo Excel: {e}")


def leer_conexiones(archivo):
    """
    Lee la hoja 'CONNECTION' de un archivo Excel con múltiples hojas.
    """
    try:
        df = pd.read_excel(archivo, sheet_name="CONNECTION")
        return df
    except Exception as e:
        raise ValueError(f"No se pudo leer la hoja 'CONNECTION': {e}")


def guardar_excel_temporal(df):
    """
    Guarda un DataFrame como archivo Excel temporal y retorna la ruta.
    """
    try:
        temp_dir = tempfile.gettempdir()
        ruta_archivo = os.path.join(temp_dir, "resultado.xlsx")
        df.to_excel(ruta_archivo, index=False)
        return ruta_archivo
    except Exception as e:
        raise ValueError(f"No se pudo guardar el archivo Excel: {e}")


def leer_datos_volumetricos_formatados(caminho_excel):
    """
    Lee un archivo Excel con múltiples bloques de datos por pozo y lo reorganiza en formato largo.
    """
    try:
        df_raw = pd.read_excel(caminho_excel, skiprows=6)

        nombres_pozos = df_raw.iloc[0, 1::3].tolist()
        columnas_datos = df_raw.iloc[1, 1:4].tolist()
        fechas = df_raw.iloc[2:, 0].reset_index(drop=True)

        datos_formatados = []

        for i, pozo in enumerate(nombres_pozos):
            col_inicio = 1 + i * 3
            col_fin = col_inicio + 3

            df_temp = df_raw.iloc[2:, col_inicio:col_fin].reset_index(drop=True)
            df_temp.columns = columnas_datos
            df_temp.insert(0, "FECHA", fechas)
            df_temp.insert(1, "POZO", pozo)

            datos_formatados.append(df_temp)

        df_final = pd.concat(datos_formatados, ignore_index=True)
        return df_final

    except Exception as e:
        raise ValueError(f"Error al procesar datos volumétricos: {e}")