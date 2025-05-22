import streamlit as st
import requests

# Configuración de la app
st.set_page_config(page_title="Gestión de Fincas", layout="wide")

# Cargar datos desde secrets
NODE_RED_URL = st.secrets["NODE_RED_URL"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

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
        if response.status_code == 200:
            return response.text
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Función para avisar por Telegram que se ha lanzado un comando desde la app
def notificar_telegram(comando):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"📡 Comando enviado desde la app Streamlit:\n\n{comando}"
    }
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error enviando notificación a Telegram: {e}")
        return False

# Prueba de conexión (visible en la interfaz)
st.caption(f"🌐 Verificando conexión con Node-RED: {NODE_RED_URL}")
try:
    test_response = requests.post(NODE_RED_URL, json={"content": "/test"})
    st.success(f"✅ Node-RED responde: {test_response.status_code}")
except Exception as e:
    st.error(f"❌ No se pudo conectar con Node-RED: {e}")

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
                st.code(comando)
                enviar_a_node_red(comando)
                notificar_telegram(comando)

    if st.button("🔄 Ejecutar /reboot"):
        for finca in fincas_seleccionadas:
            comando = f"/reboot {finca}"
            st.code(comando)
            enviar_a_node_red(comando)
            notificar_telegram(comando)

    if st.button("📱 Ejecutar /sim"):
        for finca in fincas_seleccionadas:
            comando = f"/sim {finca}"
            st.code(comando)
            enviar_a_node_red(comando)
            notificar_telegram(comando)

    if st.button("📊 Ejecutar /status"):
        for finca in fincas_seleccionadas:
            comando = f"/status {finca}"
            st.code(comando)
            enviar_a_node_red(comando)
            notificar_telegram(comando)

    if st.button("📥 Ejecutar /latest"):
        for finca in fincas_seleccionadas:
            comando = f"/latest {finca}"
            st.code(comando)
            enviar_a_node_red(comando)
            notificar_telegram(comando)

# Columna 2: comando /sleep
with col2:
    st.subheader("😴 Comando /sleep")
    tiempo = st.number_input("Duración (segundos)", min_value=1, max_value=3600, step=1, value=60)

    if st.button("💤 Ejecutar /sleep"):
        for finca in fincas_seleccionadas:
            comando = f"/sleep {finca} {tiempo}"
            st.code(comando)
            enviar_a_node_red(comando)
            notificar_telegram(comando)

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
                st.code(comando)
                enviar_a_node_red(comando)
                notificar_telegram(comando)



