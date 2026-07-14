import streamlit as st
from langchain_ollama import OllamaLLM

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Dish Description Generator",
    page_icon="🍽️"
)

st.title("🍽️ AI Dish Description Generator")

# ----------------------------
# Load LLM
# ----------------------------
llm = OllamaLLM(model="llama3.1")

# ----------------------------
# Session State
# ----------------------------
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

# ----------------------------
# User Inputs
# ----------------------------
dish_name = st.text_input(
    "Dish Name",
    placeholder="Paneer Tikka Masala"
)

cuisine = st.text_input(
    "Cuisine Type",
    placeholder="North Indian"
)

length = st.selectbox(
    "Description Length",
    ["Short", "Medium", "Long"]
)

# ----------------------------
# Prompt Function
# ----------------------------
def build_prompt():
    return f"""
You are a professional food copywriter.

Generate a {length.lower()} promotional description.

Dish Name:
{dish_name}

Cuisine:
{cuisine}

Requirements:
- Write in an appetising and customer-facing tone.
- Highlight flavour, aroma and texture.
- Encourage customers to order.
- Keep the description suitable for a food delivery app.
"""

# ----------------------------
# Generate Function
# ----------------------------
def generate_description():
    prompt = build_prompt()

    # Print prompt to terminal
    print("\n========== PROMPT ==========")
    print(prompt)
    print("============================\n")

    with st.spinner("Generating description…"):
        response = llm.invoke(prompt)

    st.session_state.generated_text = response

# ----------------------------
# Generate Button
# ----------------------------
if st.button("Generate Description"):

    if dish_name.strip() == "" or cuisine.strip() == "":
        st.warning("Please enter Dish Name and Cuisine Type.")
    else:
        generate_description()

# ----------------------------
# Regenerate Button
# ----------------------------
if st.session_state.generated_text:

    if st.button("Regenerate"):
        generate_description()

# ----------------------------
# Output Container
# ----------------------------
if st.session_state.generated_text:

    with st.container(border=True):

        st.subheader("Generated Description")

        st.write(st.session_state.generated_text)

    st.write(
        f"**Character Count:** {len(st.session_state.generated_text)}"
    )