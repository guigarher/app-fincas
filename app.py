import streamlit as st
import requests

st.set_page_config(page_title="Gestión de Fincas", layout="wide")

# ──────────────────────────────
# 🔐 DATOS SENSIBLES DESDE SECRETS
TOKEN_BOT = st.secrets["TELEGRAM_BOT_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
TOPIC_ID_1 = st.secrets["TOPIC_ID_1"]  # DataLost
TOPIC_ID_2 = st.secrets["TOPIC_ID_2"]  # Manager
TOPIC_ID_3 = st.secrets["TOPIC_ID_3"]  # Reboots
# ──────────────────────────────

# Lista de fincas disponibles
fincas = [
    "fernando_campos", "la_jaquita", "hoya_grande", "el_jardin", "torretas",
    "las_canas", "la_luz", "la_quinta_3", "majuelos", "carlos_ascanio"
]

# Parámetros configurables con /set
parametros_set = [
    "water_counter", "WD_timeout", "read_interval", "data_count",
    "max_messages", "min_signal", "min_battery"
]

# Sidebar para selección de fincas
st.sidebar.title("🌾 Fincas disponibles")
fincas_seleccionadas = [finca for finca in fincas if st.sidebar.checkbox(finca)]

st.sidebar.subheader("✅ Fincas seleccionadas:")
for finca in fincas_seleccionadas:
    st.sidebar.write(f"🔹 {finca}")

# Función para enviar comandos al bot de Telegram
def enviar_a_telegram(comando_texto):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": comando_texto
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        st.success(f"✅ Comando enviado: {comando_texto}")
    else:
        st.error("❌ Error al enviar a Telegram. Revisa el TOKEN o CHAT_ID.")

# Función para construir y enviar el comando
def ejecutar_comando(comando, extra_param=""):
    if not fincas_seleccionadas:
        st.warning("⚠️ Selecciona al menos una finca.")
        return
    for finca in fincas_seleccionadas:
        comando_final = f"/{comando} {finca}"
        if extra_param:
            comando_final += f" {extra_param}"
        st.code(comando_final)
        enviar_a_telegram(comando_final)

# Título principal
st.markdown("<h1 style='text-align: center;'>🔧 Comandos disponibles</h1>", unsafe_allow_html=True)

# Columnas principales
col1, col2, col3 = st.columns(3)

# Comandos simples
with col1:
    st.subheader("📦 Comandos directos")
    if st.button("🟢 /get"):
        ejecutar_comando("get")
    if st.button("🔄 /reboot"):
        ejecutar_comando("reboot")
    if st.button("📱 /sim"):
        ejecutar_comando("sim")
    if st.button("📊 /status"):
        ejecutar_comando("status")
    if st.button("📥 /latest"):
        ejecutar_comando("latest")

# Comando /sleep
with col2:
    st.subheader("😴 Comando /sleep")
    tiempo = st.number_input("Duración en segundos", min_value=1, max_value=3600, step=1, value=60)
    if st.button("💤 Ejecutar /sleep"):
        ejecutar_comando("sleep", str(tiempo))

# Comando /set
with col3:
    st.subheader("⚙️ Comando /set")
    parametros_seleccionados = st.multiselect("Parámetros a configurar", parametros_set)
    valores_parametros = {}

    for param in parametros_seleccionados:
        valor = st.number_input(f"Valor para {param}:", min_value=0, step=1, key=param)
        valores_parametros[param] = valor

    if st.button("⚙️ Ejecutar /set"):
        if not valores_parametros:
            st.warning("⚠️ Introduce al menos un valor.")
        else:
            extras = ",".join([f"{k}_value={v}" for k, v in valores_parametros.items()])
            ejecutar_comando("set", extras)
