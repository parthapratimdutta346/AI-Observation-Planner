from pdf_loader import load_books
from text_chunker import chunk_documents

docs = load_books()

chunks = chunk_documents(docs)

print(f"\nBooks Pages : {len(docs)}")
print(f"Chunks      : {len(chunks)}")

print("\nFirst Chunk\n")

print(chunks[0])