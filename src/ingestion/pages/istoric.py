import streamlit as st
from history import get_history, clear_history

st.set_page_config(
    page_title="Istoric - RO Tax Advisor",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Istoric conversații")
st.write("Aici poți vedea întrebările și răspunsurile anterioare.")

history = get_history()

if not history:
    st.info("Nu există conversații salvate încă.")

else:
    for item in history:
        history_id, question, answer, created_at = item

        with st.expander(
            f"📅 {created_at} — {question}"
        ):
            st.markdown("### ❓ Întrebare")
            st.write(question)

            st.markdown("### 📚 Răspuns")
            st.write(answer)

    st.write("")

    if st.button("🗑️ Șterge istoricul"):
        clear_history()
        st.success("Istoricul a fost șters.")
        st.rerun()