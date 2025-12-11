import pytest
from backend.database import calculate_popularity_scores
from backend.models import Order, OrderItem, Product

def test_popularity_frequency_vs_volume():
    """
    CRITICAL BUSINESS LOGIC TEST:
    Ensure we count 'Unique Orders' (Frequency), NOT 'Total Quantity' (Volume).
    """
    
    mock_products = [
        Product(id="BULK_ITEM", name="Bulk", description=".", price=1.0, category=".", brand=".", rating=5.0, in_stock=True, image_url=".", popularity_score=0),
        Product(id="TRENDY_ITEM", name="Trendy", description=".", price=1.0, category=".", brand=".", rating=5.0, in_stock=True, image_url=".", popularity_score=0)
    ]

    mock_orders = [
        Order(
            order_id="1", date="2023-01-01", customer_id="A", total=100,
            items=[
                OrderItem(product_id="BULK_ITEM", quantity=100, price=1.0)
            ]
        ),
        Order(
            order_id="2", date="2023-01-02", customer_id="B", total=10,
            items=[
                OrderItem(product_id="TRENDY_ITEM", quantity=1, price=10.0)
            ]
        ),
        Order(
            order_id="3", date="2023-01-03", customer_id="C", total=10,
            items=[
                OrderItem(product_id="TRENDY_ITEM", quantity=1, price=10.0)
            ]
        )
    ]
    
    calculate_popularity_scores(mock_products, mock_orders)
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
                OrderItem(product_id="A", quantity=1, price=10.0)
            ]
        )
    ]
    
    calculate_popularity_scores(mock_products, mock_orders)
    
    assert mock_products[0].popularity_score == 1