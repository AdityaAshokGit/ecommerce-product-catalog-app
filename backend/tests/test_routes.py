from starlette.testclient import TestClient
from backend.main import app
from backend.models import Product
import pytest
from unittest.mock import patch

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch('backend.product_service.get_all_products')
def test_get_products_integration(mock_get, client):
    """
    Hit the actual URL. Verify Pydantic serialization works over HTTP.
    """
    # FIX: Return Pydantic Objects, NOT Dictionaries
    mock_get.return_value = [
        Product(id="1", name="TestProduct", price=10.0, category="TestCat", brand="TestBrand", in_stock=True, description="Desc", rating=5.0, image_url="url", popularity_score=0, tags=[])
    ]
    
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    
    # Check pagination wrapper
    assert len(data['items']) == 1
    assert data['items'][0]["name"] == "TestProduct"
    assert "total" in data

@patch('backend.product_service.get_all_products')
def test_get_products_with_query_params(mock_get, client):
    """
    Verify FastAPI correctly parses query parameters from the URL string.
    """
    mock_get.return_value = [
        Product(id="1", name="TestProduct", price=100.0, category="TestCat", brand="TestBrand", in_stock=True, description="Desc", rating=5.0, image_url="url", popularity_score=0, tags=[])
    ]

    # FIX: Change 'q=API' to 'q=TestProduct' so it matches the mock name
    response = client.get("/api/products?q=TestProduct&minPrice=50")
    assert response.status_code == 200
    
    assert len(response.json()['items']) == 1

@patch('backend.product_service.get_all_products')
def test_metadata_endpoint(mock_get, client):
    mock_get.return_value = [
         Product(id="1", name="P1", category="TestCat", brand="TestBrand", price=10, in_stock=True, description="", rating=0, image_url="", popularity_score=0, tags=[])
    ]
    
    response = client.get("/api/metadata")
    assert response.status_code == 200
    data = response.json()
    
    # Check Faceted Structure
    categories = [c['name'] for c in data["categories"]]
    assert "TestCat" in categories
    
    brands = [b['name'] for b in data["brands"]]
    assert "TestBrand" in brands