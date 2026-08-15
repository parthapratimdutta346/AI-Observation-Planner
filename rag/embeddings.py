from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

# This downloads only once (~90 MB)
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Create embeddings for all chunks.

    Returns:
        numpy.ndarray
    """

    texts = [chunk["text"] for chunk in chunks]

    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return vectors