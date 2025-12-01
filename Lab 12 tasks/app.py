from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# ------------------------------------------------------------------
# LOAD MODEL + SCALER
# ------------------------------------------------------------------
with open("best_stock_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# -------------------------------------------------------------------
# LOAD FEATURE COLUMNS (from your CSV file)
# -------------------------------------------------------------------
# Example assumption: EW-MAX.csv has columns used during training
df = pd.read_csv("EW-MAX.csv")
feature_columns = df.columns.tolist()

# If target column exists, remove it
if "Target" in feature_columns:
    feature_columns.remove("Target")

# Identify numeric columns (all except any categorical you might add later)
numeric_columns = feature_columns  # all are numeric for stock data


@app.route("/", methods=["GET", "POST"])
def index():
    predicted_value = None

    if request.method == "POST":

        # Collect input features
        input_data = []
        for col in feature_columns:
            value = request.form.get(col)
            input_data.append(float(value))

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data], columns=feature_columns)

        # Scale data
        scaled_data = scaler.transform(input_df)

        # Predict
        predicted_value = model.predict(scaled_data)[0]
        predicted_value = round(float(predicted_value), 4)

    return render_template("index.html",predicted_value=predicted_value,feature_columns=feature_columns)


if __name__ == "__main__":
    app.run(debug=True)
