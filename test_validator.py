import pytest
from validator import validate_sales_data

def test_valid_data():
    valid_data = {
        "order_id": "ORD-1234",
        "customer_id": "CUST-001",
        "order_date": "2025-05-26T12:34:56Z",
        "source": "web",
        "items": [
            {"sku": "ABC123", "name": "Product A", "qty": 2, "unit_price": 10.0}
        ],
        "shipping_address": {
            "line1": "123 Street",
            "city": "City",
            "state": "State",
            "postal_code": "12345",
            "country": "Country"
        },
        "payment_method": "card",
        "total_amount": 20.0
    }

    is_valid, _ = validate_sales_data(valid_data)
    assert is_valid

def test_invalid_missing_field():
    # Missing 'customer_id'
    invalid_data = {
        "order_id": "ORD-1234",
        "order_date": "2025-05-26T12:34:56Z",
        "source": "web",
        "items": [
            {"sku": "ABC123", "name": "Product A", "qty": 2, "unit_price": 10.0}
        ],
        "shipping_address": {
            "line1": "123 Street",
            "city": "City",
            "state": "State",
            "postal_code": "12345",
            "country": "Country"
        },
        "payment_method": "card",
        "total_amount": 20.0
    }

    is_valid, error = validate_sales_data(invalid_data)
    assert not is_valid
    assert "customer_id" in error

def test_invalid_negative_amount():
    # Negative total_amount
    invalid_data = {
        "order_id": "ORD-1234",
        "customer_id": "CUST-001",
        "order_date": "2025-05-26T12:34:56Z",
        "source": "web",
        "items": [
            {"sku": "ABC123", "name": "Product A", "qty": 2, "unit_price": 10.0}
        ],
        "shipping_address": {
            "line1": "123 Street",
            "city": "City",
            "state": "State",
            "postal_code": "12345",
            "country": "Country"
        },
        "payment_method": "card",
        "total_amount": -50.0
    }

    is_valid, error = validate_sales_data(invalid_data)
    assert not is_valid
    assert "total_amount" in error
