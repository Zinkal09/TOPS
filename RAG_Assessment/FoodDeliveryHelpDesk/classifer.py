"""
classifier.py

Handles:
1. Few-shot complaint examples
2. Prompt construction
3. Complaint classification
4. Finding the closest matching example
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# ==========================================================
# Load Model
# ==========================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

# ==========================================================
# Few-Shot Example Bank
# ==========================================================

examples = [
    {
        "text": "My order arrived almost one hour late.",
        "label": "Late Delivery"
    },
    {
        "text": "I ordered pizza but received a burger.",
        "label": "Wrong Item"
    },
    {
        "text": "The cold drink was missing from my order.",
        "label": "Missing Item"
    },
    {
        "text": "The food was stale and tasted bad.",
        "label": "Poor Quality"
    }
]

# ==========================================================
# Create FAISS Index for Examples
# ==========================================================

example_texts = [example["text"] for example in examples]

embeddings = model.encode(
    example_texts,
    convert_to_numpy=True
).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ==========================================================
# Build Few-Shot Prompt
# ==========================================================

def build_few_shot_prompt(complaint):

    prompt = (
        "Classify the customer's complaint into one of the "
        "following categories:\n\n"
        "- Late Delivery\n"
        "- Wrong Item\n"
        "- Missing Item\n"
        "- Poor Quality\n\n"
        "Examples:\n\n"
    )

    for example in examples:

        prompt += f"Input: {example['text']}\n"
        prompt += f"Output: {example['label']}\n\n"

    prompt += f"Input: {complaint}\n"
    prompt += "Output: "

    return prompt

# ==========================================================
# Classify Complaint
# ==========================================================

def classify_complaint(complaint):

    query_embedding = model.encode(
        [complaint],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, 1)

    best_index = indices[0][0]

    prediction = examples[best_index]["label"]
    closest_example = examples[best_index]["text"]
    distance = float(distances[0][0])

    return {
        "category": prediction,
        "closest_example": closest_example,
        "distance": distance
    }

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    complaint = "My fries were missing from the delivery."

    prompt = build_few_shot_prompt(complaint)

    print("=" * 60)
    print("Few-Shot Prompt")
    print("=" * 60)
    print(prompt)

    result = classify_complaint(complaint)

    print("\n" + "=" * 60)
    print("Classification Result")
    print("=" * 60)

    print(f"Complaint          : {complaint}")
    print(f"Predicted Category : {result['category']}")
    print(f"Closest Example    : {result['closest_example']}")
    print(f"L2 Distance        : {result['distance']:.4f}")