def build_prompt(question, retrieved_chunks):
    """
    Build the prompt using retrieved RAG context.
    """

    context = ""

    sources = []

    for chunk in retrieved_chunks:

        context += (
            f"\nBook: {chunk['book']}"
            f"\nPage: {chunk['page']}"
            f"\nContent:\n{chunk['text']}\n"
            f"\n-------------------------\n"
        )

        sources.append(
            f"{chunk['book']} (Page {chunk['page']})"
        )

    prompt = f"""
Answer the user's question ONLY using the context below whenever possible.

If the answer is not contained in the context, clearly state that the indexed IKS books do not contain sufficient information, and then you may provide a general astronomy explanation.

========================
CONTEXT
========================

{context}

========================
QUESTION
========================

{question}
"""

    return prompt, list(dict.fromkeys(sources))