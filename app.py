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

# Custom CSS per look premium (Dark Mode friendly) & Sidebar Fix
st.markdown(
    """
<style>
    /* RESET BASE */
    .stApp {
        background-color: #0E1117;
    }
    
    /* HEADER & SIDEBAR FIX */
    /* Non nascondiamo più l'header globale per permettere l'uso dell'hamburger menu */
    header[data-testid="stHeader"] {
        background: transparent;
        z-index: 100;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22; /* Github Dark Dimmed Style */
        border-right: 1px solid #30363D;
    }
    
    /* CHAT MESSAGES REDESIGN */
    .stChatMessage {
        background-color: transparent;
        border: none;
    }
    
    /* User Message Bubble */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
        background-color: #238636; /* Green accent */
        color: white;
        padding: 15px;
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: right;
        margin-left: 20%;
    }
    
    /* AI Message Bubble */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
        background-color: #1F2428; /* Dark card */
        color: #E6EDF3;
        padding: 15px;
        border-radius: 20px 20px 20px 5px;
        border: 1px solid #30363D;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-right: 10%;
    }
    
    /* INPUT FIELD FLOATING */
    .stTextInput {
        position: fixed;
        bottom: 30px;
        left: 50%; 
        transform: translateX(-50%);
        width: 80%; /* Mobile width */
        max-width: 800px;
        z-index: 999;
    }
    
    /* Adjust input styling */
    .stTextInput input {
        background-color: #0D1117;
        color: #C9D1D9;
        border-radius: 25px;
        border: 1px solid #30363D;
        padding: 10px 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* HIDE DEFAULT ELEMENTS (Footer only) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* RESPONSIVE TWEAKS */
    @media (min-width: 768px) {
        .stTextInput {
            width: 60%;
        }
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
    sys.stdout = open(os.devnull, "w", encoding="utf-8")

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
    st.image(
        "https://img.icons8.com/3d-fluency/94/brain.png", width=60
    )  # Placeholder Icon
    st.title("Coddy AI")
    st.caption("v2.1 Godmode Enhanced")

    st.divider()

    with st.expander("⚡ System Status", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Thinker", "ON", delta="1.5B", delta_color="normal")
        with col2:
            st.metric("Speed", "ON", delta="0.5B", delta_color="normal")
        st.progress(100, "Neural Mesh Active")

    st.divider()

    st.subheader("Control Center")
    enable_online = st.toggle("🌍 Web Access", value=False)

    st.divider()

    # Bottom Action
    if st.button("🗑️ Clear Chat", type="primary", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Riavvio sistema completato. Attendo input.",
            }
        ]
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
        # Streaming manuale per gestire interruzioni (Stop button)
        placeholder = st.empty()
        full_response = ""

        try:
            stream = engine.stream_chat(
                st.session_state.messages[:-1]
                + [{"role": "user", "content": full_input}],
                model_type=model_type,
            )

            for chunk in stream:
                full_response += chunk
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception:
            # Caso interruzione utente o errore
            pass

        finally:
            # Salvataggio garantito anche se interrotto
            if full_response:
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            else:
                # Se non ha generato nulla (crash immediato?), puliamo il placeholder
                placeholder.empty()
