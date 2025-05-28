# schema.py

sales_transaction_schema = {
    "type": "object",
    "properties": {
        "order_id": {"type": "string"},
        "customer_id": {"type": "string"},
        "order_date": {"type": "string", "format": "date-time"},
        "source": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sku": {"type": "string"},
                    "name": {"type": "string"},
                    "qty": {"type": "integer", "minimum": 1},
                    "unit_price": {"type": "number", "minimum": 0}
                },
                "required": ["sku", "name", "qty", "unit_price"]
            }
        },
        "shipping_address": {
            "type": "object",
            "properties": {
                "line1": {"type": "string"},
                "line2": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "postal_code": {"type": "string"},
                "country": {"type": "string"}
            },
            "required": ["line1", "city", "state", "postal_code", "country"]
        },
        "payment_method": {"type": "string"},
        "total_amount": {"type": "number", "minimum": 0}
    },
    "required": ["order_id", "customer_id", "order_date", "source", "items", "shipping_address", "payment_method", "total_amount"]
}
