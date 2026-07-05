import streamlit as st
import json

from conversation import conversation
from conversation import store

from tools import get_delivery_estimate

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="QuickBite AI",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 QuickBite AI")
st.subheader("Your Intelligent Food Delivery Assistant")

# ---------------------------------------
# Load Menu
# ---------------------------------------

with open("menu.json", "r") as f:
    menu = json.load(f)

# ---------------------------------------
# Session State
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "address" not in st.session_state:
    st.session_state.address = ""

if "diet" not in st.session_state:
    st.session_state.diet = "Vegetarian"

# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.title("Customer Details")

st.session_state.address = st.sidebar.text_input(
    "Delivery Address",
    value=st.session_state.address
)

st.session_state.diet = st.sidebar.selectbox(
    "Dietary Preference",
    [
        "Vegetarian",
        "Non-Vegetarian"
    ]
)

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):

    st.session_state.messages = []

    # Clear LangChain Memory
    store.clear()

    st.success("Conversation Cleared")

    st.rerun()

# ---------------------------------------
# Display Previous Chat
# ---------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------
# Menu Search Function
# ---------------------------------------

def search_menu(user_query):

    query = user_query.lower()
    results = []

    for item in menu:

        # Dietary Filter
        if st.session_state.diet == "Vegetarian" and not item["veg"]:
            continue

        # Match Cuisine
        if item["cuisine"].lower() in query:
            results.append(item)

        # Match Dish Name
        elif item["name"].lower() in query:
            results.append(item)

    # Default Recommendation
    if len(results) == 0:

        for item in menu:

            if st.session_state.diet == "Vegetarian":

                if item["veg"]:
                    results.append(item)

            else:
                results.append(item)

    return results[:3]


# ---------------------------------------
# Chat Input
# ---------------------------------------

user_input = st.chat_input("Ask QuickBite anything...")

if user_input:

    # Show User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ---------------------------------------
    # Search Menu
    # ---------------------------------------

    recommendations = search_menu(user_input)

    menu_context = ""

    for item in recommendations:

        menu_context += (
            f"- {item['name']} "
            f"({item['cuisine']}) "
            f"₹{item['price']} "
            f"{'Veg' if item['veg'] else 'Non-Veg'}\n"
        )

    # ---------------------------------------
    # Delivery Tool
    # ---------------------------------------

    delivery_info = ""

    delivery_keywords = [
        "delivery",
        "deliver",
        "time",
        "eta",
        "minutes",
        "estimate"
    ]

    if any(word in user_input.lower() for word in delivery_keywords):

        # Demo values
        # Later you can take these from UI
        delivery_info = get_delivery_estimate.invoke(
            {
                "distance_km": 5,
                "num_items": 2,
                "rain_flag": 0
            }
        )

    # ---------------------------------------
    # LangChain
    # ---------------------------------------

    config = {
        "configurable": {
            "session_id": "quickbite"
        }
    }

    with st.spinner("Thinking..."):

        response = conversation.invoke(
            {
                "input": user_input,
                "address": st.session_state.address,
                "diet": st.session_state.diet,
                "menu_context": menu_context + "\n" + delivery_info
            },
            config=config
        )

    assistant_message = response.content

    # ---------------------------------------
    # Display Assistant
    # ---------------------------------------

    with st.chat_message("assistant"):
        st.markdown(assistant_message)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )
    