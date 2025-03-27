'''
# Distribución Areal - Procesador de Archivos Excel
# Versión: 0.01
streamlit run main.py
'''

import os
import streamlit as st
from app.interfaz import mostrar_interfaz

# Limpieza de la consola
os.system('clear')

# Versión del programa
version = 0.01

# Configuraciones iniciales de la página
st.set_page_config(
    page_title="Distribución Areal - Procesador de Archivos Excel",
    page_icon="📂",
    layout="wide"
)

# Título principal
def main():
    st.markdown("<h1 style='font-size: 28px;'>Distribución Areal</h1>", unsafe_allow_html=True)
    
    mostrar_interfaz()

if __name__ == "__main__":
    main()