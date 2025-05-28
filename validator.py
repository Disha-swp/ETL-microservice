# validator.py

from jsonschema import validate, ValidationError
from schema import sales_transaction_schema

def validate_sales_data(data):
    try:
        validate(instance=data, schema=sales_transaction_schema)
        return True, None
    except ValidationError as ve:
        return False, str(ve)
