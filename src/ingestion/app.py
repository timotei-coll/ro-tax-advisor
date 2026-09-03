import streamlit as st
from graph import create_graph

st.set_page_config(
    page_title="RO Tax Advisor",
    page_icon="⚖️",
    layout="centered"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
}

/* Elimină spațiul prea mare de sus */
.block-container {
    padding-top: 3rem;
    max-width: 850px;
}

/* Header */
.header {
    text-align: center;
    margin-bottom: 35px;
}

.logo {
    font-size: 55px;
    margin-bottom: 5px;
}

.title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin: 0;
}

.subtitle {
    color: #94a3b8;
    font-size: 17px;
    margin-top: 8px;
}

/* Input */
.stTextArea textarea {
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    font-size: 16px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #60a5fa !important;
    box-shadow: 0 0 0 1px #60a5fa !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    font-size: 16px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.35);
}

/* Answer */
.answer-box {
    margin-top: 35px;
    padding: 28px;
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid #334155;
    border-radius: 18px;
    color: #e2e8f0;
    animation: appear 0.4s ease;
}

/* Sources */
.sources-title {
    margin-top: 30px;
    color: white;
    font-size: 20px;
    font-weight: 700;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 45px;
    color: #64748b;
    font-size: 13px;
}

/* Animation */
@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">

    <div class="logo">⚖️</div>

    <div class="title">
        RO Tax Advisor
    </div>

    <div class="subtitle">
        Asistent AI pentru Codul fiscal din România
    </div>

</div>
""", unsafe_allow_html=True)


# =========================
# QUESTION
# =========================

question = st.text_area(
    "Întrebarea ta",
    placeholder="Scrie aici întrebarea despre Codul fiscal...",
    height=100,
    label_visibility="visible"
)

st.write("")




# =========================
# BUTTON
# =========================

if st.button("🔍 Caută răspunsul"):


    if not question.strip():

        st.warning("Te rog să introduci o întrebare.")

    else:

        with st.spinner("🤖 Analizez Codul fiscal..."):

            graph = create_graph()

            result = graph.invoke({
                "question": question
            })
            st.markdown("### 📖 Surse")

            for i, chunk in enumerate(result["chunks"], 1):

                metadata = chunk["metadata"]

                article = metadata.get("article", "")
                chapter = metadata.get("chapter", "")
                title = metadata.get("title", "")

                with st.expander(f"📄 Sursa {i} — {article or 'Articol necunoscut'}"):
                    if title:
                        st.write(f"**Titlu:** {title}")

                    if chapter:
                        st.write(f"**Capitol:** {chapter}")

                    if article:
                        st.write(f"**Articol:** {article}")

                    st.write("**Fragment:**")
                    st.write(chunk["text"])


        # =========================
        # ANSWER
        # =========================

        st.markdown(
            '<div class="answer-box">',
            unsafe_allow_html=True
        )

        st.markdown("### 📚 Răspuns")

        st.write(result["answer"])

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# FOOTER
# =========================

st.markdown("""
<div class="footer">
    RO Tax Advisor • Powered by AI & RAG
</div>
""", unsafe_allow_html=True)