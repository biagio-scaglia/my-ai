import streamlit as st
import os
import sys
import gc

# Configurazione Pagina
st.set_page_config(
    page_title="Coddy AI v2.0 (Godmode)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS per look premium
st.markdown(
    """
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput input {
        border-radius: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Importa Engine (Lazy loading gestito da cache_resource)
# Modifica il path per includere la directory corrente
sys.path.append(os.getcwd())


@st.cache_resource(show_spinner="Caricamento Motori Neurali (Dual Brain)...")
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


# Sidebar - Stato Sistema
with st.sidebar:
    st.title("🤖 Coddy Godmode")
    st.markdown("---")
    st.success("⚡ Coder Engine (1.5B): Ready")
    st.success("⚡ Light Engine (0.5B): Ready")
    st.info("📚 RAG Memory: Active")

    # Online Toggle
    enable_online = st.toggle("Ricerca Web (Online)", value=False)

    st.markdown("---")
    if st.button("🧹 Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# Main Interface
st.title("Coddy AI Assistant")
st.caption("🚀 Powered by Llama.cpp & Qdrant | Local Godmode")

# Caricamento Motori
engine, rag = load_engine()

# Inizializza Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ciao! Sono Coddy v2.0. In cosa posso aiutarti oggi?",
        }
    ]

# Render History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Utente
if prompt := st.chat_input("Scrivi qui..."):
    # 1. Aggiungi user msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Logica RAG + Web (Simile a coddy.py)
    context_parts = []

    # RAG Search
    rag_results = rag.search(prompt)
    if rag_results:
        context_parts.append("=== KNOWLEDGE BASE ===")
        for r in rag_results:
            context_parts.append(f"{r['text']}")
        with st.expander(f"📚 RAG Found ({len(rag_results)} frammenti)"):
            for r in rag_results:
                st.text(f"Source: {r['source']}\n{r['text'][:200]}...")

    # Web Search (Se attivo)
    if enable_online:
        from coddy import web_search  # Riutilizzo funzione esistente

        with st.spinner("🌐 Searching Web..."):
            web_results = web_search(prompt)
            if web_results:
                context_parts.append("=== WEB RESULTS ===")
                context_parts.extend(web_results)
                with st.expander("🌐 Web Results"):
                    st.write(web_results)

    # Costruzione Prompt completo
    full_input = prompt
    if context_parts:
        full_input += "\n\n" + "\n".join(context_parts)

    # 3. Generazione Risposta (Streaming)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Routing Dinamico Visuale
        model_type = engine.route_query(full_input)
        if model_type == "coder":
            st.toast("⚡ Switched to **CODER** Brain", icon="🧠")
        else:
            st.toast("⚡ Switched to **LIGHT** Brain", icon="💡")

        # Streaming dal generatore
        # st.write_stream accetta un generatore
        full_response = st.write_stream(
            engine.stream_chat(
                st.session_state.messages[:-1]
                + [{"role": "user", "content": full_input}],
                model_type=model_type,
            )
        )

        # Salva history (usando la risposta completa)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
