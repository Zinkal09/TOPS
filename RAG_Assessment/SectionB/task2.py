# ==========================================
# Task 2 : Few-Shot Complaint Classifier
# ==========================================

# Few-shot labelled examples
examples = [

    {
        "input": "My order arrived 45 minutes late.",
        "output": "Late Delivery"
    },

    {
        "input": "I ordered pizza but received a burger.",
        "output": "Wrong Item"
    },

    {
        "input": "My cold drink was missing from the order.",
        "output": "Missing Item"
    },

    {
        "input": "The food was stale and tasted bad.",
        "output": "Poor Quality"
    }

]

# ------------------------------------------
# Function to add a new labelled example
# ------------------------------------------
def add_example(text, label):

    examples.append({
        "input": text,
        "output": label
    })


# ------------------------------------------
# Function to build few-shot prompt
# ------------------------------------------
def build_few_shot_prompt(complaint_text):

    prompt = (
        "Classify the customer's complaint into one of the following categories:\n"
        "- Late Delivery\n"
        "- Wrong Item\n"
        "- Missing Item\n"
        "- Poor Quality\n\n"
    )

    prompt += "Examples:\n\n"

    for example in examples:

        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n\n"

    prompt += f"Input: {complaint_text}\n"
    prompt += "Output: "

    return prompt


# ==========================================
# Test 1
# ==========================================

print("=" * 60)
print("Prompt for Complaint 1\n")

prompt1 = build_few_shot_prompt(
    "My food reached me almost one hour late."
)

print(prompt1)


# ==========================================
# Add New Example
# ==========================================

add_example(
    "The fries were completely cold and soggy.",
    "Poor Quality"
)

print("=" * 60)
print("New example added successfully!\n")


# ==========================================
# Test 2
# ==========================================

print("=" * 60)
print("Prompt for Complaint 2\n")

prompt2 = build_few_shot_prompt(
    "The dessert I ordered was not included."
)

print(prompt2)