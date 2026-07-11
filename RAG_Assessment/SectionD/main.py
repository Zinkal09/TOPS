from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# ======================================================
# Read Policy File
# ======================================================

with open("policy.txt", "r", encoding="utf-8") as file:
    policy_text = file.read()

# ======================================================
# Chunking Function
# ======================================================

def chunk_text(text, chunk_size=100):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


chunks = chunk_text(policy_text)

print(f"Total Chunks : {len(chunks)}")

# ======================================================
# Load Sentence Transformer
# ======================================================

print("Loading Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully.")

# ======================================================
# Generate Embeddings
# ======================================================

embeddings = model.encode(
    chunks,
    convert_to_numpy=True
).astype("float32")

# ======================================================
# Build FAISS Index
# ======================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print(f"Indexed Chunks : {index.ntotal}")

# ======================================================
# Retrieval Function
# ======================================================

def retrieve(query, k=2):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        results.append({
            "chunk": chunks[idx],
            "distance": float(distance)
        })

    return results

# ======================================================
# Build RAG Prompt
# ======================================================

def build_prompt(question, contexts):

    prompt = """
SYSTEM

You are a Food Delivery Support Assistant.

Answer ONLY using the provided context.

If the answer is unavailable, reply:

I don't know.

CONTEXT

"""

    for i, item in enumerate(contexts, start=1):

        prompt += f"\nContext {i}\n"
        prompt += item["chunk"]
        prompt += "\n"

    prompt += "\nQUESTION\n"

    prompt += question

    prompt += "\n\nANSWER"

    return prompt

# ======================================================
# Main Loop
# ======================================================

while True:

    print("\n" + "=" * 60)

    question = input("Ask a question (or type 'quit'): ").strip()

    if question.lower() == "quit":

        print("\nExiting Chatbot...")

        break

    if not question:

        print("Question cannot be empty.")

        continue

    results = retrieve(question)

    print("\nRetrieved Chunks")
    print("-" * 50)

    for i, item in enumerate(results, start=1):

        print(f"\nChunk {i}")
        print(item["chunk"])

    prompt = build_prompt(question, results)

    print("\n" + "=" * 60)
    print("RAG Prompt")
    print("=" * 60)

    print(prompt)

    print("\nSimulated Answer")

    print("--------------------------------------")

    print(
        "This is a placeholder response generated "
        "using the retrieved policy context."
    )