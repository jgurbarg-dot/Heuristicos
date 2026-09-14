import streamlit as st
import PyPDF2

# Función para buscar texto en el PDF
def buscar_en_pdf(archivo_pdf, palabra_clave):
    resultados = []
    try:
        with open(archivo_pdf, 'rb') as f:
            lector = PyPDF2.PdfReader(f)
            for num_pagina, pagina in enumerate(lector.pages):
                texto = pagina.extract_text()
                if texto and palabra_clave.lower() in texto.lower():
                    # Extraer un poco de contexto alrededor de la palabra encontrada
                    inicio = max(0, texto.lower().find(palabra_clave.lower()) - 80)
                    fin = min(len(texto), inicio + 160 + len(palabra_clave))
                    contexto = texto[inicio:fin].replace('\n', ' ')
                    resultados.append({'pagina': num_pagina + 1, 'contexto': contexto})
    except FileNotFoundError:
        st.error(f"⚠️ No se encontró el archivo '{archivo_pdf}'. Asegúrate de que esté en la misma carpeta que app.py y tenga el nombre exacto.")
    except Exception as e:
        st.error(f"Ocurrió un error al leer el PDF: {e}")
    return resultados

# Configuración inicial de la página
st.set_page_config(page_title="Análisis de Heurísticas", page_icon="⚙️", layout="centered")

# 1. Inicializar la variable de control en el estado de la sesión
if 'fuente_elegida' not in st.session_state:
    st.session_state.fuente_elegida = None

st.title("Análisis de Heurísticas en Ingeniería Química")

# 2. Pantalla inicial: Mostrar los botones si aún no se ha elegido nada
if st.session_state.fuente_elegida is None:
    st.write("Por favor, selecciona qué conjunto de heurísticas deseas consultar antes de continuar:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Heurísticas de Seider", use_container_width=True):
            st.session_state.fuente_elegida = "Seider"
            st.rerun()
            
    with col2:
        if st.button("Heurísticas de Walas", use_container_width=True):
            st.session_state.fuente_elegida = "Walas"
            st.rerun()

# 3. Flujo de ejecución principal según la elección del usuario
if st.session_state.fuente_elegida == "Seider":
    st.success("Base de datos seleccionada: Seider - Capítulo 6")
    st.subheader("Buscador: Heurísticas para la Síntesis de Procesos")
    
    # Buscador para Seider
    palabra_busqueda = st.text_input("🔍 Ingresa una palabra o término (ej. destilación, reflujo):", key="buscador_seider")
    
    if palabra_busqueda:
        with st.spinner('Buscando en el documento...'):
            resultados = buscar_en_pdf("Seider - Capítulo 6.pdf", palabra_busqueda)
            
            if resultados:
                st.write(f"**Se encontraron {len(resultados)} coincidencias para '{palabra_busqueda}':**")
                for res in resultados:
                    with st.expander(f"📄 Página {res['pagina']}"):
                        st.write(f"...{res['contexto']}...")
            else:
                st.warning("No se encontraron coincidencias en este documento.")
    
    st.divider()
    if st.button("← Volver al menú principal"):
        st.session_state.fuente_elegida = None
        st.rerun()

elif st.session_state.fuente_elegida == "Walas":
    st.success("Base de datos seleccionada: 122 - Heurísticas _Walas (2012)")
    st.subheader("Buscador: Heurísticas para Selección de Equipos")
    
    # Buscador para Walas
    palabra_busqueda = st.text_input("🔍 Ingresa una palabra o término (ej. bomba, intercambiador):", key="buscador_walas")
    
    if palabra_busqueda:
        with st.spinner('Buscando en el documento...'):
            resultados = buscar_en_pdf("122 - Heurísticas _Walas (2012).pdf", palabra_busqueda)
            
            if resultados:
                st.write(f"**Se encontraron {len(resultados)} coincidencias para '{palabra_busqueda}':**")
                for res in resultados:
                    with st.expander(f"📄 Página {res['pagina']}"):
                        st.write(f"...{res['contexto']}...")
            else:
                st.warning("No se encontraron coincidencias en este documento.")
    
    st.divider()
    if st.button("← Volver al menú principal"):
        st.session_state.fuente_elegida = None
        st.rerun()
