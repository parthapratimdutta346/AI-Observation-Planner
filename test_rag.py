from rag.retriever import retrieve

query = "Who was Aryabhata?"

results = retrieve(query, top_k=3)

for i, r in enumerate(results, start=1):
    print("=" * 60)
    print(f"Result {i}")
    print(f"Book : {r['book']}")
    print(f"Page : {r['page']}")
    print(f"Text :\n{r['text'][:500]}")