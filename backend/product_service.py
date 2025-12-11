from typing import List, Optional
from backend.models import Product
from backend.database import get_all_products

def filter_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None
) -> List[Product]:
    
    # 1. Start with all products (In-Memory)
    # In a real DB, this would be a "SELECT * FROM products" query builder
    products = get_all_products()

    # 2. Apply Search (Case-insensitive)
    if search:
        query = search.lower()
        products = [
            p for p in products 
            if query in p.name.lower() or query in p.description.lower()
        ]

    # 3. Apply Filters
    if category:
        products = [p for p in products if p.category.lower() == category.lower()]
    
    if brand:
        products = [p for p in products if p.brand.lower() == brand.lower()]

    if min_price is not None:
        products = [p for p in products if p.price >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]

    # 4. Apply Sorting
    # We use Python's stable sort.
    if sort_by == "price_asc":
        products.sort(key=lambda p: p.price)
    elif sort_by == "price_desc":
        products.sort(key=lambda p: p.price, reverse=True)
    elif sort_by == "rating":
        products.sort(key=lambda p: p.rating, reverse=True) # Highest rating first
    elif sort_by == "popular":
        products.sort(key=lambda p: p.popularity_score, reverse=True) # Highest score first

    return products

def get_filter_options():
    """
    Returns unique categories, brands, and price range.
    Used for the Frontend Sidebar.
    """
    products = get_all_products()
    
    categories = sorted(list(set(p.category for p in products)))
    brands = sorted(list(set(p.brand for p in products)))
    
    prices = [p.price for p in products]
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0

    return {
        "categories": categories,
        "brands": brands,
        "minPrice": min_price,
        "maxPrice": max_price
    }