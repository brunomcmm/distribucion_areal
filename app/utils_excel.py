import pandas as pd
import tempfile
import os


def leer_excel_ou_csv(archivo, sheet_name=None, skiprows=None):
    """
    Lê um arquivo Excel (.xls, .xlsx) ou CSV (.csv) e retorna um DataFrame.
    Se for Excel, pode usar sheet_name e skiprows.
    """
    try:
        if archivo.name.endswith('.csv'):
            return pd.read_csv(archivo, skiprows=skiprows)
        else:
            return pd.read_excel(archivo, sheet_name=sheet_name, skiprows=skiprows)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")


def leer_conexiones(archivo):
    """
    Lê a aba 'CONNECTION' de um arquivo Excel ou todo o CSV.
    """
    try:
        return leer_excel_ou_csv(archivo, sheet_name="CONNECTION")
    except Exception as e:
        raise ValueError(f"No se pudo leer la hoja 'CONNECTION': {e}")


def leer_datos_volumetricos_formatados(archivo):
    """
    Lê dados volumétricos formatados a partir de um Excel ou CSV.
    """
    try:
        df_raw = leer_excel_ou_csv(archivo, skiprows=6)

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


def guardar_excel_temporal(df):
    """
    Salva um DataFrame como Excel temporário e retorna o caminho.
    """
    try:
        temp_dir = tempfile.gettempdir()
        ruta_archivo = os.path.join(temp_dir, "resultado.xlsx")
        df.to_excel(ruta_archivo, index=False)
        return ruta_archivo
    except Exception as e:
        raise ValueError(f"No se pudo guardar el archivo Excel: {e}")