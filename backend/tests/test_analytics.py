from backend.models import Order, OrderItem
from backend.database import calculate_popularity_scores

def test_popularity_frequency_vs_volume():
    """
    CRITICAL BUSINESS LOGIC TEST:
    Ensure we count 'Unique Orders' (Frequency), NOT 'Total Quantity' (Volume).
    """
    
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
    
    scores = calculate_popularity_scores(mock_orders)
    
    # Logic Check:
    # BULK_ITEM: 1 Order = Score 1 (Even though volume is 100)
    assert scores["BULK_ITEM"] == 1
    
    # TRENDY_ITEM: 2 Orders = Score 2 (Even though volume is only 2)
    assert scores["TRENDY_ITEM"] == 2
    
    # Conclusion: Trendy > Bulk
    assert scores["TRENDY_ITEM"] > scores["BULK_ITEM"]

def test_popularity_duplicate_items_in_one_order():
    """
    Edge Case: What if the same product appears twice in the SAME order line items?
    (e.g. user added it, then added it again as a separate line).
    It should still only count as +1 score for that order.
    """
    mock_orders = [
        Order(
            order_id="1", date="2023-01-01", customer_id="A", total=20,
            items=[
                OrderItem(product_id="A", quantity=1, price=10.0),
                OrderItem(product_id="A", quantity=1, price=10.0) # Duplicate line
            ]
        )
    ]
    
    scores = calculate_popularity_scores(mock_orders)
    assert scores["A"] == 1