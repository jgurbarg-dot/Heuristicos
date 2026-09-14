import io
import re
import PyPDF2
import requests
import streamlit as st
from deep_translator import GoogleTranslator

# Configuración de archivos (puedes usar URLs o archivos locales)
URLS_NUBE = {
    "Seider": "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/Seider%20-%20Cap%C3%ADtulo%206.pdf",
    "Walas": "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/122%20-%20Heur%C3%ADsticas%20_Walas%20(2012).pdf",
}

ARCHIVOS_LOCALES = {
    "Seider": "Seider - Capítulo 6.pdf",
    "Walas": "122 - Heurísticas _Walas (2012).pdf",
}

@st.cache_data(show_spinner="Cargando documento en memoria...")
def cargar_lector_pdf(fuente):
    url = URLS_NUBE.get(fuente)
    if url and "TU_USUARIO" not in url:
        try:
            respuesta = requests.get(url, timeout=10)
            if respuesta.status_code == 200:
                archivo_en_memoria = io.BytesIO(respuesta.content)
                return PyPDF2.PdfReader(archivo_en_memoria)
        except Exception:
            pass 

    nombre_archivo = ARCHIVOS_LOCALES.get(fuente)
    try:
        return PyPDF2.PdfReader(nombre_archivo)
    except FileNotFoundError:
        st.error(f"⚠️ No se encontró el archivo '{nombre_archivo}'.")
        return None
    except Exception as e:
        st.error(f"Error al leer el archivo PDF: {e}")
        return None

@st.cache_data(show_spinner=False)
def extraer_bloques_heuristicos(_lector):
    if not _lector:
        return []
    bloques = []
    for num_pag, pagina in enumerate(_lector.pages):
        texto = pagina.extract_text()
        if texto:
            parrafos = re.split(r"\n\s*\n|(?=\n\d+[\.\)])|(?=\nHeuristic)|(?=\nRegla)", texto)
            for p in parrafos:
                p_limpio = p.strip()
                if len(p_limpio) > 40:
                    bloques.append({"pagina": num_pag + 1, "texto": p_limpio})
    return bloques

def buscar_heuristicos(lector, palabra_clave):
    bloques = extraer_bloques_heuristicos(lector)
    palabra = palabra_clave.lower().strip()
    resultados = []
    for b in bloques:
        if palabra in b["texto"].lower():
            resultados.append(b)
    return resultados

@st.cache_data(show_spinner=False)
def traducir_texto(texto):
    """Traduce el texto al español y lo guarda en caché para no repetir el proceso."""
    try:
        # El límite de caracteres de Google Translator es 5000 por bloque
        if len(texto) > 4999:
            texto = texto[:4999]
        traductor = GoogleTranslator(source='auto', target='es')
        return traductor.translate(texto)
    except Exception as e:
        return f"[Error al traducir: {e}]\n\n{texto}"

# Interfaz Streamlit
st.set_page_config(page_title="Análisis de Heurísticas", page_icon="⚙️", layout="centered")

if "fuente_elegida" not in st.session_state:
    st.session_state.fuente_elegida = None
if "indice_resultado" not in st.session_state:
    st.session_state.indice_resultado = 0
if "ultima_busqueda" not in st.session_state:
    st.session_state.ultima_busqueda = ""

st.title("Análisis de Heurísticas en Ingeniería Química")

if st.session_state.fuente_elegida is None:
    st.write("Por favor, selecciona qué conjunto de heurísticas deseas consultar antes de continuar:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Heurísticas de Seider", use_container_width=True):
            st.session_state.fuente_elegida = "Seider"
            st.session_state.indice_resultado = 0
            st.session_state.ultima_busqueda = ""
            st.rerun()
    with col2:
        if st.button("Heurísticas de Walas", use_container_width=True):
            st.session_state.fuente_elegida = "Walas"
            st.session_state.indice_resultado = 0
            st.session_state.ultima_busqueda = ""
            st.rerun()

else:
    fuente = st.session_state.fuente_elegida
    st.success(f"Base de datos seleccionada: **{fuente}**")
    lector = cargar_lector_pdf(fuente)
    palabra_busqueda = st.text_input(f"🔍 Ingresa un término en español o inglés (ej. bomba, destilación, reflux, pump):", key="campo_busqueda")

    if palabra_busqueda != st.session_state.ultima_busqueda:
        st.session_state.indice_resultado = 0
        st.session_state.ultima_busqueda = palabra_busqueda

    if palabra_busqueda:
        resultados = buscar_heuristicos(lector, palabra_busqueda)
        if resultados:
            total_res = len(resultados)
            idx_actual = st.session_state.indice_resultado
            if idx_actual >= total_res:
                idx_actual = 0
                st.session_state.indice_resultado = 0

            st.markdown(f"**Coincidencia {idx_actual + 1} de {total_res}**")
            heuristico_actual = resultados[idx_actual]
            st.info(f"**Página del PDF:** {heuristico_actual['pagina']}")

            # Traducción en tiempo real del bloque actual
            with st.spinner("Traduciendo al español..."):
                texto_espanol = traducir_texto(heuristico_actual["texto"])

            st.text_area(label="Heurístico Completo (Traducido):", value=texto_espanol, height=220)
            
            with st.expander("Ver texto original en inglés"):
                st.write(heuristico_actual["texto"])

            col_prev, col_num, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("⬅️ Anterior", disabled=(idx_actual == 0), use_container_width=True):
                    st.session_state.indice_resultado -= 1
                    st.rerun()
            with col_num:
                st.write(f"<div style='text-align: center; padding-top: 5px;'><b>{idx_actual + 1} / {total_res}</b></div>", unsafe_allow_html=True)
            with col_next:
                if st.button("Siguiente ➡️", disabled=(idx_actual == total_res - 1), use_container_width=True):
                    st.session_state.indice_resultado += 1
                    st.rerun()
        else:
            st.warning(f"No se encontraron heurísticos que contengan la palabra '{palabra_busqueda}'.")

    st.divider()
    if st.button("← Volver al menú principal"):
        st.session_state.fuente_elegida = None
        st.session_state.indice_resultado = 0
        st.session_state.ultima_busqueda = ""
        st.rerun()
