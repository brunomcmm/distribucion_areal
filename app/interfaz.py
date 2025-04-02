import os
import streamlit as st
from app.procesador import procesar_archivos
from app.utils_excel import leer_conexiones, leer_datos_volumetricos_formatados, guardar_excel_temporal

def mostrar_interfaz():
    st.write("Sube dos archivos Excel o CSV y genera una salida procesada con la opción de descargarla.")

    archivo1 = st.file_uploader("Selecciona el archivo Excel o CSV (con hoja 'CONNECTION')", type=[".xlsx", ".xls", ".csv"])
    archivo2 = st.file_uploader("Selecciona el archivo Excel o CSV (volúmenes por pozo)", type=[".xlsx", ".xls", ".csv"])

    df_conexiones = None
    df_volumenes  = None

    if archivo1:
        try:
            df_conexiones = leer_conexiones(archivo1)
            st.success("Hoja 'CONNECTION' cargada correctamente.")

            columnas_mostradas = ["INJECTOR", "PRODUCER", "WELL_TYPE", "DIST_BYPROD"]
            columnas_disponibles = [col for col in columnas_mostradas if col in df_conexiones.columns]

            # Vista previa opcional
            # if columnas_disponibles:
            #     st.dataframe(df_conexiones[columnas_disponibles].head(10))

        except Exception as e:
            st.error(f"Error al leer la hoja 'CONNECTION': {e}")

    if archivo2:
        try:
            df_volumenes = leer_datos_volumetricos_formatados(archivo2)
            df_volumenes.rename(columns={"POZO": "POZO INJECTOR"}, inplace=True)
            st.success("Archivo de volúmenes cargado correctamente.")

            # Vista previa opcional
            # st.dataframe(df_volumenes.head(10))

        except Exception as e:
            st.error(f"Error al procesar el archivo de volúmenes: {e}")

    if df_conexiones is not None and df_volumenes is not None:
        if st.button("Procesar Archivos"):
            try:
                df_resultado = procesar_archivos(df_conexiones, df_volumenes)
                ruta_salida = guardar_excel_temporal(df_resultado)

                with open(ruta_salida, "rb") as f:
                    st.download_button(
                        label="🗂️ Descargar archivo resultado",
                        data=f,
                        file_name="resultado.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                st.success("¡Procesamiento finalizado exitosamente!")

            except Exception as e:
                st.error(f"Ocurrió un error durante el procesamiento: {e}")
    else:
        st.info("Por favor, sube ambos archivos para habilitar el procesamiento.")

    if st.button("Salir del programa"):
        st.warning("Cerrando aplicación...")
        os._exit(0)