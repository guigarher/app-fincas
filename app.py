import streamlit as st
import requests

# Configuración de la app
st.set_page_config(page_title="Gestión de Fincas", layout="wide")

# Cargar la URL de Node-RED desde secrets
NODE_RED_URL = st.secrets["NODE_RED_URL"]

# Lista de fincas
fincas = [
    "fernando_campos", "la_jaquita", "hoya_grande", "el_jardin", "torretas",
    "las_canas", "la_luz", "la_quinta_3", "majuelos", "carlos_ascanio"
]

# Parámetros posibles para /set
parametros_set = [
    "water_counter", "WD_timeout", "read_interval", "data_count",
    "max_messages", "min_signal", "min_battery"
]

# Sidebar: selección de fincas
st.sidebar.title("🌾 Fincas disponibles")
fincas_seleccionadas = [
    finca for finca in fincas if st.sidebar.checkbox(finca, key=f"check_{finca}")
]

st.sidebar.subheader("✅ Fincas seleccionadas:")
for finca in fincas_seleccionadas:
    st.sidebar.markdown(f"- {finca}")

# Función para enviar comando a Node-RED
def enviar_a_node_red(comando):
    payload = {"content": comando}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(NODE_RED_URL, json=payload, headers=headers)
        return response.text if response.status_code == 200 else f"❌ Error {response.status_code}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Variables para almacenar respuestas a mostrar en col2
respuestas_pendientes = []

# Título principal
st.markdown("<h1 style='text-align: center;'>🔧 Comandos disponibles</h1>", unsafe_allow_html=True)

# Dividir en columnas
col1, col2, col3 = st.columns(3)

# Columna 1: comandos directos
with col1:
    st.subheader("📦 Comandos directos")

    if st.button("🟢 Ejecutar /get"):
        if not fincas_seleccionadas:
            st.warning("Selecciona al menos una finca.")
        else:
            for finca in fincas_seleccionadas:
                comando = f"/get {finca}"
                respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

    if st.button("🔄 Ejecutar /reboot"):
        for finca in fincas_seleccionadas:
            comando = f"/reboot {finca}"
            respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

    if st.button("📱 Ejecutar /sim"):
        for finca in fincas_seleccionadas:
            comando = f"/sim {finca}"
            respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

    if st.button("📊 Ejecutar /status"):
        for finca in fincas_seleccionadas:
            comando = f"/status {finca}"
            respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

    if st.button("📥 Ejecutar /latest"):
        for finca in fincas_seleccionadas:
            comando = f"/latest {finca}"
            respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

# Columna 2: comando /sleep + mostrar todas las respuestas acumuladas
with col2:
    st.subheader("😴 Comando /sleep")
    tiempo = st.number_input("Duración (segundos)", min_value=1, max_value=3600, step=1, value=60)

    if st.button("💤 Ejecutar /sleep"):
        for finca in fincas_seleccionadas:
            comando = f"/sleep {finca} {tiempo}"
            respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

    if respuestas_pendientes:
        st.subheader("📋 Respuestas de comandos enviados")
        for i, (comando, respuesta) in enumerate(respuestas_pendientes):
            st.markdown(f"**{comando}**")
            st.text_area("Respuesta", respuesta, height=100, key=f"respuesta_{i}")

# Columna 3: comando /set
with col3:
    st.subheader("⚙️ Comando /set")

    parametros_seleccionados = st.multiselect("Selecciona parámetros", parametros_set)
    valores_parametros = {}

    for param in parametros_seleccionados:
        valor = st.number_input(f"Valor para {param}", min_value=0, step=1, key=f"valor_{param}")
        valores_parametros[param] = valor

    if st.button("⚙️ Ejecutar /set"):
        if not fincas_seleccionadas:
            st.warning("Selecciona al menos una finca.")
        elif not valores_parametros:
            st.warning("Introduce al menos un parámetro con valor.")
        else:
            extras = ",".join([f"{k}={v}" for k, v in valores_parametros.items()])
            for finca in fincas_seleccionadas:
                comando = f"/set {finca} {extras}"
                respuestas_pendientes.append((comando, enviar_a_node_red(comando)))

