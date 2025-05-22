import streamlit as st
import requests

st.set_page_config(page_title="Gestión de Fincas", layout="wide")

# ──────────────────────────────────────────────
# 🔐 SECRETS NECESARIOS
NODE_RED_URL = st.secrets["NODE_RED_URL"]
# ──────────────────────────────────────────────

# Lista de fincas disponibles
fincas = [
    "fernando_campos", "la_jaquita", "hoya_grande", "el_jardin", "torretas",
    "las_canas", "la_luz", "la_quinta_3", "majuelos", "carlos_ascanio"
]

parametros_set = [
    "water_counter", "WD_timeout", "read_interval", "data_count",
    "max_messages", "min_signal", "min_battery"
]

# ─────────────── INTERFAZ LATERAL ─────────────── #
st.sidebar.title("🌾 Fincas disponibles")
fincas_seleccionadas = [
    f for f in fincas if st.sidebar.checkbox(f, key=f"checkbox_{f}")
]

st.sidebar.subheader("✅ Fincas seleccionadas:")
for finca in fincas_seleccionadas:
    st.sidebar.write(f"🔹 {finca}")

# ─────────────── FUNCIONES ─────────────── #
def enviar_a_node_red(comando_texto):
    """Envía un comando al backend Node-RED como contenido JSON."""
    payload = { "content": comando_texto }
    headers = { "Content-Type": "application/json" }

    try:
        response = requests.post(NODE_RED_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            st.error(f"❌ Error al enviar a Node-RED: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ Excepción al conectar con Node-RED: {str(e)}")
        return False

def consultar_estado_finca(finca):
    """Envía un comando /get y devuelve respuesta (texto plano o JSON)."""
    comando_final = f"/get {finca}"
    payload = { "content": comando_final }
    headers = { "Content-Type": "application/json" }

    try:
        response = requests.post(NODE_RED_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return f"❌ Error al consultar {finca}: {response.status_code}"
    except Exception as e:
        return f"❌ Excepción: {str(e)}"

def ejecutar_comando_simple(comando, extra_param=""):
    """Construye y envía el comando sin mostrar respuesta."""
    if not fincas_seleccionadas:
        st.warning("⚠️ Selecciona al menos una finca.")
        return

    for finca in fincas_seleccionadas:
        comando_final = f"/{comando} {finca}"
        if extra_param:
            comando_final += f" {extra_param}"
        st.code(comando_final)
        ok = enviar_a_node_red(comando_final)
        if ok:
            st.success(f"✅ Comando enviado: {comando_final}")

# ─────────────── SECCIÓN PRINCIPAL ─────────────── #
st.markdown("<h1 style='text-align: center;'>🔧 Comandos disponibles</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# 📦 Columna 1: Comandos directos
with col1:
    st.subheader("📦 Comandos directos")

    if st.button("🟢 /get"):
        if not fincas_seleccionadas:
            st.warning("⚠️ Selecciona al menos una finca.")
        for finca in fincas_seleccionadas:
            comando = f"/get {finca}"
            st.code(comando)
            ok = enviar_a_node_red(comando)
            if ok:
                respuesta = consultar_estado_finca(finca)
                st.markdown(f"**📡 Respuesta de `{finca}`:**")
                st.text_area("Contenido", respuesta, height=100)

    if st.button("🔄 /reboot"):
        ejecutar_comando_simple("reboot")

    if st.button("📱 /sim"):
        ejecutar_comando_simple("sim")

    if st.button("📊 /status"):
        ejecutar_comando_simple("status")

    if st.button("📥 /latest"):
        ejecutar_comando_simple("latest")

# 😴 Columna 2: sleep
with col2:
    st.subheader("😴 Comando /sleep")
    tiempo = st.number_input("Duración en segundos", min_value=1, max_value=3600, step=1, value=60)
    if st.button("💤 Ejecutar /sleep"):
        ejecutar_comando_simple("sleep", str(tiempo))

# ⚙️ Columna 3: set
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
            extras = ",".join([f"{k}={v}" for k, v in valores_parametros.items()])
            ejecutar_comando_simple("set", extras)


