"""
main.py

Food Delivery Help Desk Chatbot
Menu Driven Console Application
"""

from rag import retrieve, build_rag_prompt
from classifier import build_few_shot_prompt, classify_complaint
from logger import initialize_log, log_interaction

# ==========================================
# Initialize Session
# ==========================================

initialize_log()

policy_questions = 0
complaints = 0

print("=" * 60)
print("   FOOD DELIVERY HELP DESK CHATBOT")
print("=" * 60)

# ==========================================
# Main Menu Loop
# ==========================================

while True:

    print("\nChoose an option:")
    print("1. Ask a Policy Question (RAG)")
    print("2. Classify a Complaint")
    print("3. Exit")

    choice = input("\nEnter your choice: ").strip()

    # ==========================================
    # Option 1 : RAG
    # ==========================================

    if choice == "1":

        while True:

            query = input("\nEnter your policy question: ").strip()

            if query:
                break

            print("Question cannot be empty. Please try again.")

        policy_questions += 1

        retrieved_chunks = retrieve(query, k=3)

        print("\n" + "=" * 60)
        print("Retrieved Context")
        print("=" * 60)

        context_text = ""

        for i, item in enumerate(retrieved_chunks, start=1):

            print(f"\nContext {i}")
            print("-" * 40)
            print(item["chunk"])

            context_text += f"\nContext {i}\n"
            context_text += item["chunk"] + "\n"

        prompt = build_rag_prompt(query, retrieved_chunks)

        print("\n" + "=" * 60)
        print("Generated RAG Prompt")
        print("=" * 60)

        print(prompt)

        simulated_answer = (
            "This is a simulated response generated from the retrieved context."
        )

        print("\nAnswer:")
        print(simulated_answer)

        log_interaction(
            mode="RAG",
            query=query,
            output=simulated_answer
        )

    # ==========================================
    # Option 2 : Complaint Classification
    # ==========================================

    elif choice == "2":

        while True:

            complaint = input("\nEnter complaint: ").strip()

            if complaint:
                break

            print("Complaint cannot be empty. Please try again.")

        complaints += 1

        prompt = build_few_shot_prompt(complaint)

        print("\n" + "=" * 60)
        print("Few-Shot Prompt")
        print("=" * 60)

        print(prompt)

        result = classify_complaint(complaint)

        print("\nPrediction")
        print("-" * 40)
        print(f"Category         : {result['category']}")
        print(f"Closest Example  : {result['closest_example']}")
        print(f"L2 Distance      : {result['distance']:.4f}")

        output = (
            f"Category: {result['category']}\n"
            f"Closest Example: {result['closest_example']}"
        )

        log_interaction(
            mode="Classify",
            query=complaint,
            output=output
        )

    # ==========================================
    # Exit
    # ==========================================

    elif choice == "3":

        print("\n" + "=" * 60)
        print("Session Summary")
        print("=" * 60)

        print(f"Policy Questions Asked : {policy_questions}")
        print(f"Complaints Classified  : {complaints}")

        print("\nSession log saved to session_log.txt")

        print("\nThank you for using Food Delivery Help Desk Chatbot!")

        break

    # ==========================================
    # Invalid Choice
    # ==========================================

    else:

        print("\nInvalid choice. Please enter 1, 2 or 3.")