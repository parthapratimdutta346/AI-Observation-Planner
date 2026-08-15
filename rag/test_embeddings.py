from pdf_loader import load_books
from text_chunker import chunk_documents
from embeddings import create_embeddings

print("Loading PDFs...")
docs = load_books()

print("Chunking...")
chunks = chunk_documents(docs)

print("Creating embeddings...")
vectors = create_embeddings(chunks)

print("\n==============================")
print("Books     :", len(docs))
print("Chunks    :", len(chunks))
print("Embeddings:", len(vectors))
print("Dimension :", len(vectors[0]))
print("==============================")