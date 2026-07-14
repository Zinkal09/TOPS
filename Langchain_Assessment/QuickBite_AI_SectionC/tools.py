import requests
from langchain_core.tools import tool


@tool
def get_delivery_estimate(distance_km: float,
                          num_items: int,
                          rain_flag: int) -> str:
    """
    Estimate food delivery time using the local Flask API.

    Parameters:
        distance_km : Distance to customer
        num_items   : Number of ordered items
        rain_flag   : 1 if raining else 0

    Returns:
        Human readable delivery estimate.
    """

    payload = {
        "distance_km": distance_km,
        "num_items": num_items,
        "rain_flag": rain_flag
    }

    try:

        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=payload,
            timeout=5
        )

        if response.status_code == 200:

            prediction = response.json()

            return (
                f"Estimated delivery time is "
                f"{prediction['predicted_delivery_time_min']} minutes."
            )

        return f"API Error : {response.text}"

    except Exception as e:

        return f"Connection Error : {e}"