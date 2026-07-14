from langchain_ollama import OllamaLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# ----------------------------------------
# Load LLM
# ----------------------------------------

llm = OllamaLLM(model="llama3.1")

# ---------------------------------------
# Prompt Template
# ----------------------------------------

template = """
You are a helpful AI assistant for QuickBite Food Delivery.

Your responsibilities:
- Help customers order food.
- Remember the customer's delivery address once they mention it.
- Remember the customer's dietary preference once they mention it.
- Use this information naturally in later replies.
- Be friendly and concise.

Conversation History:
{history}

User:
{input}

QuickBite:
"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template
)

# ----------------------------------------
# Memory
# ----------------------------------------

memory = ConversationBufferMemory(
    memory_key="history"
)

# ----------------------------------------
# Conversation Chain
# ----------------------------------------

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=False
)

# ----------------------------------------
# Chat Loop
# ----------------------------------------

print("=" * 50)
print("QuickBite Food Delivery Assistant")
print("Type 'exit' to end the conversation.")
print("=" * 50)

turns = 0

while True:

    user_input = input("\nUser: ")

    if user_input.lower() == "exit":
        print("\nConversation Ended.")
        print(f"Total Turns: {turns}")

        print("\nMemory Buffer")
        print("-" * 50)
        print(memory.buffer)

        break

    response = conversation.predict(input=user_input)

    print(f"QuickBite: {response}")

    turns += 1