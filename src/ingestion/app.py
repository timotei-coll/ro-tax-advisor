
import streamlit as st
from graph import create_graph
from history import init_database, save_history


# =========================
# CONFIGURARE PAGINĂ
# =========================

st.set_page_config(
    page_title="RO Tax Advisor",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_database()


# =========================
# CSS
# =========================

st.markdown("""
<style>

/* =========================
   PAGINA
   ========================= */

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(37, 99, 235, 0.18), transparent 30%),
        radial-gradient(circle at 80% 20%, rgba(79, 70, 229, 0.15), transparent 30%),
        linear-gradient(135deg, #0b1120 0%, #0f172a 50%, #172554 100%);
    min-height: 100vh;
}


/* =========================
   CONTAINER
   ========================= */

.block-container {
    max-width: 850px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}


/* =========================
   HEADER
   ========================= */

.header {
    text-align: center;
    margin-bottom: 2.5rem;
}

.logo {
    width: 76px;
    height: 76px;
    margin: 0 auto 18px auto;
    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 22px;

    font-size: 42px;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.25),
        inset 0 0 20px rgba(96, 165, 250, 0.05);
}

.title {
    color: #f8fafc;
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 10px;
}

.subtitle {
    color: #94a3b8;
    font-size: 17px;
    line-height: 1.5;
}


/* =========================
   ISTORIC
   ========================= */

.history-button {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 18px;
}


/* =========================
   ZONA ÎNTREBĂRII
   ========================= */

.question-card {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 20px;
    padding: 24px;

    box-shadow:
        0 15px 40px rgba(0, 0, 0, 0.20),
        inset 0 1px 0 rgba(255, 255, 255, 0.03);

    margin-bottom: 18px;
}

.question-label {
    color: #e2e8f0;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
}


/* =========================
   TEXTAREA
   ========================= */

.stTextArea textarea {
    background: rgba(30, 41, 59, 0.90) !important;
    color: #f8fafc !important;

    border: 1px solid #334155 !important;
    border-radius: 14px !important;

    font-size: 16px !important;
    line-height: 1.5 !important;

    padding: 14px !important;
}

.stTextArea textarea::placeholder {
    color: #64748b !important;
}

.stTextArea textarea:focus {
    border: 1px solid #60a5fa !important;

    box-shadow:
        0 0 0 1px #60a5fa,
        0 0 25px rgba(37, 99, 235, 0.12) !important;
}


/* =========================
   BUTOANE
   ========================= */

.stButton > button {
    width: 100%;
    min-height: 48px;

    border-radius: 14px;
    border: 1px solid rgba(96, 165, 250, 0.25);

    background: linear-gradient(
        90deg,
        #2563eb,
        #4f46e5
    );

    color: white;

    font-size: 16px;
    font-weight: 700;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        opacity 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 30px rgba(37, 99, 235, 0.30);

    border-color: rgba(147, 197, 253, 0.45);
}

.stButton > button:active {
    transform: translateY(0);
}


/* =========================
   BUTON ISTORIC
   ========================= */

.history-button + div .stButton > button {
    background: rgba(30, 41, 59, 0.75);
    border: 1px solid #334155;
}

.history-button + div .stButton > button:hover {
    background: rgba(51, 65, 85, 0.90);
}


/* =========================
   RĂSPUNS
   ========================= */

.answer-box {
    margin-top: 32px;
    padding: 28px;

    background: rgba(15, 23, 42, 0.78);

    border: 1px solid rgba(96, 165, 250, 0.20);
    border-left: 4px solid #3b82f6;

    border-radius: 18px;

    color: #e2e8f0;

    box-shadow:
        0 15px 40px rgba(0, 0, 0, 0.20);

    animation: appear 0.35s ease;
}

.answer-title {
    color: #f8fafc;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 16px;
}


/* =========================
   SURSE
   ========================= */

.sources-title {
    color: #f8fafc;
    font-size: 21px;
    font-weight: 750;

    margin-top: 32px;
    margin-bottom: 14px;
}

.streamlit-expanderHeader {
    background: rgba(30, 41, 59, 0.70) !important;
    border-radius: 12px !important;
}

.streamlit-expanderContent {
    background: rgba(15, 23, 42, 0.65) !important;
}


/* =========================
   FOOTER
   ========================= */

.footer {
    text-align: center;

    margin-top: 50px;

    color: #64748b;

    font-size: 13px;
    letter-spacing: 0.2px;
}


/* =========================
   ANIMAȚIE
   ========================= */

@keyframes appear {

    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


/* =========================
   RESPONSIVE
   ========================= */

@media (max-width: 700px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .title {
        font-size: 36px;
    }

    .subtitle {
        font-size: 15px;
    }

    .logo {
        width: 68px;
        height: 68px;
        font-size: 36px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown(
    "<h1 style='text-align: center;'>⚖️ RO Tax Advisor</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>"
    "Asistent AI pentru Codul fiscal din România"
    "</p>",
    unsafe_allow_html=True
)


# =========================
# BUTON ISTORIC
# =========================

if st.button("📜  Istoric conversații"):
    st.switch_page("pages/istoric.py")


# =========================
# ÎNTREBARE
# =========================

st.markdown("### 💬 Pune o întrebare despre Codul fiscal")

question = st.text_area(
    "Întrebarea ta",
    placeholder="Exemplu: Ce condiții trebuie îndeplinite pentru scutirea de impozit a profitului reinvestit?",
    height=120,
    label_visibility="collapsed"
)


# =========================
# BUTON CĂUTARE
# =========================

if st.button("🔍  Caută răspunsul"):

    if not question.strip():

        st.warning("Te rog să introduci o întrebare.")

    else:

        with st.spinner("🤖 Analizez Codul fiscal..."):

            graph = create_graph()

            result = graph.invoke({
                "question": question
            })

            save_history(
                question,
                result["answer"]
            )


        # =========================
        # RĂSPUNS
        # =========================

        st.markdown(
            '<div class="answer-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="answer-title">📚 Răspuns</div>',
            unsafe_allow_html=True
        )

        st.write(result["answer"])

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        # =========================
        # SURSE
        # =========================

        st.markdown(
            '<div class="sources-title">📖 Surse relevante</div>',
            unsafe_allow_html=True
        )

        for i, chunk in enumerate(
            result["chunks"],
            1
        ):

            metadata = chunk["metadata"]

            article = metadata.get(
                "article",
                ""
            )

            chapter = metadata.get(
                "chapter",
                ""
            )

            title = metadata.get(
                "title",
                ""
            )

            with st.expander(
                f"📄 Sursa {i} — {article or 'Articol necunoscut'}"
            ):

                if title:
                    st.write(
                        f"**Titlu:** {title}"
                    )

                if chapter:
                    st.write(
                        f"**Capitol:** {chapter}"
                    )

                if article:
                    st.write(
                        f"**Articol:** {article}"
                    )

                st.write("**Fragment:**")

                st.write(
                    chunk["text"]
                )


# =========================
# FOOTER
# =========================

st.markdown("""
<div class="footer">
    ⚖️ RO Tax Advisor • Powered by AI & RAG
</div>
""", unsafe_allow_html=True)
