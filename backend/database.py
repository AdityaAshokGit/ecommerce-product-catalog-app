import json
import os
from typing import List, Optional, Dict
from backend.models import Product, Order

# Global In-Memory Database
PRODUCTS: List[Product] = []
ORDERS: List[Order] = []

# --- RECOMMENDATION ENGINE (Co-Occurrence Graph) ---
# Map<TargetID, Map<RelatedID, Frequency>>
# Example: "101": { "102": 5, "105": 2 }
CO_PURCHASE_MAP: Dict[str, Dict[str, int]] = {}

def build_recommendation_graph(orders: List[Order]):
    """
    Analyzes order history to build a co-occurrence matrix.
    Time Complexity: O(K * M^2) where K=Orders, M=Items per order.
    """
    global CO_PURCHASE_MAP
    CO_PURCHASE_MAP.clear()
    
    print("🔄 Building Recommendation Graph...")
    
    for order in orders:
        # Get unique items in this order to avoid self-linking
        # (e.g. buying 2 of the same item doesn't link it to itself)
        item_ids = list({item.product_id for item in order.items})
        
        # Double loop to link every item with every other item in the cart
        for i in range(len(item_ids)):
            p1 = item_ids[i]
            for j in range(i + 1, len(item_ids)):
                p2 = item_ids[j]
                
                # Link p1 -> p2
                if p1 not in CO_PURCHASE_MAP: CO_PURCHASE_MAP[p1] = {}
                CO_PURCHASE_MAP[p1][p2] = CO_PURCHASE_MAP[p1].get(p2, 0) + 1
                
                # Link p2 -> p1 (Symmetric)
                if p2 not in CO_PURCHASE_MAP: CO_PURCHASE_MAP[p2] = {}
                CO_PURCHASE_MAP[p2][p1] = CO_PURCHASE_MAP[p2].get(p1, 0) + 1
    
    print(f"✅ Recommendation Graph built. tracked relationships for {len(CO_PURCHASE_MAP)} products.")

def get_recommended_product_ids(product_id: str, limit: int = 3) -> List[str]:
    """
    Returns the top N product IDs frequently bought with the given product.
    """
    if product_id not in CO_PURCHASE_MAP:
        return []
    
    # Get neighbors map: { "102": 5, "105": 2 }
    neighbors = CO_PURCHASE_MAP[product_id]
    
    # Sort by frequency count (Descending) -> [("102", 5), ("105", 2)]
    sorted_neighbors = sorted(neighbors.items(), key=lambda item: item[1], reverse=True)
    
    # Return just the IDs
    return [pid for pid, count in sorted_neighbors[:limit]]

def calculate_popularity_scores(products: List[Product], orders: List[Order]):
    """
    Calculates popularity based on ORDER FREQUENCY (Unique Orders).
    """
    frequency_map = {} # ProductID -> Count of Orders it appeared in

    for order in orders:
        # Use a set to count a product only ONCE per order
        unique_items_in_order = {item.product_id for item in order.items}
        
        for product_id in unique_items_in_order:
            frequency_map[product_id] = frequency_map.get(product_id, 0) + 1

    # Update products
    for product in products:
        product.popularity_score = frequency_map.get(product.id, 0)

def load_data():
    global PRODUCTS, ORDERS
    
    # Get absolute path to data directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    products_path = os.path.join(data_dir, 'products.json')
    orders_path = os.path.join(data_dir, 'orders.json')

    # 1. Load Products
    try:
        with open(products_path, 'r') as f:
            data = json.load(f)
            PRODUCTS = [Product(**item) for item in data]
            print(f"✅ Loaded {len(PRODUCTS)} products")
    except FileNotFoundError:
        print("❌ Critical: products.json missing")
        PRODUCTS = []
    except json.JSONDecodeError:
         print("❌ Critical: products.json corrupt")
         PRODUCTS = []

    # 2. Load Orders
    try:
        with open(orders_path, 'r') as f:
            orders_data = json.load(f)
            ORDERS = [Order(**item) for item in orders_data]
            print(f"✅ Loaded {len(ORDERS)} orders")
            
            # --- CALCULATE METRICS ---
            calculate_popularity_scores(PRODUCTS, ORDERS)
            build_recommendation_graph(ORDERS) # <--- NEW STEP
            
    except FileNotFoundError:
        print("⚠️ Warning: orders.json missing. Analytics disabled.")
        ORDERS = []
    except json.JSONDecodeError:
         print("⚠️ Warning: orders.json corrupt. Analytics disabled.")
         ORDERS = []

def get_all_products() -> List[Product]:
    return PRODUCTS

def get_all_orders() -> List[Order]:
    return ORDERS