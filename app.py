import streamlit as st
import os
import sys
import gc

# Configurazione Pagina
st.set_page_config(
    page_title="Coddy AI v2.0",
    page_icon="💻",
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
    
    /* Stile Chat Message */
    .stChatMessage {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    
    /* Stile Input */
    .stTextInput input {
        border-radius: 20px;
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #444;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111;
    }
    
    /* Titoli */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Importa Engine (Lazy loading gestito da cache_resource)
sys.path.append(os.getcwd())


@st.cache_resource(
    show_spinner="Inizializzazione Core C++ (Coder 1.5B + Light 0.5B)..."
)
def load_engine():
    """
    Carica i modelli una volta sola e li mantiene in RAM.
    """
    from engine_cpp import CoddyEngine2
    from rag_engine import RagEngine

    # Init RAG
    rag = RagEngine()

    # Init Engine
    engine = CoddyEngine2()
    engine.start()

    return engine, rag


# Layout Sidebar - Monitoraggio
with st.sidebar:
    st.header("System Status")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Coder Core", value="Active", delta="On")
    with col2:
        st.metric(label="Light Core", value="Active", delta="On")

    st.info("RAG Memory: Connected")

    st.subheader("Settings")
    enable_online = st.toggle("Web Search Access", value=False)

    st.markdown("---")
    if st.button("Clear Context", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main Interface
st.title("Coddy AI")
st.markdown("##### Assistant for Advanced Programming")

# Caricamento Motori
engine, rag = load_engine()

# Inizializza Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sistema online. Pronto per il coding."}
    ]

# Render History
for msg in st.session_state.messages:
    # Icone personalizzate
    avatar = "💻" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Input Utente
if prompt := st.chat_input("Inserisci comando o query..."):
    # 1. Aggiungi user msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Logica RAG + Web (Simile a coddy.py)
    context_parts = []

    # RAG Search
    rag_results = rag.search(prompt)
    if rag_results:
        context_parts.append("=== KNOWLEDGE BASE ===")
        for r in rag_results:
            context_parts.append(f"{r['text']}")

        # Feedback RAG discreto
        with st.status(
            f"Consultazione Memoria ({len(rag_results)} ref)", expanded=False
        ) as status:
            for r in rag_results:
                st.caption(f"Source: {r['source']}")
                st.code(r["text"][:200])

    # Web Search (Se attivo)
    if enable_online:
        from coddy import web_search

        with st.status("Ricerca Web in corso...", expanded=False):
            web_results = web_search(prompt)
            if web_results:
                context_parts.append("=== WEB RESULTS ===")
                context_parts.extend(web_results)
                st.write(web_results)

    # Costruzione Prompt completo
    full_input = prompt
    if context_parts:
        full_input += "\n\n" + "\n".join(context_parts)

    # 3. Generazione Risposta (Streaming)
    with st.chat_message("assistant", avatar="💻"):
        full_response = ""

        # Routing Dinamico Visuale
        model_type = engine.route_query(full_input)

        # Badge del modello usato (piccolo e discreto)
        if model_type == "coder":
            st.caption("⚡ Engine: Coder Pro")
        else:
            st.caption("⚡ Engine: Light Speed")

        # Streaming
        full_response = st.write_stream(
            engine.stream_chat(
                st.session_state.messages[:-1]
                + [{"role": "user", "content": full_input}],
                model_type=model_type,
            )
        )

        # Salva history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
