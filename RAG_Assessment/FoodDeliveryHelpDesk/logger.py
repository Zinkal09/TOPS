"""
logger.py

Handles session logging.
Each interaction is saved in session_log.txt
"""

from datetime import datetime

LOG_FILE = "session_log.txt"


def log_interaction(mode, query, output):
    """
    Logs each interaction to a text file.

    Parameters
    ----------
    mode : str
        RAG or Classify

    query : str
        User input

    output : str
        System response
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write("=" * 70 + "\n")
        file.write(f"Timestamp : {timestamp}\n")
        file.write(f"Mode      : {mode}\n")
        file.write(f"Query     : {query}\n")
        file.write(f"Output    :\n{output}\n")
        file.write("=" * 70 + "\n\n")


def initialize_log():
    """
    Creates a new session log when the application starts.
    """

    with open(LOG_FILE, "w", encoding="utf-8") as file:

        file.write("=" * 70 + "\n")
        file.write(" FOOD DELIVERY HELP DESK CHATBOT SESSION LOG\n")
        file.write("=" * 70 + "\n\n")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    initialize_log()

    log_interaction(
        mode="RAG",
        query="What is the refund policy?",
        output="Refunds are available for missing or wrong items."
    )

    log_interaction(
        mode="Classify",
        query="My order arrived very late.",
        output="Predicted Category: Late Delivery"
    )

    print("Session log created successfully!")