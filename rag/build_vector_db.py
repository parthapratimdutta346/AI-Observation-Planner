import os
import pickle
import faiss
import numpy as np

from pdf_loader import load_books
from text_chunker import chunk_documents
from embeddings import create_embeddings

VECTOR_DB_FOLDER = "vectorstore"

os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

print("Loading books...")
docs = load_books()

print("Chunking...")
chunks = chunk_documents(docs)

print("Creating embeddings...")
vectors = create_embeddings(chunks)

print("Building FAISS index...")

dimension = vectors.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(vectors).astype("float32"))

faiss.write_index(
    index,
    os.path.join(VECTOR_DB_FOLDER, "faiss_index.bin")
)

with open(
    os.path.join(VECTOR_DB_FOLDER, "metadata.pkl"),
    "wb"
) as f:
    pickle.dump(chunks, f)

print("\n==============================")
print("FAISS database created!")
print("Vectors :", index.ntotal)
print("Saved to:", VECTOR_DB_FOLDER)
print("==============================")