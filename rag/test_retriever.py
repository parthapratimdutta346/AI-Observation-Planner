from retriever import retrieve

question = input("Ask a question: ")

results = retrieve(question)

print("\n")

if not results:
    print("❌ No relevant information found in the indexed books.")
    exit()

print("=" * 80)
print("TOP MATCHES")
print("=" * 80)

for i, r in enumerate(results, start=1):

    print(f"\nResult {i}")
    print(f"Book     : {r['book']}")
    print(f"Page     : {r['page']}")
    print(f"Distance : {r['distance']:.4f}")

    print("-" * 60)
    print(r["text"][:500])
    print("-" * 60)