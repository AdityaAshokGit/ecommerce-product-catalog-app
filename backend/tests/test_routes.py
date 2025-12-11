import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import backend.database as db  # Import module alias to avoid stale references
from backend.main import app
from backend.models import Product

# --- FIXTURES ---

@pytest.fixture
def client():
    """
    Create a TestClient where 'load_data' is disabled.
    We patch 'backend.main.load_data' because main.py imports it directly.
    """
    with patch("backend.main.load_data"):
        with TestClient(app) as c:
            yield c

@pytest.fixture(autouse=True)
def setup_data():
    """
    Automatically inject a test product before EVERY test function.
    We modify the list inside the module directly.
    """
    # 1. Clear any existing data
    db.PRODUCTS.clear()
    
    # 2. Inject Test Data
    db.PRODUCTS.append(
        Product(
            id="1", name="API Test Product", description="Desc", 
            price=100.0, category="TestCat", brand="TestBrand", 
            rating=5.0, in_stock=True, image_url="url", popularity_score=10
        )
    )
    yield
    # Cleanup after test
    db.PRODUCTS.clear()

# --- TESTS ---

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Backend is running"}

def test_get_products_integration(client):
    """
    Hit the actual URL. Verify Pydantic serialization works over HTTP.
    """
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    
    # Should now be exactly 1, because we blocked the real file load
    assert len(data) == 1
    assert data[0]["name"] == "API Test Product"
    assert "imageUrl" in data[0] 

def test_get_products_with_query_params(client):
    """
    Verify FastAPI correctly parses query parameters from the URL string.
    """
    # Filter that SHOULD match
    response = client.get("/api/products?q=API&minPrice=50")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Filter that SHOULD NOT match
    response = client.get("/api/products?minPrice=200")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_metadata_endpoint(client):
    response = client.get("/api/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "TestCat" in data["categories"]
    assert "TestBrand" in data["brands"]
    assert data["maxPrice"] == 100.0

def test_validation_error_422(client):
    """
    What if a user sends text as a price? 
    FastAPI should return 422 Unprocessable Entity automatically.
    """
    response = client.get("/api/products?minPrice=not_a_number")
    assert response.status_code == 422