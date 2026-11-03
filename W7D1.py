import os
import chromadb

client = chromadb.PersistentClient(path="./chromadb_storage")
collection_name = "phantoms_knowledge_base"

try:
    client.delete_collection(name=collection_name)
    print("تم حذف الـ Collection القديمة لمنع التكرار.")
except:
    pass

collection = client.create_collection(name=collection_name)
documents = [
    # Programming
    "Python lists are mutable sequences that can store items of different types.",
    "Git branches let developers work on features without affecting the main code.",
    "A REST API exposes resources through HTTP methods like GET and POST.",
    "SQL JOINs combine rows from two tables based on a related column.",
    # Fitness
    "Regular walking for thirty minutes a day improves heart health.",
    "Drinking enough water helps maintain energy and concentration.",
    "Sleep of seven to eight hours supports muscle recovery and memory.",
    "Stretching before exercise can reduce the risk of muscle injuries.",
    # Cooking
    "To make rice fluffy, rinse it first and let it steam after cooking.",
    "Letting dough rest allows the gluten to relax and makes bread softer.",
    "Searing meat at high heat creates a flavorful brown crust.",
    "Adding salt to pasta water seasons the noodles from the inside."
]

ids = [f"doc_{i+1}" for i in range(len(documents))]

metadatas = [
    {"topic": "programming"}, {"topic": "programming"}, {"topic": "programming"}, {"topic": "programming"},
    {"topic": "fitness"}, {"topic": "fitness"}, {"topic": "fitness"}, {"topic": "fitness"},
    {"topic": "cooking"}, {"topic": "cooking"}, {"topic": "cooking"}, {"topic": "cooking"}
]

collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

queries = [
    "How do I store different kinds of values together in Python?",
    "How can I avoid hurting myself when working out?",
    "Why is my bread dense and hard?",
    "What is the best way to merge data from two database tables?",
    "How do I deploy a rocket to Mars?"
]

for i, q in enumerate(queries, 1):
    results = collection.query(
        query_texts=[q],
        n_results=3
    )
    print(f"\nQ{i}: {q}")
    for doc, dist in zip(results['documents'][0], results['distances'][0]):
        print(f"  - المسافة: {dist:.4f} | النص: {doc}")

# 8. تجربة Metadata Filter على Q2 (بدون فلتر و بفلتر fitness)
print("\n--- تجربة Metadata Filter على Q2 ---")
q2 = "How can I avoid hurting myself when working out?"

print("بدون فلتر:")
res_no_filter = collection.query(query_texts=[q2], n_results=2)
for doc, meta in zip(res_no_filter['documents'][0], res_no_filter['metadatas'][0]):
    print(f"  - [{meta['topic']}] {doc}")

print("مع فلتر (topic = fitness):")
res_filtered = collection.query(
    query_texts=[q2], 
    n_results=2, 
    where={"topic": "fitness"}
)
for doc, meta in zip(res_filtered['documents'][0], res_filtered['metadatas'][0]):
    print(f"  - [{meta['topic']}] {doc}")
