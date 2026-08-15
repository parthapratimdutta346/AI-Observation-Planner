import streamlit as st
from components.ai_utils import ask_ai


# ==========================================================
# AI Astronomy Assistant
# ==========================================================

def show_ai_assistant():

    st.header("🤖 AI Astronomy Assistant")

    st.write("""
Ask questions related to:

- 🌌 Modern Astronomy
- 🕉 Indian Knowledge System (IKS)
- ⭐ Nakshatras
- 🪐 Planets & Celestial Objects
- 📖 Ancient Indian Astronomy
- 🔭 Observation Tips
""")

    question = st.text_area(
        "Ask your question",
        placeholder="Example: Why is Jupiter called Brihaspati?"
    )

    if st.button("🚀 Ask AI", use_container_width=True):

        if not question.strip():
            st.warning("Please enter a question.")
            return

        # Simple prompt
        prompt = question.strip()

        with st.spinner("🧠 Thinking..."):

            answer = ask_ai(prompt)

        st.success("✨ AI Response")

        st.markdown(answer)