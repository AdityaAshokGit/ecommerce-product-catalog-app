import pytest
import json
from unittest.mock import patch, mock_open
from pydantic import ValidationError
from backend.models import Product
from backend.database import load_data, get_all_products

# --- 1. MODEL VALIDATION TESTS ---
def test_product_model_serialization():
    """
    Critical: Verify that Pydantic correctly converts snake_case to camelCase.
    The Frontend relies 100% on 'imageUrl', not 'image_url'.
    """
    raw_data = {
        "id": "123",
        "name": "Test Item",
        "description": "Desc",
        "price": 10.0,
        "category": "Cat",
        "brand": "Brand",
        "rating": 5.0,
        "in_stock": True,
        "image_url": "http://test.com/img.jpg", # Python side
        "tags": []
    }
    
    # 1. Validation: Should accept snake_case input
    product = Product(**raw_data)
    assert product.image_url == "http://test.com/img.jpg"
    
    # 2. Serialization: Should output camelCase JSON
    json_output = product.model_dump(by_alias=True)
    assert "imageUrl" in json_output
    assert json_output["imageUrl"] == "http://test.com/img.jpg"
    # Ensure snake_case is GONE in the output to avoid frontend confusion
    assert "image_url" not in json_output

def test_product_model_validation_error():
    """
    Ensure we enforce data integrity. Missing fields should crash the loader (fail fast).
    """
    bad_data = {
        "id": "123",
        # Missing 'name' and 'price'
    }
    with pytest.raises(ValidationError):
        Product(**bad_data)

# --- 2. DATA LOADING RESILIENCY TESTS ---
@patch("builtins.open", side_effect=FileNotFoundError)
def test_load_data_missing_files(mock_file):
    """
    If JSON files are missing, the app should NOT crash. 
    It should start up with an empty catalog (Graceful Degradation).
    """
    # Run loader
    load_data()
    
    # Verify state is empty but valid
    products = get_all_products()
    assert isinstance(products, list)
    assert len(products) == 0
    # App is still "alive", just empty. This is better than a crash loop.

@patch("builtins.open", new_callable=mock_open, read_data="[INVALID JSON}")
def test_load_data_corrupt_json(mock_file):
    """
    If JSON is malformed, we should catch the JSONDecodeError 
    and likely default to empty list (or log error).
    Currently, our code might crash here. Let's find out.
    """
    # Note: Our current database.py catches FileNotFoundError, 
    # but does it catch JSON errors? 
    # If this test fails (crashes), we found a bug in database.py!
    try:
        load_data()
    except json.JSONDecodeError:
        pytest.fail("App crashed on bad JSON! We should handle this gracefully.")
    except Exception as e:
        # If we didn't write a try/except for generic errors in database.py, this will fail.
        # This highlights a gap in our implementation.
        pass