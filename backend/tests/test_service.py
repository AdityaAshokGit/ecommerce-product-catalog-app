import pytest
from unittest.mock import patch, MagicMock
from backend.product_service import filter_products
import backend.product_service # Import module to access globals
from backend.models import Product

# --- FIX: RESET GLOBAL STATE ---
# This ensures every test builds a fresh index based on its specific mock data
@pytest.fixture(autouse=True)
def reset_search_index():
    backend.product_service.IS_INDEX_BUILT = False
    backend.product_service.SEARCH_INDEX.clear()

@pytest.fixture
def chaos_data():
    """Generates a list of products with tricky edge cases."""
    return [
        Product(id="1", name="Standard Shoe", description="Normal", price=50.0, category="Basic", brand="Nike", rating=4.0, in_stock=True, image_url="u", tags=[], popularity_score=10),
        Product(id="2", name="Expensive!", description="Pricey", price=1000000.0, category="Luxury", brand="Gucci", rating=5.0, in_stock=True, image_url="u", tags=[], popularity_score=5),
        Product(id="3", name="SQL Injection", description="SELECT * FROM users", price=10.0, category="Hack", brand="BobbyTables", rating=1.0, in_stock=True, image_url="u", tags=[], popularity_score=0),
        Product(id="4", name="   Whitespace   ", description="   ", price=20.0, category="Messy", brand="   ", rating=2.0, in_stock=True, image_url="u", tags=[], popularity_score=1),
        Product(id="5", name="Emoji 👟", description="Fire 🔥", price=100.0, category="Cool", brand="Brand™", rating=4.5, in_stock=True, image_url="u", tags=[], popularity_score=100),
        Product(id="6", name="Freebie", description="Zero price", price=0.0, category="Promo", brand="Generic", rating=3.0, in_stock=True, image_url="u", tags=[], popularity_score=500),
    ]

@patch('backend.product_service.get_all_products')
@pytest.mark.parametrize("query,expected_ids", [
    ("sql", ["3"]),
    ("WHITESPACE", ["4"]),
    ("1000000", []), 
    ("DROP TABLE", []),
])
def test_search_edge_cases(mock_get, chaos_data, query, expected_ids):
    mock_get.return_value = chaos_data
    result = filter_products(search=query)
    found_ids = sorted([p.id for p in result['items']])
    assert found_ids == sorted(expected_ids)

@patch('backend.product_service.get_all_products')
def test_price_mathematics(mock_get, chaos_data):
    mock_get.return_value = chaos_data
    res = filter_products(min_price=0, max_price=0)
    assert len(res['items']) == 1
    assert res['items'][0].name == "Freebie"

@patch('backend.product_service.get_all_products')
def test_sort_stability(mock_get, chaos_data):
    # Add items to existing chaos_data list for this specific test
    test_data = chaos_data + [
        Product(id="7", name="Negative Price", description="Buggy data", price=-5.0, category="Err", brand="Bug", rating=0.0, in_stock=True, image_url="u", tags=[], popularity_score=0),
        Product(id="8", name="Twin A", description=".", price=50.0, category="Basic", brand="Nike", rating=4.0, in_stock=True, image_url="u", tags=[], popularity_score=10),
        Product(id="9", name="Twin B", description=".", price=50.0, category="Basic", brand="Nike", rating=4.0, in_stock=True, image_url="u", tags=[], popularity_score=10)
    ]
    mock_get.return_value = test_data
    
    results = filter_products(sort_by="price_asc")
    items = results['items']
    
    assert items[0].price == -5.0
    twins = [p for p in items if "Twin" in p.name]
    assert len(twins) == 2

@patch('backend.product_service.get_all_products')
def test_empty_database(mock_get):
    mock_get.return_value = []
    res = filter_products(search="Anything")
    assert res['items'] == []
    assert res['total'] == 0

@patch('backend.product_service.get_all_products')
@pytest.mark.parametrize("query,expected_count", [
    ("Nike", 1),
    ("nike", 1),
    ("RUNNING", 2),
    ("", 5),
])
def test_search_scenarios(mock_get, query, expected_count):
    # Define data INSIDE the test function so index builds with THIS data
    data = [
        Product(id="1", name="Nike Air Max", description="Running", price=100.0, category="Footwear", brand="Nike", rating=4.5, in_stock=True, image_url="u", tags=[], popularity_score=10),
        Product(id="2", name="Adidas Ultraboost", description="Running shoes", price=120.0, category="Footwear", brand="Adidas", rating=4.8, in_stock=True, image_url="u", tags=[], popularity_score=50),
        Product(id="3", name="Puma T-Shirt", description="Cotton", price=30.0, category="Apparel", brand="Puma", rating=4.0, in_stock=True, image_url="u", tags=[], popularity_score=5),
        Product(id="4", name="Apple Watch", description="Tech", price=300.0, category="Electronics", brand="Apple", rating=4.9, in_stock=True, image_url="u", tags=[], popularity_score=100),
        Product(id="5", name="Generic Cable", description="Wire", price=10.0, category="Accessories", brand="Store", rating=5.0, in_stock=True, image_url="u", tags=[], popularity_score=1),
    ]
    mock_get.return_value = data
    
    results = filter_products(search=query)
    assert len(results['items']) == expected_count

@patch('backend.product_service.get_all_products')
def test_filters_strict(mock_get):
    data = [
        Product(id="1", name="Nike Air Max", description="Running", price=100.0, category="Footwear", brand="Nike", rating=4.5, in_stock=True, image_url="u", tags=[], popularity_score=10),
        Product(id="2", name="Adidas Ultraboost", description="Running shoes", price=120.0, category="Footwear", brand="Adidas", rating=4.8, in_stock=True, image_url="u", tags=[], popularity_score=50),
        Product(id="3", name="Puma T-Shirt", description="Cotton", price=30.0, category="Apparel", brand="Puma", rating=4.0, in_stock=True, image_url="u", tags=[], popularity_score=5),
        Product(id="4", name="Apple Watch", description="Tech", price=300.0, category="Electronics", brand="Apple", rating=4.9, in_stock=True, image_url="u", tags=[], popularity_score=100),
        Product(id="5", name="Generic Cable", description="Wire", price=10.0, category="Accessories", brand="Generic", rating=3.0, in_stock=True, image_url="u", tags=[], popularity_score=5),
    ]
    mock_get.return_value = data

    assert len(filter_products(categories=["Footwear"])['items']) == 2
    assert len(filter_products(brands=["Nike"])['items']) == 1
    assert len(filter_products(min_price=200)['items']) == 1
    assert len(filter_products(brands=["NonExistent"])['items']) == 0

@patch('backend.product_service.get_all_products')
def test_complex_combination(mock_get):
    data = [
        Product(id="1", name="Nike Air Max", description="Running", price=100.0, category="Footwear", brand="Nike", rating=4.5, in_stock=True, image_url="u", tags=[], popularity_score=10),
        Product(id="2", name="Adidas Ultraboost", description="Running shoes", price=120.0, category="Footwear", brand="Adidas", rating=4.8, in_stock=True, image_url="u", tags=[], popularity_score=50),
        Product(id="3", name="Puma T-Shirt", description="Cotton", price=30.0, category="Apparel", brand="Puma", rating=4.0, in_stock=True, image_url="u", tags=[], popularity_score=5),
        Product(id="4", name="Apple Watch", description="Tech", price=300.0, category="Electronics", brand="Apple", rating=4.9, in_stock=True, image_url="u", tags=[], popularity_score=100),
        Product(id="5", name="Generic Cable", description="Wire", price=10.0, category="Accessories", brand="Generic", rating=3.0, in_stock=True, image_url="u", tags=[], popularity_score=5),
    ]
    mock_get.return_value = data
    
    results = filter_products(
        search="Running", 
        categories=["Footwear"], 
        max_price=120, 
        sort_by="rating"
    )
    
    items = results['items']
    assert len(items) == 2
    assert items[0].brand == "Adidas"