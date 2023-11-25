import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from lxml import etree
import fitz
from time import sleep
from tqdm import tqdm

# Función para descargar archivos PDF
def download_pdfs():
    # Resto del código para descargar PDFs

# Función para procesar archivos PDF descargados
def process_downloaded_pdfs(keyword):
    # Resto del código para procesar PDFs

# Función para borrar todos los PDF descargados
def delete_downloaded_pdfs():
    path = "PDF"
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            os.remove(file_path)
        st.success("Archivos PDF descargados eliminados con éxito.")

# Interfaz de usuario
menu = st.sidebar.selectbox("Selecciona una opción:", ["Descargar PDFs", "Procesar PDFs", "Eliminar PDFs"])

if menu == "Descargar PDFs":
    st.sidebar.header("Descargar PDFs")
    st.sidebar.write("Haga clic en el botón para descargar archivos PDF.")
    if st.sidebar.button("Descargar"):
        download_pdfs()

elif menu == "Procesar PDFs":
    st.sidebar.header("Procesar PDFs")
    keyword = st.text_input("Ingrese una palabra clave:")
    if st.sidebar.button("Procesar"):
        if not keyword:
            st.error("Por favor, ingrese una palabra clave.")
        else:
            process_downloaded_pdfs(keyword)

elif menu == "Eliminar PDFs":
    st.sidebar.header("Eliminar PDFs")
    st.sidebar.write("Haga clic en el botón para eliminar los archivos PDF descargados manualmente.")
    
    if st.sidebar.button("Eliminar"):
        # Se añade una confirmación del usuario antes de eliminar los PDFs
        if st.checkbox("Confirmar eliminación"):
            delete_downloaded_pdfs()
            st.success("Archivos PDF descargados eliminados con éxito.")
        else:
            st.warning("Por favor, confirme la eliminación marcando la casilla.")

