from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from prompts import prompt

# -----------------------------
# Load Ollama Model
# -----------------------------
llm = ChatOllama(
    model="llama3.1",
    temperature=0.7
)

# -----------------------------
# Build Chain
# -----------------------------
chain = prompt | llm

# -----------------------------
# Store Chat History
# -----------------------------
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)