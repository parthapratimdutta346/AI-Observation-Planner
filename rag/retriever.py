import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index("vectorstore/faiss_index.bin")

with open("vectorstore/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def retrieve(query, top_k=5, distance_threshold=1.2):
    """
    Retrieve relevant chunks from the vector database.
    Lower distance = better match.
    """

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    seen = set()

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        # Reject weak matches
        if distance > distance_threshold:
            continue

        chunk = metadata[idx]

        # Remove duplicate chunks
        key = (chunk["book"], chunk["page"])

        if key in seen:
            continue

        seen.add(key)

        results.append({
            "book": chunk["book"],
            "page": chunk["page"],
            "text": chunk["text"],
            "distance": float(distance)
        })

    return results