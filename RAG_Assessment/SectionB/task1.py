# ==========================================
# Task 1: Structured Prompt Builder
# Food Delivery Customer Support Chatbot
# ==========================================

# -------------------------------
# System Prompt
# -------------------------------
SYSTEM_PROMPT = """
You are a Food Delivery Customer Support Agent.

Role:
- Help customers resolve order-related issues.
- Be polite, professional, and helpful.
- Apologize when appropriate.
- Provide clear solutions.
- Keep every response under 80 words.
"""

# -------------------------------
# User Prompt Template
# -------------------------------
USER_PROMPT_TEMPLATE = """
Customer Name : {customer_name}
Order ID      : {order_id}
Issue Type    : {issue_type}

Please help the customer resolve this issue.
"""

# -------------------------------
# Allowed Issue Types
# -------------------------------
ALLOWED_ISSUES = [
    "late delivery",
    "missing item",
    "wrong item"
]

# -------------------------------
# Validation Function
# -------------------------------
def validate_issue(issue_type):
    """
    Validates whether the issue type is allowed.
    Raises ValueError if invalid.
    """
    if issue_type.lower() not in ALLOWED_ISSUES:
        raise ValueError(
            f"Invalid issue type: '{issue_type}'. "
            f"Allowed values are: {', '.join(ALLOWED_ISSUES)}."
        )

# -------------------------------
# Prompt Builder
# -------------------------------
def build_prompt(customer_name, order_id, issue_type):

    # Validate input
    validate_issue(issue_type)

    # Create user prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        customer_name=customer_name,
        order_id=order_id,
        issue_type=issue_type
    )

    return SYSTEM_PROMPT, user_prompt


# ==========================================
# Test Cases
# ==========================================

test_cases = [

    {
        "customer_name": "Rahul",
        "order_id": "FD10234",
        "issue_type": "late delivery"
    },

    {
        "customer_name": "Priya",
        "order_id": "FD90876",
        "issue_type": "missing item"
    },

    # Invalid test case (to demonstrate exception handling)
    {
        "customer_name": "Amit",
        "order_id": "FD44567",
        "issue_type": "payment issue"
    }

]

# ==========================================
# Run Test Cases
# ==========================================

for case in test_cases:

    print("=" * 60)

    try:

        system_prompt, user_prompt = build_prompt(
            case["customer_name"],
            case["order_id"],
            case["issue_type"]
        )

        print("SYSTEM PROMPT")
        print(system_prompt)

        print("USER PROMPT")
        print(user_prompt)

    except ValueError as error:
        print("Prompt could not be created.")
        print("Reason:", error)

print("=" * 60)