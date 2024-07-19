import streamlit as st
import requests
from bs4 import BeautifulSoup
import PyPDF2
from io import BytesIO

def obtener_url_editos():
    r = requests.get("https://www.cornare.gov.co/boletin-oficial/")
    soup = BeautifulSoup(r.content, "html.parser")
    url = soup.select_one('#f935fbc7ba2b28a6f > div > ul > li > a')['href']
    return url

def buscar_palabra_clave_en_pdf(url, palabra_clave):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    total_pdfs = 0
    encontrados = 0

    # Contar el número total de archivos PDF
    for link in links:
        if link.get('href').endswith('.pdf'):
            total_pdfs += 1

    if total_pdfs == 0:
        st.sidebar.write("No se encontraron archivos PDF para revisar.")
        return

    progreso = st.sidebar.progress(0)
    progreso_texto = st.sidebar.empty()
    pdfs_procesados = 0

    for link in links:
        link_href = link.get('href')
        if link_href.endswith('.pdf'):
            # Convertir URLs relativas a absolutas
            if not link_href.startswith('http'):
                link_href = 'https://www.cornare.gov.co' + link_href

            try:
                pdf_response = requests.get(link_href)
                if pdf_response.status_code == 200:
                    # Descargar todo el PDF en memoria
                    pdf_data = pdf_response.content

                    # Procesar el PDF en memoria
                    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_data))
                    paginas_con_palabra_clave = []

                    for page_num, page in enumerate(pdf_reader.pages):
                        page_text = page.extract_text()

                        # Buscar la palabra clave en cada página
                        if page_text and palabra_clave in page_text:
                            paginas_con_palabra_clave.append(page_num + 1)

                    if paginas_con_palabra_clave:
                        st.write(f"La palabra clave '{palabra_clave}' se encontró en las páginas {paginas_con_palabra_clave} del PDF: {link_href}")
                        encontrados += 1

            except Exception as e:
                st.write(f"No se pudo analizar el PDF en '{link_href}': {e}")

            # Actualizar progreso
            pdfs_procesados += 1
            porcentaje = pdfs_procesados / total_pdfs
            progreso.progress(porcentaje)
            progreso_texto.text(f"Progreso: {int(porcentaje * 100)}%")

    if encontrados == 0:
        st.write("No se encontró la palabra clave en ninguno de los PDFs revisados.")
    else:
        st.write("Todos los archivos PDF han sido revisados.")

st.set_page_config(page_title="Vigías del Río Dormilón", page_icon=":guardsman:", layout="wide")

st.title("Vigías del Río Dormilón de San Luis Antioquia")
st.image("https://github.com/echeverri58/vigiadigital/blob/main/logo.png?raw=true", width=200)  # Asegúrate de tener un archivo 'logo.png' en tu directorio
st.markdown("""
### Este es un script para fortalecer los procesos de resistencia e incidencia de las comunidades en defensa de los recursos naturales.

Desde el Movimiento Vigías del Río Dormilón de San Luis Antioquia queremos compartir este código con todas las organizaciones sociales y ambientales, con el fin de tener más herramientas que permitan estar informados de los procesos de licenciamiento y solicitudes de permisos ambientales expedidos por las autoridades ambientales, logrando asi evidenciar si se esta garantizando el derecho de la participación de todos los actores sociales y comunidades del territorio.

Este programa permite descargar PDF de un enlace para posteriormente hacer búsquedas automatizadas de palabras claves y posteriormente si encuentra algún documento con esas palabras, los envía a un grupo de Telegram, con el fin de alertar a las comunidades sobre posibles amenazas de proyectos extractivos.

Es un gusto poder servir en la lucha por la defensa del territorio, el ambiente, el agua y la vida.
""")

st.sidebar.header("Buscar en PDFs")
palabra_clave = st.sidebar.text_input("Palabra clave para buscar", value="San Luis")

if st.sidebar.button("Buscar"):
    url = obtener_url_editos()
    buscar_palabra_clave_en_pdf(url, palabra_clave)
