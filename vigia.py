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
    # Comprobar si la carpeta "PDF" ya existe, y si no, crearla
    if not os.path.exists('PDF'):
        os.mkdir('PDF')
    else:
        st.warning("El directorio 'PDF' ya existe.")

    # Por medio del Xpath extraemos la URL del mes actual de los editos de CORNARE
    r = requests.get("https://www.cornare.gov.co/boletin-oficial/")
    soup = BeautifulSoup(r.content, "html.parser")
    dom = etree.HTML(str(soup))
    url = dom.xpath('//*[@id="f935fbc7ba2b28a6f"]/div/ul/li[1]/a/@href')
    url2 = str(url)
    url3 = url2.strip("['/']")

    response = requests.get(url3)

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    i = 0
    total_pdfs = sum('.pdf' in link.get('href', []) for link in links)

    with st.empty():
        for link in links:
            if '.pdf' in link.get('href', []):
                i += 1
                pdf_url = link.get('href')
                st.write(f"Descargando archivo {i}/{total_pdfs}: {pdf_url}")

                # Intentar descargar el archivo
                try:
                    response = requests.get(pdf_url)
                    pdf_path = os.path.join("PDF", f"pdf{i}.pdf")
                    with open(pdf_path, 'wb') as pdf:
                        pdf.write(response.content)
                    st.write(f"Archivo {i} descargado y guardado en {pdf_path}")

                    # Actualizar barra de progreso
                    progress = i / total_pdfs
                    st.progress(progress)

                except Exception as e:
                    st.error(f"Error al descargar el archivo {pdf_url}: {e}")

    st.success("Archivos PDF descargados exitosamente.")

# Función para procesar archivos PDF descargados
def process_downloaded_pdfs(keyword):
    path = "PDF"
    path2 = "separados"
    files = os.listdir(path)
    contador = 0
    st.write(f"Buscando la palabra '{keyword}' en los archivos PDF descargados:")

    for file in tqdm(files):
        try:
            doc = fitz.open(os.path.join(path, file))
            encontrado = False

            for page in doc:
                text = page.get_text()
                if keyword in text:
                    page.add_highlight_annot(text.find(keyword), text.rfind(keyword), fill="red")
                    encontrado = True

            if encontrado:
                doc.save(os.path.join(path2, file))
                sleep(0.5)
                contador += 1

        except Exception as e:
            st.error(f"Error al procesar el archivo {file}: {e}")
            continue

    st.success(f"De {len(files)} archivos analizados, {contador} tienen la palabra '{keyword}' resaltada.")

# Función para borrar todos los PDF descargados
def delete_downloaded_pdfs():
    path = "PDF"
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            os.remove(file_path)
        st.success("Archivos PDF descargados eliminados con éxito.")

# Limpiar archivos PDF descargados al inicio de la aplicación
if os.path.exists("PDF"):
    delete_downloaded_pdfs()

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
        delete_downloaded_pdfs()
