import sys
import os
import streamlit as st

# Patch per Windows Error 6 su shutdown (Streamlit/Colorama issue)
if sys.platform == "win32":
    import colorama

    colorama.init(strip=False)

# Configurazione Pagina
st.set_page_config(
    page_title="Coddy AI v2.0",
    page_icon="⚡",  # Icona tab
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS per look premium (Dark Mode friendly)
st.markdown(
    """
<style>
    /* Nasconde menu hamburger e footer standard */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} /* Nasconde barra colorata in alto */
    
    /* Stile Chat Message per renderlo più "App Native" */
    .stChatMessage {
        background-color: #262730;
        border-radius: 12px;
        border: 1px solid #3E3E3E;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1E1E1E;
    }
    
    /* Input field più pulito */
    .stTextInput input {
        border-radius: 12px;
        background-color: #2D2D2D;
        color: #E0E0E0;
        border: 1px solid #444;
    }
    
    /* Sidebar scura */
    section[data-testid="stSidebar"] {
        background-color: #0E1117;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Importa Engine (Lazy loading gestito da cache_resource)
sys.path.append(os.getcwd())


@st.cache_resource(show_spinner="Booting Neural Core (1.5B Parameters)...")
def load_engine():
    """
    Carica i modelli una volta sola e li mantiene in RAM.
    """
    # Silenzia stdout durante importazione per pulizia CLI
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    try:
        from engine_cpp import CoddyEngine2
        from rag_engine import RagEngine

        # Init RAG
        rag = RagEngine()

        # Init Engine
        engine = CoddyEngine2()
        engine.start()
    finally:
        sys.stdout = original_stdout

    return engine, rag


# Layout Sidebar - Monitoraggio
with st.sidebar:
    st.header("🔮 System Status")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Thinker", value="ON", delta="1.5B")
    with col2:
        st.metric(label="Speed", value="ON", delta="0.5B")

    st.caption("🧠 RAG Memory: Active")

    st.divider()

    st.subheader("Configuration")
    enable_online = st.checkbox("Web Access", value=False)

    st.divider()
    if st.button("Reset Session", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main Interface
st.title("Coddy Assistant")
st.caption("Advanced Local Intelligence")

# Caricamento Motori
engine, rag = load_engine()

# Inizializza Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sistema operativo. Attendo istruzioni."}
    ]

# Render History
for msg in st.session_state.messages:
    # Usa icone di default (SVG Streamlit) che sono molto più belle delle emoji
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Utente
if prompt := st.chat_input("Digita una richiesta..."):
    # 1. Aggiungi user msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Logica RAG + Web
    context_parts = []

    # RAG Search
    rag_results = rag.search(prompt)
    if rag_results:
        context_parts.append("=== KNOWLEDGE BASE ===")
        for r in rag_results:
            context_parts.append(f"{r['text']}")

        with st.status(
            f"Analisi Memoria ({len(rag_results)} found)", expanded=False
        ) as status:
            for r in rag_results:
                st.caption(f"📄 {r['source']}")
                st.code(r["text"][:200])

    # Web Search
    if enable_online:
        from coddy import web_search

        with st.status("Analisi Web...", expanded=False):
            web_results = web_search(prompt)
            if web_results:
                context_parts.append("=== WEB RESULTS ===")
                context_parts.extend(web_results)
                st.write(web_results)

    # Costruzione Prompt
    full_input = prompt
    if context_parts:
        full_input += "\n\n" + "\n".join(context_parts)

    # 3. Generazione (Streaming)
    with st.chat_message("assistant"):
        full_response = ""

        # Routing Dinamico
        model_type = engine.route_query(full_input)

        # Indicatore Modello (Minimale)
        if model_type == "coder":
            st.caption("_Thinking with Coder Core_")
        else:
            st.caption("_Quick Reply via Light Core_")

        # Streaming
        full_response = st.write_stream(
            engine.stream_chat(
                st.session_state.messages[:-1]
                + [{"role": "user", "content": full_input}],
                model_type=model_type,
            )
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
