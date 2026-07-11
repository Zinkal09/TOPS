"""
policy.py

Contains:
1. Food delivery policy document (500+ words)
2. Chunking function (100 words with 20-word overlap)
"""

# ==========================================================
# Food Delivery Policy Document
# ==========================================================

POLICY_TEXT = """
FoodExpress is committed to providing customers with a reliable, safe, and convenient food delivery experience. Our delivery service is designed to ensure that every customer receives their order in the best possible condition and within the expected delivery time. Delivery time generally ranges from 30 to 45 minutes depending on the restaurant location, preparation time, traffic conditions, weather, and courier availability. During weekends, holidays, festivals, or periods of unusually high demand, deliveries may take longer than expected. Customers can monitor the live status of their order using the Order Tracking feature available in the mobile application and website.

Customers should ensure that the delivery address and contact number entered while placing an order are accurate. Incorrect addresses, incomplete delivery instructions, or unreachable phone numbers may result in delivery delays or unsuccessful deliveries. If the delivery partner cannot reach the customer after multiple attempts, the order may be cancelled without refund if the failure was caused by incorrect customer information.

Orders may be cancelled only before the restaurant begins preparing the food. Once food preparation has started, cancellation requests cannot normally be accepted because the restaurant has already invested time and resources in preparing the order. If a cancellation request is approved before preparation begins, a full refund will be processed using the customer's original payment method. Depending on the customer's bank or payment provider, refunds usually appear within five to seven business days. Cash-on-delivery orders cancelled before preparation will not incur any charge.

Refunds are available under specific situations. Customers are eligible for a full refund if they receive the wrong order, if the entire order cannot be delivered, if the restaurant cancels the order after accepting it, or if payment has been deducted but the order was never successfully placed. Partial refunds may be provided when only some items are missing from the order or when individual items cannot be delivered. Customers requesting refunds should submit their request within twenty-four hours of delivery through the Help section of the application together with photographs whenever possible.

If a restaurant is temporarily out of stock for a selected item, the restaurant may contact the customer to suggest an alternative item of similar value. Item substitutions will only be made with customer approval whenever possible. If the customer does not agree with the substitution, the unavailable item will be removed and a refund for that item will be initiated. Restaurants strive to maintain menu accuracy, but availability may occasionally change without notice.

Food quality is the responsibility of the restaurant partner. If customers receive damaged packaging, spoiled food, cold food when it should be hot, or any quality issue, they should immediately report the issue using the Help section. Supporting photographs help our customer support team investigate the issue more quickly. Depending on the investigation, customers may receive a replacement meal, store credit, or a partial or full refund.

Delivery partners follow optimized routes to reduce delivery time while maintaining food quality. Unexpected traffic congestion, severe weather, road closures, or public events may increase delivery times beyond the estimated arrival window. Customers will receive updated estimated delivery times whenever possible through push notifications and live tracking.

Customer support is available twenty-four hours a day through the mobile application, website, email, and live chat. Support representatives assist with refund requests, cancellation issues, delivery delays, payment concerns, technical problems, account-related issues, missing items, wrong items, and restaurant-related complaints. Every complaint is reviewed individually to ensure a fair resolution. Customers are encouraged to provide complete information, including order number, description of the issue, and supporting evidence when applicable. Our goal is to resolve most support requests within twenty-four hours while maintaining transparency, fairness, and customer satisfaction.
"""

# ==========================================================
# Chunking Function
# ==========================================================

def chunk_text(text, chunk_size=100, overlap=20):
    """
    Splits text into overlapping chunks.

    Parameters:
        text (str): Input document
        chunk_size (int): Number of words per chunk
        overlap (int): Overlapping words between chunks

    Returns:
        list[str]: List of text chunks
    """

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        # Move start forward while keeping overlap
        start += chunk_size - overlap

    return chunks


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    chunks = chunk_text(POLICY_TEXT)

    print("=" * 60)
    print("Food Delivery Policy Loaded")
    print("=" * 60)

    print(f"Total Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}")
        print("-" * 40)
        print(chunk)