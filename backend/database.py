import json
import os
from typing import List, Dict
from backend.models import Product, Order

# Global In-Memory Storage
PRODUCTS: List[Product] = []
ORDERS: List[Order] = []

# --- NEW: Pure Function for Testing ---
def calculate_popularity_scores(orders: List[Order]) -> Dict[str, int]:
    """
    Calculates popularity based on Order Frequency (Unique Orders).
    Rules:
    - If a user buys 100 units in 1 order -> Score = 1
    - If a user buys 1 unit in 5 different orders -> Score = 5
    """
    popularity_map: Dict[str, int] = {}
    
    for order in orders:
        # Set comprehension ensures we only count each product ONCE per order
        unique_products = {item.product_id for item in order.items}
        
        for pid in unique_products:
            popularity_map[pid] = popularity_map.get(pid, 0) + 1
            
    return popularity_map

def load_data():
    global PRODUCTS, ORDERS
    # ... path setup remains the same ...
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    products_path = os.path.join(base_dir, "data", "products.json")
    orders_path = os.path.join(base_dir, "data", "orders.json")

    # 1. Load Orders
    try:
        with open(orders_path, "r") as f:
            orders_data = json.load(f)
            ORDERS = [Order(**item) for item in orders_data]
            print(f"✅ Loaded {len(ORDERS)} orders.")
    except (FileNotFoundError, json.JSONDecodeError): # <--- UPDATED
        print(f"⚠️ Warning: orders.json missing or corrupt")
        ORDERS = []

    # 2. Compute Popularity
    popularity_map = calculate_popularity_scores(ORDERS)

    # 3. Load Products
    try:
        with open(products_path, "r") as f:
            products_data = json.load(f)
            loaded_products = []
            for item in products_data:
                product = Product(**item)
                product.popularity_score = popularity_map.get(product.id, 0)
                loaded_products.append(product)
            
            PRODUCTS = loaded_products
            print(f"✅ Loaded {len(PRODUCTS)} products.")
    except (FileNotFoundError, json.JSONDecodeError): # <--- UPDATED
        print(f"❌ Critical: products.json missing or corrupt")
        PRODUCTS = []

def get_all_products() -> List[Product]:
    return PRODUCTS