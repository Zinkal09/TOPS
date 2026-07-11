from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# =====================================================
# Step 1 : Policy Document (300+ words)
# =====================================================

policy_text = """
FoodExpress aims to provide a smooth and reliable food delivery experience.
Customers usually receive their orders within 30 to 45 minutes depending on
traffic, weather conditions, restaurant preparation time, and courier
availability. During peak hours, festivals, weekends, or severe weather,
delivery may take longer than expected. Customers can track their order in
real time through the application.

Orders may be cancelled only before the restaurant starts preparing the food.
Once preparation has begun, cancellation requests may be rejected because the
restaurant has already started processing the order. If cancellation is
approved before preparation begins, the customer receives a full refund through
the original payment method within five to seven business days.

Refunds are provided in specific situations. Customers are eligible for a full
refund if the wrong item is delivered, if one or more ordered items are
missing, if the restaurant accepts cancellation before food preparation, or if
the order cannot be delivered due to operational reasons. Partial refunds may
be issued when only certain items are missing from the order. Refund requests
must normally be submitted within twenty-four hours after delivery together
with photographs whenever applicable.

If a restaurant is temporarily out of stock, it may substitute an item with a
similar product only after notifying the customer whenever possible. Customers
who do not accept the substitution may request a refund for that specific item.
Quality complaints should be reported immediately through customer support.

Customers can contact customer support using the Help section inside the mobile
application or website. Support agents are available twenty-four hours a day to
assist with delivery issues, refunds, payment concerns, missing items, wrong
items, and technical problems.
"""

# =====================================================
# Step 2 : Chunking (100 words with 20-word overlap)
# =====================================================

def chunk_text(text, chunk_size=100, overlap=20):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


chunks = chunk_text(policy_text)

print("Total Chunks:", len(chunks))

# =====================================================
# Step 3 : Embeddings
# =====================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

# =====================================================
# Step 4 : FAISS Index
# =====================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS Index Size:", index.ntotal)

# =====================================================
# Step 5 : Retrieval Function
# =====================================================

def retrieve(query, k=3):

    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, k)

    retrieved = []

    for idx in indices[0]:
        retrieved.append(chunks[idx])

    return retrieved

# =====================================================
# Step 6 : Build RAG Prompt
# =====================================================

def build_rag_prompt(query, retrieved_chunks):

    prompt = """
SYSTEM:
You are a helpful Food Delivery Support Assistant.

Use ONLY the provided context to answer the question.
If the answer is not found in the context, reply:
"I don't know."

"""

    prompt += "CONTEXT:\n\n"

    for i, chunk in enumerate(retrieved_chunks, start=1):

        prompt += f"[{i}] {chunk}\n\n"

    prompt += f"USER QUESTION:\n{query}\n\n"

    prompt += "ANSWER ONLY FROM THE CONTEXT."

    return prompt

# =====================================================
# Step 7 : Demo
# =====================================================

query = "What is the refund policy for missing items?"

retrieved_chunks = retrieve(query)

print("\n" + "=" * 60)
print("Retrieved Chunks\n")

for i, chunk in enumerate(retrieved_chunks, start=1):

    print(f"Chunk {i}:\n")
    print(chunk)
    print()

print("=" * 60)
print("Final RAG Prompt\n")

prompt = build_rag_prompt(query, retrieved_chunks)

print(prompt)

print("\n" + "=" * 60)

print("Simulated Answer:\n")

print(
    "Customers are eligible for a refund if items are missing from their "
    "order. Partial refunds may be issued when only some items are missing, "
    "and refund requests should be submitted within 24 hours."
)