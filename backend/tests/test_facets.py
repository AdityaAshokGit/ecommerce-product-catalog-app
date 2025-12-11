import pytest
from unittest.mock import patch
from backend.product_service import get_faceted_metadata
from backend.models import Product

@pytest.fixture
def facet_mock_data():
    return [
        Product(id="1", name="A", category="Shoes", brand="Nike", price=100, in_stock=True, description="", rating=0, image_url="", popularity_score=0, tags=[]),
        Product(id="2", name="B", category="Shoes", brand="Adidas", price=100, in_stock=True, description="", rating=0, image_url="", popularity_score=0, tags=[]),
        Product(id="3", name="C", category="Shirts", brand="Nike", price=50, in_stock=True, description="", rating=0, image_url="", popularity_score=0, tags=[]),
        Product(id="4", name="D", category="Hats", brand="Puma", price=20, in_stock=False, description="", rating=0, image_url="", popularity_score=0, tags=[]),
    ]

@patch('backend.product_service.get_all_products')
def test_facet_exclude_self_logic(mock_get, facet_mock_data):
    """
    CRITICAL: Verify that selecting a value in a filter does NOT hide its peers.
    """
    mock_get.return_value = facet_mock_data

    # Scenario: Select Category="Shoes"
    # Expectation: 
    #   - Brands: Should show Nike(1), Adidas(1). (Nike Shirt is excluded)
    #   - Categories: Should STILL show Shirts(1), Hats(1) alongside Shoes(2).
    
    meta = get_faceted_metadata(categories=["Shoes"])
    
    # 1. Verify Brands filtered correctly (Context Awareness)
    brands = {b['name']: b['count'] for b in meta['brands']}
    assert brands['Nike'] == 1  # Only the Shoe, not the Shirt
    assert brands['Adidas'] == 1
    assert 'Puma' not in brands # Puma is Hats, so it's gone. Correct.

    # 2. Verify Categories did NOT filter themselves (Exclude Self)
    cats = {c['name']: c['count'] for c in meta['categories']}
    assert cats['Shoes'] == 2
    assert cats['Shirts'] == 1 # This must remain visible!
    assert cats['Hats'] == 1   # This must remain visible!

@patch('backend.product_service.get_all_products')
def test_availability_facets(mock_get, facet_mock_data):
    """
    Verify Availability counts dynamic updates.
    """
    mock_get.return_value = facet_mock_data
    
    # Scenario: Filter by Brand="Nike"
    # Nike items: 1 Shoe (In Stock), 1 Shirt (In Stock). Total 2.
    meta = get_faceted_metadata(brands=["Nike"])
    
    avail = {a['value']: a['count'] for a in meta['availability']}
    assert avail['in-stock'] == 2
    assert avail['sold-out'] == 0

    # Scenario: Filter by Brand="Puma"
    # Puma items: 1 Hat (Sold Out)
    meta_puma = get_faceted_metadata(brands=["Puma"])
    avail_puma = {a['value']: a['count'] for a in meta_puma['availability']}
    assert avail_puma['in-stock'] == 0
    assert avail_puma['sold-out'] == 1