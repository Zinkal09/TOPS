from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# -------------------------------------------------
# Step 1: Restaurant FAQs
# -------------------------------------------------

faqs = [
    "Our average delivery time is 30 to 45 minutes.",
    "Orders can be cancelled within 5 minutes of placing them.",
    "Refunds are provided for eligible cancelled or incorrect orders.",
    "If an item is unavailable, we may substitute it with a similar product.",
    "You can contact customer support through the Help section in the app.",
    "Track your order in real time using the Order Tracking page."
]

# -------------------------------------------------
# Step 2: Load Sentence Transformer Model
# -------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------------------------
# Step 3: Generate Embeddings
# -------------------------------------------------

faq_embeddings = model.encode(faqs)

# Convert to float32
faq_embeddings = np.array(faq_embeddings).astype("float32")

# -------------------------------------------------
# Step 4: Build FAISS Index
# -------------------------------------------------

dimension = faq_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(faq_embeddings)

print(f"Total FAQs indexed: {index.ntotal}")

# -------------------------------------------------
# Step 5: Semantic Search Function
# -------------------------------------------------

def search_faq(query, k=2):

    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        results.append((faqs[idx], distance))

    return results

# -------------------------------------------------
# Test Query 1
# -------------------------------------------------

print("\n" + "="*60)
print("Query 1: How do I get money back?\n")

results = search_faq("How do I get money back?")

for i, (faq, distance) in enumerate(results, start=1):
    print(f"{i}. FAQ: {faq}")
    print(f"   Distance: {distance:.4f}")

# -------------------------------------------------
# Test Query 2
# -------------------------------------------------

print("\n" + "="*60)
print("Query 2: I want to talk to someone.\n")

results = search_faq("I want to talk to someone.")

for i, (faq, distance) in enumerate(results, start=1):
    print(f"{i}. FAQ: {faq}")
    print(f"   Distance: {distance:.4f}")