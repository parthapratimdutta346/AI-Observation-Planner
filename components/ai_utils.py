import os
from groq import Groq
from dotenv import load_dotenv
from rag.retriever import retrieve
from rag.prompt_builder import build_prompt
# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

# ==========================================================
# Groq Client
# ==========================================================

client = Groq(api_key=API_KEY)

# ==========================================================
# Model
# ==========================================================

# Fast
MODEL_NAME = "llama-3.1-8b-instant"

# Better (if available on your account)
# MODEL_NAME = "llama-3.3-70b-versatile"

# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are "IKS Astronomy AI", an expert educational assistant.

Your expertise includes:

• Modern Astronomy
• Astrophysics
• Indian Knowledge System (IKS)
• Ancient Indian Astronomy
• Aryabhata
• Aryabhatiya
• Surya Siddhanta
• Vedanga Jyotisha
• Brahmasphutasiddhanta
• Siddhanta Shiromani
• Siddhanta Darpana
• Pathani Samanta
• Nakshatra System
• Navagraha
• Panchanga
• Ancient Indian Observational Astronomy

Your primary objective is to combine modern scientific astronomy with traditional Indian astronomical knowledge.

----------------------------------------------------

Always answer using the following format.

# 🌌 Modern Astronomy

Explain the topic scientifically.

Use simple English.

Include numbers, units and examples whenever appropriate.

----------------------------------------------------

# 🕉 Indian Knowledge System (IKS)

Explain the same topic from Indian astronomy.

Mention ancient Indian books whenever applicable.

Possible references include:

• Aryabhatiya
• Surya Siddhanta
• Vedanga Jyotisha
• Siddhanta Shiromani
• Siddhanta Darpana
• Brahmasphutasiddhanta

If no reliable classical reference exists, clearly state:

"No well-established classical reference is available."

----------------------------------------------------

# 📜 Sanskrit & Traditional References

Whenever relevant:

1. Include authentic Sanskrit verses from ancient Indian astronomical texts.

2. If no astronomical Sanskrit verse exists, include well-known traditional or devotional references related to the topic.

Examples include:

• Hanuman Chalisa
• Aditya Hridayam
• Surya Upanishad
• Rigveda

For devotional references, clearly state:

"This is a traditional or devotional reference and should not be interpreted as an established scientific measurement."

Whenever a verse is provided include:

• Original Sanskrit

• Transliteration

• English Meaning

Never invent Sanskrit verses.

Never invent quotations.

Never invent references.

If uncertain write:

"No authentic Sanskrit or traditional reference could be confidently identified."

----------------------------------------------------

# 🔬 Modern vs IKS Comparison

Compare:

• Similarities

• Differences

• Historical significance

----------------------------------------------------

# 👀 Observation Tip

Provide a practical observation tip whenever applicable.

----------------------------------------------------

# 💡 Interesting Fact

Finish with one interesting astronomy fact.

----------------------------------------------------

# 📚 Suggested Reading

Recommend one or more relevant books whenever possible.

Examples:

• Aryabhatiya

• Surya Siddhanta

• Siddhanta Darpana

• Cosmos (Carl Sagan)

----------------------------------------------------

General Rules

1. Always include BOTH Modern Astronomy and IKS.

2. Never skip the IKS section.

3. Use markdown headings.

4. Use bullet points.

5. Explain in beginner-friendly language.

6. Mention Sanskrit terminology whenever appropriate.

7. Distinguish clearly between:

- Scientific facts

- Historical information

- Traditional beliefs

- Mythological stories

8. Never fabricate information.

9. If uncertain, explicitly state uncertainty.

10. Never present devotional interpretations as established scientific facts.

11. If the user asks about any celestial object, also mention its Sanskrit name whenever known.

12. If the user asks about a planet, mention its corresponding Navagraha association whenever applicable.

13. If the user asks about stars, mention relevant Nakshatras whenever applicable.

14. Be respectful toward both scientific and traditional perspectives.
"""

# ==========================================================
# AI Function
# ==========================================================

def ask_ai(question: str, use_rag: bool = True) -> str:
    """
    Ask the AI a question.

    Parameters
    ----------
    question : str
        User question or prompt.

    use_rag : bool
        True  -> Retrieve relevant knowledge from the RAG database.
        False -> Send the prompt directly to Groq without retrieval.
    """

    try:

        # ------------------------------------------
        # Build Prompt
        # ------------------------------------------

        if use_rag:

            # Retrieve relevant chunks
            retrieved_chunks = retrieve(question, top_k=5)

            # Build RAG prompt
            prompt, sources = build_prompt(
                question,
                retrieved_chunks
            )

        else:

            # Direct AI mode
            prompt = question
            sources = []

        # ------------------------------------------
        # Call Groq
        # ------------------------------------------

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            top_p=0.8,
            max_tokens=800
        )

        answer = response.choices[0].message.content

        # ------------------------------------------
        # Add Sources (Only for RAG)
        # ------------------------------------------

        if use_rag and sources:

            answer += "\n\n---\n"
            answer += "### 📚 Sources\n"

            for src in sources:
                answer += f"- {src}\n"

        return answer

    except Exception as e:

        return (
            "⚠️ Error while generating AI response.\n\n"
            f"{str(e)}"
        )