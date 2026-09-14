import streamlit as st

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
        # Botón para Seider
        if st.button("Heurísticas de Seider", use_container_width=True):
            st.session_state.fuente_elegida = "Seider"
            st.rerun()
            
    with col2:
        # Botón para Walas
        if st.button("Heurísticas de Walas", use_container_width=True):
            st.session_state.fuente_elegida = "Walas"
            st.rerun()

# 3. Flujo de ejecución principal según la elección del usuario
if st.session_state.fuente_elegida == "Seider":
    st.success("Cargando base de datos: Seider - Capítulo 6.pdf")
    st.subheader("Heurísticas para la Síntesis de Procesos (Seider)")
    
    # Aquí puedes integrar tu lógica de procesamiento (RAG, lectura de PDF, Firestore, etc.)
    st.info("Espacio para insertar el código de lectura/consulta del documento de Seider.")
    
    st.divider()
    if st.button("← Volver al menú principal"):
        st.session_state.fuente_elegida = None
        st.rerun()

elif st.session_state.fuente_elegida == "Walas":
    st.success("Cargando base de datos: 122 - Heurísticas _Walas (2012).pdf")
    st.subheader("Heurísticas para Selección de Equipos (Walas)")
    
    # Aquí puedes integrar tu lógica de procesamiento (RAG, lectura de PDF, Firestore, etc.)
    st.info("Espacio para insertar el código de lectura/consulta del documento de Walas.")
    
    st.divider()
    if st.button("← Volver al menú principal"):
        st.session_state.fuente_elegida = None
        st.rerun()
