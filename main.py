# main.py

from flask import Flask, request, jsonify
from validator import validate_sales_data
from datetime import datetime
from google.cloud import bigquery

app = Flask(__name__)

# ---------- Transformation Logic ----------
def transform_data(data):
    TAX_RATE = 0.10  # 10% tax
    data["processed_at"] = datetime.utcnow().isoformat() + "Z"
    data["tax_amount"] = round(data["total_amount"] * TAX_RATE, 2)
    data["final_amount"] = round(data["total_amount"] + data["tax_amount"], 2)
    return data

# ---------- BigQuery Load Logic ----------
def load_to_bigquery(data):
    client = bigquery.Client()
    table_id = "etl-microservice-project.sales_data.transactions"  
    errors = client.insert_rows_json(table_id, [data])  # List of rows
    if errors:
        raise RuntimeError("BigQuery insert errors: {errors}")

# ---------- Route Handler ----------
@app.route("/", methods=["POST"])
def etl_handler():
    data = request.get_json()

    # 1. Validate JSON
    is_valid, error = validate_sales_data(data)
    if not is_valid:
        return jsonify({"error": "Invalid JSON", "details": error}), 400

    # 2. Transform
    transformed_data = transform_data(data)

    # 3. Load to BigQuery
    try:
        load_to_bigquery(transformed_data)
    except Exception as e:
        return jsonify({"error": "Failed to insert to BigQuery", "details": str(e)}), 500

    # 4. Return success response
    return jsonify({"message": "Validated, transformed, and loaded to BigQuery", "data": transformed_data}), 200

# ---------- App Run (for local testing) ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
