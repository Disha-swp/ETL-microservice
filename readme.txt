Here’s a **beginner-friendly step-by-step guide** to build your Cloud Run ETL microservice with validation, transformation, BigQuery loading, and CI/CD using Cloud Build.

---

## 🧩 Step 1: **Set Up the Project Environment**

1. **Create a Google Cloud project** or use an existing one.
2. **Enable these APIs**:

   * Cloud Run
   * BigQuery
   * Cloud Build
   * Artifact Registry
3. **Install necessary tools**:

   * Docker
   * Git
   * Python (or Node.js, Go, etc. — we’ll use Python + Flask here)
   * `gcloud` CLI

---

## 🛠️ Step 2: **Write the Cloud Run Service (Python + Flask Example)**

Create a project folder and add these files:

### `main.py` — Flask App

```python
from flask import Flask, request, jsonify
from validator import validate_json
from transformer import transform_data
from bigquery_loader import load_to_bigquery

app = Flask(__name__)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    if not validate_json(data):
        return jsonify({'error': 'Invalid schema'}), 400

    transformed = transform_data(data)
    load_to_bigquery(transformed)
    return jsonify({'message': 'Data processed'}), 200
```

### `validator.py` — Schema Validation

```python
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "sale_id": {"type": "string"},
        "amount": {"type": "number"},
        "region": {"type": "string"}
    },
    "required": ["sale_id", "amount", "region"]
}

def validate_json(data):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False
```

### `transformer.py` — Data Transformation

```python
from datetime import datetime

def transform_data(data):
    data['tax'] = round(data['amount'] * 0.1, 2)  # Add 10% tax
    data['timestamp'] = datetime.utcnow().isoformat()
    return data
```

### `bigquery_loader.py` — Load to BigQuery

```python
from google.cloud import bigquery

client = bigquery.Client()
table_id = "your_project.your_dataset.your_table"

def load_to_bigquery(data):
    errors = client.insert_rows_json(table_id, [data])
    if errors:
        raise Exception(f"BigQuery errors: {errors}")
```

---

## 📦 Step 3: **Containerize the Service**

### `Dockerfile`

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### `requirements.txt`

```
Flask
jsonschema
google-cloud-bigquery
```

---

## ☁️ Step 4: **Deploy to Cloud Run**

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sales-etl
gcloud run deploy sales-etl \
  --image gcr.io/YOUR_PROJECT_ID/sales-etl \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🧪 Step 5: **Write Unit Tests**

### `test_validator.py`

```python
from validator import validate_json

def test_valid_data():
    assert validate_json({"sale_id": "123", "amount": 100.0, "region": "US"}) is True

def test_invalid_data():
    assert validate_json({"sale_id": "123"}) is False
```

### `test_transformer.py`

```python
from transformer import transform_data

def test_transformation():
    data = {"sale_id": "123", "amount": 100.0, "region": "US"}
    transformed = transform_data(data)
    assert "tax" in transformed
    assert transformed["tax"] == 10.0
```

Run tests with `pytest` or `unittest`.

---

## ⚙️ Step 6: **Set Up Cloud Build Pipeline**

### `cloudbuild.yaml`

```yaml
steps:
- name: 'python'
  entrypoint: 'pip'
  args: ['install', '-r', 'requirements.txt']

- name: 'python'
  entrypoint: 'pytest'
  args: ['.']

- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/sales-etl', '.']

- name: 'gcr.io/cloud-builders/gcloud'
  args: ['run', 'deploy', 'sales-etl', '--image', 'gcr.io/$PROJECT_ID/sales-etl',
         '--region', 'us-central1', '--platform', 'managed', '--allow-unauthenticated']

images:
- 'gcr.io/$PROJECT_ID/sales-etl'
```

---

## 🔁 Step 7: **Trigger on Main Branch Pushes**

1. Go to **Cloud Build > Triggers** in Google Cloud Console.
2. Create a new trigger:

   * Source: your GitHub repo
   * Branch: `main`
   * Config file: `cloudbuild.yaml`

---

## ✅ Done!

Now every push to `main`:

* Runs tests
* Builds Docker image
* Deploys to Cloud Run

You can access the service using the Cloud Run URL and POST your JSON payloads to `/ingest`.

---
