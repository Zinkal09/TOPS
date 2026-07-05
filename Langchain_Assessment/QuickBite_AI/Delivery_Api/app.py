from flask import Flask, request, jsonify
import joblib
import pandas as pd

# ------------------------------------
# Load model ONCE when the app starts
# ------------------------------------
model = joblib.load("delivery_model.joblib")

app = Flask(__name__)

# ------------------------------------
# Prediction Route
# ------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    required_fields = [
        "distance_km",
        "num_items",
        "rain_flag"
    ]

    # Check missing fields
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({
            "error": "Missing required field(s).",
            "missing_fields": missing
        }), 400

    # Create DataFrame
    input_data = pd.DataFrame({
        "distance_km": [data["distance_km"]],
        "num_items": [data["num_items"]],
        "rain_flag": [data["rain_flag"]]
    })

    prediction = model.predict(input_data)[0]

    return jsonify({
        "predicted_delivery_time_min": round(float(prediction), 1)
    }), 200


# ------------------------------------
# Run App
# ------------------------------------
if __name__ == "__main__":
    app.run(debug=True)