import pytest
from backend.database import calculate_popularity_scores
from backend.models import Order, OrderItem, Product

def test_popularity_frequency_vs_volume():
    """
    CRITICAL BUSINESS LOGIC TEST:
    Ensure we count 'Unique Orders' (Frequency), NOT 'Total Quantity' (Volume).
    """
    
    # 1. Setup Mock Products
    # We need products to hold the scores now
    mock_products = [
        Product(id="BULK_ITEM", name="Bulk", description=".", price=1.0, category=".", brand=".", rating=5.0, in_stock=True, image_url=".", popularity_score=0),
        Product(id="TRENDY_ITEM", name="Trendy", description=".", price=1.0, category=".", brand=".", rating=5.0, in_stock=True, image_url=".", popularity_score=0)
    ]

    # 2. Setup Mock Orders
    # Scenario:
    # Product "BULK_ITEM": Bought 100 times in 1 order.
    # Product "TRENDY_ITEM": Bought 1 time in 2 separate orders.
    mock_orders = [
        # Order 1: Bulk buy
        Order(
            order_id="1", date="2023-01-01", customer_id="A", total=100,
            items=[
                OrderItem(product_id="BULK_ITEM", quantity=100, price=1.0)
            ]
        ),
        # Order 2: Trendy buy
        Order(
            order_id="2", date="2023-01-02", customer_id="B", total=10,
            items=[
                OrderItem(product_id="TRENDY_ITEM", quantity=1, price=10.0)
            ]
        ),
        # Order 3: Trendy buy again
        Order(
            order_id="3", date="2023-01-03", customer_id="C", total=10,
            items=[
                OrderItem(product_id="TRENDY_ITEM", quantity=1, price=10.0)
            ]
        )
    ]
    
    # 3. Execute Logic (In-Place Update)
    calculate_popularity_scores(mock_products, mock_orders)
    
    # 4. Assertions
    # Map back to a dict for easier checking
    scores = {p.id: p.popularity_score for p in mock_products}

    # BULK_ITEM: Appeared in 1 order -> Score 1
    assert scores["BULK_ITEM"] == 1
    
    # TRENDY_ITEM: Appeared in 2 orders -> Score 2
    # If we were counting volume, this would be 2 vs 100.
    # Since we count frequency, 2 > 1.
    assert scores["TRENDY_ITEM"] == 2

def test_popularity_duplicate_items_in_one_order():
    """
    Edge Case: What if the same product appears twice in the SAME order line items?
    It should still only count as +1 score for that order.
    """
    mock_products = [
        Product(id="A", name="A", description=".", price=1.0, category=".", brand=".", rating=5.0, in_stock=True, image_url=".", popularity_score=0)
    ]

    mock_orders = [
        Order(
            order_id="1", date="2023-01-01", customer_id="A", total=20,
            items=[
                OrderItem(product_id="A", quantity=1, price=10.0),
                OrderItem(product_id="A", quantity=1, price=10.0) # Duplicate line
            ]
        )
    ]
    
    calculate_popularity_scores(mock_products, mock_orders)
    
    assert mock_products[0].popularity_score == 1