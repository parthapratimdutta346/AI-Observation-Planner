import streamlit as st


def show_about():

    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    st.markdown("""
    <div style='text-align:center;padding:30px 10px;'>

    <h1>🌌 AI Observation Planner</h1>

    <h4 style='color:#9db2ce;'>
    Where Artificial Intelligence meets Modern Astronomy
    and the Indian Knowledge System
    </h4>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # Vision
    # --------------------------------------------------------

    st.header("🌍 Vision")

    st.write("""
The universe has always inspired humanity to ask questions.

Every civilization looked toward the night sky with curiosity.
Some created stories.
Some developed mathematics.
Some dedicated their lives to understanding the movement of celestial bodies.

This project is a humble attempt to continue that journey.

AI Observation Planner combines Artificial Intelligence,
Machine Learning, Modern Astronomy and the Indian Knowledge
System (IKS) into a single platform that encourages people to
observe, learn and appreciate the universe from both scientific
and historical perspectives.
""")

    st.divider()

    # --------------------------------------------------------
    # Mission
    # --------------------------------------------------------

    st.header("🎯 Mission")

    st.write("""
Our mission is simple.

• Make astronomy easier to understand.

• Preserve India's scientific heritage.

• Inspire more people—especially the younger generation—to
look toward the night sky with curiosity.

Every great discovery begins with one simple question:

**"What am I looking at?"**
""")

    st.divider()

    # --------------------------------------------------------
    # Workflow
    # --------------------------------------------------------

    st.header("⚙️ System Workflow")

    st.code("""
                User
                  │
                  ▼
      Location • Date • Time
                  │
                  ▼
      Weather & Atmospheric Data
          (OpenWeather API)
                  │
                  ▼
      Skyfield Astronomy Engine
                  │
                  ▼
     Machine Learning Prediction
 Observation Score & Sky Quality
                  │
                  ▼
      Recommendation Engine
                  │
       ┌──────────┴──────────┐
       ▼                     ▼
Modern Astronomy      Indian Knowledge
 Scientific Data       Ancient Texts
       └──────────┬──────────┘
                  ▼
      AI Astronomy Assistant
                  │
                  ▼
 Intelligent Observation Planning
""")

    st.divider()

    # --------------------------------------------------------
    # Science
    # --------------------------------------------------------

    st.header("🔬 Science with Heritage")

    st.write("""
This platform is built upon modern scientific astronomy while
also highlighting India's remarkable astronomical heritage.

Modern astronomy provides the calculations,
observations, physics and prediction models.

The Indian Knowledge System contributes centuries of
astronomical wisdom preserved through scholars and
classical literature.

The objective is not to compare one against the other,
but to understand how both contribute to humanity's
understanding of the universe.
""")

    st.divider()

    # --------------------------------------------------------
    # Legacy
    # --------------------------------------------------------

    st.header("🕉 India's Astronomical Legacy")

    st.markdown("""
- Aryabhata
- Brahmagupta
- Bhaskaracharya
- Pathani Samanta
- Surya Siddhanta
- Aryabhatiya
- Siddhanta Darpana
- Vedanga Jyotisha
""")

    st.write("""
These scholars observed the heavens with remarkable
dedication using the knowledge and tools available during
their time.

Their work continues to inspire astronomers,
researchers and students.
""")

    st.divider()

    # --------------------------------------------------------
    # Odisha
    # --------------------------------------------------------

    st.header("🌾 Odisha's Contribution")

    st.write("""
Odisha holds a special place in India's astronomical history.

One of its greatest astronomers,
**Pathani Samanta (1835–1904)**,
performed highly accurate celestial observations using
instruments designed and built by himself.

His masterpiece,
**Siddhanta Darpana**,
remains one of India's finest examples of traditional
observational astronomy.

This project proudly acknowledges Odisha's contribution
to India's scientific heritage.
""")

    st.divider()

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    st.header("🚀 Current Features")

    col1, col2 = st.columns(2)

    with col1:
        st.success("AI Observation Prediction")
        st.success("Weather Analysis")
        st.success("Skyfield Calculations")
        st.success("Celestial Object Recommendation")

    with col2:
        st.success("AI Astronomy Assistant")
        st.success("IKS Integration")
        st.success("Image Identification")
        st.success("RAG Knowledge Base")

    st.divider()

    # --------------------------------------------------------
    # Future
    # --------------------------------------------------------

    st.header("🌱 Future Vision")

    st.write("""
This application is currently a prototype.

With continued research,
collaboration,
institutional support,
larger astronomical datasets,
and future funding,

it has the potential to become a comprehensive
educational and observation platform for

• Students

• Researchers

• Educators

• Observatories

• Astronomy Enthusiasts
""")

    st.divider()

    # --------------------------------------------------------
    # Developer
    # --------------------------------------------------------

    st.header("👨‍💻 About the Developer")

    st.write("""
Developed by

**Partha Pratim Dutta**

This platform is continuously being enhanced
through ongoing work in the field of the
Indian Knowledge System (IKS),
with the vision of making astronomy more
accessible while preserving India's
scientific heritage.
""")

    st.divider()

    # --------------------------------------------------------
    # Final Thoughts
    # --------------------------------------------------------

    st.header("🌠 Final Thoughts")

    st.info(
        '"The stars belong to no nation, no language, '
        'and no generation. They belong to everyone '
        'who chooses to look up."'
    )

    st.write("""
If this project inspires even one person
to observe the night sky,
learn something new,
or become curious about the universe,

then it has already achieved its purpose.

The greatest credit for this project does not belong
to the developer.

It belongs to scientists.

It belongs to mathematicians.

It belongs to astronomers.

It belongs to teachers and researchers.

Above all,

**It belongs to Science.**
""")

    st.divider()

    # --------------------------------------------------------
    # Connect
    # --------------------------------------------------------

    st.header("🤝 Connect")

    st.markdown("""
**Partha Pratim Dutta**

🔗 LinkedIn

https://www.linkedin.com/in/partha-pratim-dutta/

---

*"May we continue to explore the universe with curiosity,
humility, and respect for those who showed us the way."*
""")