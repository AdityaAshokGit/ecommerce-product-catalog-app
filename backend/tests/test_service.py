import pytest
from unittest.mock import patch
from backend.models import Product
from backend.product_service import filter_products

# --- 1. THE "CHAOS" DATASET ---
@pytest.fixture
def chaos_data():
    """
    A dataset designed to break weak logic.
    Includes: Emojis, Special Chars, Negative Prices, Huge Numbers, Duplicates.
    """
    return [
        Product(id="1", name="Standard Shoe", description="Normal", price=50.0, category="Basic", brand="Nike", rating=4.0, in_stock=True, image_url="u", popularity_score=10),
        Product(id="2", name="🔥 Hot Item!", description="Unicode test", price=50.0, category="Trend", brand="Nike", rating=4.5, in_stock=True, image_url="u", popularity_score=100),
        Product(id="3", name="SQL' Injection --", description="Security check", price=99.99, category="Hack", brand="Null", rating=1.0, in_stock=True, image_url="u", popularity_score=0),
        Product(id="4", name="   Whitespace   ", description="Trim check", price=10.0, category="Basic", brand="   ", rating=2.0, in_stock=True, image_url="u", popularity_score=5),
        Product(id="5", name="Expensive", description="Rich", price=1_000_000.0, category="Lux", brand="Gucci", rating=5.0, in_stock=True, image_url="u", popularity_score=10),
        Product(id="6", name="Freebie", description="Zero price", price=0.0, category="Promo", brand="Generic", rating=3.0, in_stock=True, image_url="u", popularity_score=500),
        Product(id="7", name="Negative Price", description="Buggy data", price=-5.0, category="Err", brand="Bug", rating=0.0, in_stock=True, image_url="u", popularity_score=0),
        # Identical Items for Sort Stability Check
        Product(id="8", name="Twin A", description="Twin", price=20.0, category="Clone", brand="X", rating=4.0, in_stock=True, image_url="u", popularity_score=10),
        Product(id="9", name="Twin B", description="Twin", price=20.0, category="Clone", brand="X", rating=4.0, in_stock=True, image_url="u", popularity_score=10),
    ]

# --- 2. SEARCH ROBUSTNESS ---
@patch('backend.product_service.get_all_products')
@pytest.mark.parametrize("query,expected_ids", [
    ("🔥", ["2"]),                 # Unicode/Emoji Search
    ("sql", ["3"]),                 # Case insensitive on special chars
    ("   ", ["4"]),                 # Whitespace search (should match whitespace name)
    ("WHITESPACE", ["4"]),          # Trimmed logic check
    ("1000000", []),                # Searching numbers in string fields (usually fails)
    ("DROP TABLE", []),             # SQL Injection attempt (should just return empty)
    ("nonexistent_super_long_string_that_should_not_crash_the_server_12345", []), # Buffer overflow-ish
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

    # B. Negative Handling (Should logic allow it? Or filter it out?)
    # If we pass min=-10, max=-1, we might find the buggy product.
    # This tests if your filter blindly accepts inputs.
    res = filter_products(min_price=-10, max_price=-1)
    assert len(res) == 1
    assert res[0].name == "Negative Price"

    # C. Massive Range
    res = filter_products(min_price=0, max_price=float('inf'))
    assert len(res) >= 6 # Should find almost everything

    # D. Inverted Range (User Error)
    res = filter_products(min_price=100, max_price=50)
    assert len(res) == 0 # Should gracefully return nothing

    # E. Floating Point Precision
    # Product is 99.99. Search for 99.98 to 99.991
    res = filter_products(min_price=99.98, max_price=99.991)
    assert len(res) == 1
    assert res[0].id == "3"

# --- 4. SORT STABILITY ---
@patch('backend.product_service.get_all_products')
def test_sort_stability(mock_get, chaos_data):
    mock_get.return_value = chaos_data
    
    # Twin A and Twin B have IDENTICAL price, rating, and score.
    # A stable sort preserves their original order (ID 8 then ID 9).
    
    results = filter_products(sort_by="price_asc")
    # Filter down to just the twins for easy checking
    twins = [p for p in results if "Twin" in p.name]
    
    # If sort is stable: Twin A comes before Twin B (because it was loaded first)
    assert twins[0].name == "Twin A"
    assert twins[1].name == "Twin B"

# --- 5. EMPTY STORE SCENARIOS ---
@patch('backend.product_service.get_all_products')
def test_empty_database(mock_get):
    """What if the store has went bankrupt and has 0 products?"""
    mock_get.return_value = []
    
    # Should not crash
    assert filter_products(search="Anything") == []
    assert filter_products(min_price=0, max_price=100) == []
    assert filter_products(sort_by="popular") == []

# --- 6. DEFENSIVE PROGRAMMING (None Handling) ---
@patch('backend.product_service.get_all_products')
def test_none_inputs(mock_get, chaos_data):
    mock_get.return_value = chaos_data
    
    # If I pass explicit None to everything, it should return full list
    results = filter_products(search=None, category=None, brand=None)
    assert len(results) == len(chaos_data)

# --- 7. PAGINATION SIMULATION (Future Proofing) ---
# Even though we don't have pagination, we test that large result sets 
# are returned correctly without truncation (unless we add that feature).
@patch('backend.product_service.get_all_products')
def test_large_result_set(mock_get, chaos_data):
    # Duplicate the chaos data 100 times to simulate 900 products
    large_dataset = chaos_data * 100
    mock_get.return_value = large_dataset
    
    results = filter_products(category="Basic")
    # "Standard Shoe" (ID 1) and "Whitespace" (ID 4) are Basic.
    # 2 items * 100 duplicates = 200 items.
    assert len(results) == 200