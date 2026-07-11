"""
rag.py

Handles:
1. Embedding generation
2. FAISS index creation
3. Semantic retrieval
4. RAG prompt construction
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

from policy import POLICY_TEXT, chunk_text


# ==========================================================
# Load Model
# ==========================================================

print("Loading Sentence Transformer Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully.\n")


# ==========================================================
# Chunk Policy
# ==========================================================

chunks = chunk_text(POLICY_TEXT)

print(f"Total Policy Chunks : {len(chunks)}")


# ==========================================================
# Generate Embeddings
# ==========================================================

print("Generating Embeddings...")

embeddings = model.encode(
    chunks,
    convert_to_numpy=True
).astype("float32")

print("Embeddings Generated Successfully.\n")


# ==========================================================
# Build FAISS Index
# ==========================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print(f"FAISS Index Created Successfully.")
print(f"Indexed Chunks : {index.ntotal}\n")


# ==========================================================
# Retrieve Relevant Chunks
# ==========================================================

def retrieve(query, k=3):
    """
    Returns top-k relevant policy chunks.
    """

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        results.append(
            {
                "chunk": chunks[idx],
                "distance": float(distance)
            }
        )

    return results


# ==========================================================
# Build RAG Prompt
# ==========================================================

def build_rag_prompt(query, retrieved_chunks):
    """
    Builds the final prompt that would be sent to an LLM.
    """

    prompt = """
================ SYSTEM =================

You are a Food Delivery Help Desk Assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply exactly:

I don't know.

========================================

Retrieved Context:

"""

    for i, item in enumerate(retrieved_chunks, start=1):

        prompt += f"\n[{i}]\n"
        prompt += item["chunk"]
        prompt += "\n"

    prompt += "\n========================================\n"

    prompt += f"User Question:\n{query}\n\n"

    prompt += (
        "Instruction:\n"
        "Answer ONLY from the provided context.\n"
        "If information is missing, reply 'I don't know.'"
    )

    return prompt


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    query = "What is the refund policy for missing items?"

    results = retrieve(query)

    print("=" * 60)
    print("Retrieved Chunks")
    print("=" * 60)

    for i, item in enumerate(results, start=1):

        print(f"\nChunk {i}")
        print("-" * 40)
        print(item["chunk"])
        print(f"\nDistance : {item['distance']:.4f}")

    print("\n" + "=" * 60)
    print("Generated RAG Prompt")
    print("=" * 60)

    prompt = build_rag_prompt(query, results)

    print(prompt)