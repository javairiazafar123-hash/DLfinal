
import streamlit as st
import os
import tempfile
from rag_pipeline import RAGPipeline

st.set_page_config(page_title="RAG PDF Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 RAG PDF Chatbot")
st.markdown("Ask questions about your uploaded PDFs")

# Initialize session state
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store_ready" not in st.session_state:
    st.session_state.vector_store_ready = False

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    chunk_size = st.slider("Chunk Size", 256, 1024, 512)
    top_k = st.slider("Retrieve Top-K", 1, 10, 3)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

    st.subheader("📁 Upload PDFs")
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files and st.button("🚀 Process PDFs"):
        with st.spinner("Processing..."):
            st.session_state.rag_pipeline = RAGPipeline(
                api_key=api_key, chunk_size=chunk_size, top_k=top_k
            )

            pdf_paths = []
            with tempfile.TemporaryDirectory() as tmpdir:
                for file in uploaded_files:
                    path = os.path.join(tmpdir, file.name)
                    with open(path, "wb") as f:
                        f.write(file.getbuffer())
                    pdf_paths.append(path)

                st.session_state.rag_pipeline.build_vector_store(pdf_paths)

            st.session_state.vector_store_ready = True
            st.success("✅ PDFs processed!")

# Main chat interface
if not st.session_state.vector_store_ready:
    st.warning("⬅️ Upload PDFs to get started")
else:
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.write(f"**You:** {msg['content']}")
        else:
            st.write(f"**Assistant:** {msg['content']}")

    # Chat input
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        user_input = st.text_input("Ask a question:")
    with col2:
        send = st.button("Send")

    if send and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Generating response..."):
            answer, sources = st.session_state.rag_pipeline.query(user_input, temperature)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.write(f"**Assistant:** {answer}")

            if sources:
                st.markdown("### 📚 Sources")
                for src, content in sources:
                    st.write(f"*{src}*: {content}...")
