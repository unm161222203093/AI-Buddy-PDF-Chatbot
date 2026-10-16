import streamlit as st
import chromadb
import ollama
from pypdf import PdfReader
import hashlib
import html

st.set_page_config(
    page_title="AI BUDDY",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------

st.markdown("""
<style>
.stApp {
    background: #F5F7FF;
    color: #172554;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E0E7FF, #F3E8FF);
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172554 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF !important;
    color: #172554 !important;
    border: 1px solid #C7D2FE !important;
    border-radius: 12px !important;
    min-height: 45px !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] .stButton > button p {
    color: #172554 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #C7D2FE !important;
    border-color: #818CF8 !important;
}

/* Welcome banner */
.hero {
    background: linear-gradient(115deg, #E0E7FF, #DBF4FF);
    padding: 38px 35px;
    border-radius: 24px;
    border: 1px solid #C7D2FE;
    margin: 12px 0 24px 0;
}

.hero h1 {
    color: #172554 !important;
    font-size: 36px;
    margin-bottom: 12px;
}

.hero h2 {
    color: #273C75 !important;
}

.hero p {
    color: #334155 !important;
    font-size: 17px;
    line-height: 1.7;
}

.eyebrow {
    color: #4338CA !important;
    font-weight: 700;
    font-size: 14px !important;
}

/* Feature cards */
.feature {
    background: #FFFFFF;
    padding: 23px 15px;
    border-radius: 18px;
    border: 1px solid #DDE4F5;
    min-height: 170px;
    text-align: center;
}

.feature h3 {
    font-size: 18px;
    color: #172554 !important;
}

.feature p {
    font-size: 14px;
    color: #475569 !important;
}

/* Getting started panel */
.info-panel {
    background: #E0E7FF;
    color: #172554 !important;
    border-radius: 18px;
    padding: 22px;
    margin-top: 22px;
}

.info-panel h3,
.info-panel p {
    color: #172554 !important;
}

/* Main buttons */
.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 600;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    color: #172554;
    border: 1px solid #DDE4F5;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)


# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection" not in st.session_state:
    st.session_state.collection = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""

if "client" not in st.session_state:
    st.session_state.client = chromadb.Client()

def go(page):
    st.session_state.page = page

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 📚AI BUDDY")
    st.caption("PDF Based Chatbot")
    st.divider()

    pages = [
        ("🏠", "Home"),
        ("➕", "New Chat"),
        ("◷", "History"),
        ("📁", "Project"),
        ("📄", "Resume"),
        ("🔎", "Research")
    ]

    for icon, page_name in pages:
        if st.button(
            f"{icon}   {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True
        ):
            if page_name == "New Chat":
                st.session_state.messages = []
                st.session_state.page = "Chat"
            else:
                go(page_name)

    st.markdown("---")
    st.markdown("### 👤 Keerthana")
    st.caption("Your personal PDF assistant")

# ---------- HOME ----------
if st.session_state.page == "Home":
    st.markdown("""
    <div class="hero">
        <p class="eyebrow">WELCOME TO AI BUDDY</p>
        <h1>Hello Keerthana 👋</h1>
        <h2>Welcome to your PDF assistant</h2>
        <p>Turn your documents into conversations.
        Upload a PDF, ask questions, and get clear answers
        from the information in your document.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        if st.button(
            "📤  Upload PDF & Start",
            type="primary",
            use_container_width=True
        ):
            go("Chat")
            st.rerun()

    with right:
        if st.button("💬  Go to Chat", use_container_width=True):
            go("Chat")
            st.rerun()

    st.markdown("## ✨ What you can do")

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (c1, "📄", "Upload Any PDF",
         "Upload a PDF document to get started."),
        (c2, "🔍", "Smart Retrieval",
         "ChromaDB finds relevant document text."),
        (c3, "🧠", "Powerful AI",
         "Ollama generates answers from your PDF."),
        (c4, "⚡", "Quick Answers",
         "Receive concise answers up to 500 characters.")
    ]

    for col, icon, title, description in cards:
        with col:
            st.markdown(
                f'<div class="feature"><div style="font-size:32px">'
                f'{icon}</div><h3>{title}</h3>'
                f'<p>{description}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("""
    <div class="info-panel">
        <h3>🚀 How to get started</h3>
        <p>✅ Upload your PDF document</p>
        <p>✅ Click Process PDF</p>
        <p>✅ Ask questions about the content</p>
        <p>✅ Get relevant answers, up to 500 characters</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- CHAT PAGE ----------
elif st.session_state.page == "Chat":
    st.title("💬 Chat with your PDF")
    st.caption("Upload a document, process it, and ask questions.")

    uploaded = st.file_uploader(
        "Choose your PDF file",
        type=["pdf"],
        key="pdf_upload"
    )

    if uploaded and st.button("⚙️ Process PDF", type="primary"):
        try:
            with st.spinner("Reading PDF and creating embeddings..."):
                reader = PdfReader(uploaded)
                text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

                if not text.strip():
                    st.error(
                        "No readable text found. "
                        "This PDF may need OCR."
                    )
                else:
                    chunks = [
                        text[i:i + 1000]
                        for i in range(0, len(text), 800)
                        if text[i:i + 1000].strip()
                    ]

                    digest = hashlib.sha256(
                        uploaded.getvalue()
                    ).hexdigest()[:16]

                    collection_name = "pdf_" + digest

                    client = st.session_state.client

                    try:
                        client.delete_collection(collection_name)
                    except Exception:
                        pass

                    collection = client.create_collection(
                        name=collection_name
                    )

                    batch_size = 20

                    for start in range(0, len(chunks), batch_size):
                        batch = chunks[start:start + batch_size]

                        result = ollama.embed(
                            model="nomic-embed-text",
                            input=batch
                        )

                        collection.add(
                            ids=[
                                f"chunk_{i}"
                                for i in range(start, start + len(batch))
                            ],
                            documents=batch,
                            embeddings=result["embeddings"]
                        )

                    st.session_state.collection = collection
                    st.session_state.pdf_name = uploaded.name
                    st.session_state.messages = []

                    st.success(
                        f"Successfully processed: {uploaded.name}"
                    )

        except Exception as e:
            st.error(f"PDF processing failed: {e}")

    if st.session_state.collection is not None:
        st.info(f"📄 Current document: {st.session_state.pdf_name}")

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask anything about your PDF...")

    if question:
        if st.session_state.collection is None:
            st.warning("Please upload and process a PDF first.")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Finding the answer..."):
                        embedding_result = ollama.embed(
                            model="nomic-embed-text",
                            input=question
                        )

                        collection = st.session_state.collection

                        results = collection.query(
                            query_embeddings=embedding_result["embeddings"],
                            n_results=min(3, collection.count())
                        )

                        docs = results.get("documents", [[]])[0]
                        context = "\n\n".join(docs)

                        response = ollama.chat(
                            model="llama3.2",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "Answer using only the supplied PDF "
                                        "context. Give a useful, clear answer "
                                        "and explain the main points. "
                                        "Never exceed 500 characters. "
                                        "If the answer is missing from the "
                                        "context, say the PDF does not contain "
                                        "enough information."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": (
                                        f"PDF context:\n{context}\n\n"
                                        f"Question: {question}"
                                    )
                                }
                            ]
                        )

                        answer = response["message"]["content"].strip()
                        answer = answer[:500].rstrip()

                        st.markdown(answer)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                except Exception as e:
                    st.error(f"Answer generation failed: {e}")

# ---------- OTHER SIDEBAR PAGES ----------
elif st.session_state.page == "History":
    st.title("◷ Chat History")
    if st.session_state.messages:
        for message in st.session_state.messages:
            st.write(f"**{message['role'].title()}:** {message['content']}")
    else:
        st.info("No messages in this session yet.")

elif st.session_state.page == "Project":
    st.title("📁 Project")
    st.write("Your PDF-based question-answering project.")
    st.write("Technology: Python, Streamlit, ChromaDB and Ollama.")

elif st.session_state.page == "Resume":
    st.title("📄 Resume")
    st.write("Upload a resume PDF in the Chat page to ask questions about it.")

elif st.session_state.page == "Research":
    st.title("🔎 Research")
    st.write("Upload a research paper PDF in the Chat page to explore its content.")
