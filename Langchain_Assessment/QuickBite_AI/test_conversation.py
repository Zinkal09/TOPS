from conversation import conversation

config = {
    "configurable": {
        "session_id": "quickbite_user"
    }
}

address = "Science City, Ahmedabad"

diet = "Vegetarian"

menu_context = """
Paneer Butter Masala
Veg Biryani
Dal Makhani
"""

print("QuickBite AI")
print("Type 'exit' to quit.\n")

while True:

    question = input("You : ")

    if question.lower() == "exit":
        break

    response = conversation.invoke(
        {
            "input": question,
            "address": address,
            "diet": diet,
            "menu_context": menu_context
        },
        config=config
    )

    print("\nQuickBite :", response.content)
    print("-" * 60)