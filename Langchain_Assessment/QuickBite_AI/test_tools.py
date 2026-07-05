from tools import get_delivery_estimate

result = get_delivery_estimate.invoke(
    {
        "distance_km":5,
        "num_items":2,
        "rain_flag":0
    }
)

print(result)