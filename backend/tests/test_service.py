import pytest
from unittest.mock import patch
from backend.models import Product
# Import the module so we can reset globals
import backend.product_service as service
from backend.product_service import filter_products

# --- FIXTURE: RESET INDEX STATE ---
@pytest.fixture(autouse=True)
def reset_search_index():
    """
    CRITICAL: Reset the global search index before every test.
    Otherwise, the index built in 'test_search_scenarios' (mock_data)
    will be reused in 'test_search_edge_cases' (chaos_data), causing 0 matches.
    """
    service.SEARCH_INDEX.clear()
    service.IS_INDEX_BUILT = False
    yield
    service.SEARCH_INDEX.clear()
    service.IS_INDEX_BUILT = False

# --- 1. THE "CHAOS" DATASET ---
@pytest.fixture
def chaos_data():
    return [
        Product(id="1", name="Standard Shoe", description="Normal", price=50.0, category="Basic", brand="Nike", rating=4.0, in_stock=True, image_url="u", popularity_score=10),
        Product(id="2", name="🔥 Hot Item!", description="Unicode test", price=50.0, category="Trend", brand="Nike", rating=4.5, in_stock=True, image_url="u", popularity_score=100),
        Product(id="3", name="SQL' Injection --", description="Security check", price=99.99, category="Hack", brand="Null", rating=1.0, in_stock=True, image_url="u", popularity_score=0),
        Product(id="4", name="   Whitespace   ", description="Trim check", price=10.0, category="Basic", brand="   ", rating=2.0, in_stock=True, image_url="u", popularity_score=5),
        Product(id="5", name="Expensive", description="Rich", price=1_000_000.0, category="Lux", brand="Gucci", rating=5.0, in_stock=True, image_url="u", popularity_score=10),
        Product(id="6", name="Freebie", description="Zero price", price=0.0, category="Promo", brand="Generic", rating=3.0, in_stock=True, image_url="u", popularity_score=500),
        Product(id="7", name="Negative Price", description="Buggy data", price=-5.0, category="Err", brand="Bug", rating=0.0, in_stock=True, image_url="u", popularity_score=0),
        Product(id="8", name="Twin A", description="Twin", price=20.0, category="Clone", brand="X", rating=4.0, in_stock=True, image_url="u", popularity_score=10),
        Product(id="9", name="Twin B", description="Twin", price=20.0, category="Clone", brand="X", rating=4.0, in_stock=True, image_url="u", popularity_score=10),
    ]

# --- 2. SEARCH ROBUSTNESS ---
@patch('backend.product_service.get_all_products')
@pytest.mark.parametrize("query,expected_ids", [
    ("🔥", ["2"]),                 # Unicode/Emoji Search (Now Supported!)
    ("sql", ["3"]),                 # Case insensitive on special chars
    ("WHITESPACE", ["4"]),          # Matches token "whitespace"
    ("1000000", []),                # Numbers in string fields not tokenized as keywords usually
    ("DROP TABLE", []),             # SQL Injection attempt
])
def test_search_edge_cases(mock_get, chaos_data, query, expected_ids):
    mock_get.return_value = chaos_data
    results = filter_products(search=query)
    found_ids = sorted([p.id for p in results])
    expected_ids = sorted(expected_ids)
    assert found_ids == expected_ids

# --- 3. PRICE MATHEMATICS ---
@patch('backend.product_service.get_all_products')
def test_price_mathematics(mock_get, chaos_data):
    mock_get.return_value = chaos_data
    # A. Exact Zero
    res = filter_products(min_price=0, max_price=0)
    assert len(res) == 1
    assert res[0].name == "Freebie"
    # B. Massive Range
    res = filter_products(min_price=0, max_price=float('inf'))
    assert len(res) >= 6

# --- 4. SORT STABILITY ---
@patch('backend.product_service.get_all_products')
def test_sort_stability(mock_get, chaos_data):
    mock_get.return_value = chaos_data
    results = filter_products(sort_by="price_asc")
    twins = [p for p in results if "Twin" in p.name]
    # Stable sort check
    assert twins[0].name == "Twin A"
    assert twins[1].name == "Twin B"

# --- 5. EMPTY STORE SCENARIOS ---
@patch('backend.product_service.get_all_products')
def test_empty_database(mock_get):
    mock_get.return_value = []
    assert filter_products(search="Anything") == []

# --- 6. SHARED FIXTURE FOR HAPPY PATH ---
@pytest.fixture
def mock_data():
    return [
        Product(id="1", name="Nike Air Max", description="Running", price=100.0, category="Footwear", brand="Nike", rating=4.5, in_stock=True, image_url="u", popularity_score=10),
        Product(id="2", name="Adidas Ultraboost", description="Running", price=150.0, category="Footwear", brand="Adidas", rating=4.8, in_stock=True, image_url="u", popularity_score=50),
        Product(id="3", name="Apple iPhone", description="Phone", price=999.0, category="Electronics", brand="Apple", rating=4.9, in_stock=False, image_url="u", popularity_score=100),
        Product(id="4", name="Cheap Socks", description="Cotton", price=10.0, category="Footwear", brand="Generic", rating=3.0, in_stock=True, image_url="u", popularity_score=5),
        Product(id="5", name="Free Sticker", description="Promo", price=0.0, category="Accessories", brand="Store", rating=5.0, in_stock=True, image_url="u", popularity_score=1),
    ]

@patch('backend.product_service.get_all_products')
@pytest.mark.parametrize("query,expected_count", [
    ("Nike", 1),
    ("nike", 1),
    ("RUNNING", 2),
    ("", 5),
])
def test_search_scenarios(mock_get, mock_data, query, expected_count):
    mock_get.return_value = mock_data
    results = filter_products(search=query)
    assert len(results) == expected_count