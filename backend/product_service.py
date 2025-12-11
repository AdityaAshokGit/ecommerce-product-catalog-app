from typing import List, Optional, Dict, Set
from backend.models import Product
from backend.database import get_all_products
import string

# --- INVERTED INDEX STORAGE ---
SEARCH_INDEX: Dict[str, Set[str]] = {}
IS_INDEX_BUILT = False

def normalize_tokens(text: str) -> Set[str]:
    """
    Splits text into lowercase tokens.
    UPDATED: Now strictly splits by whitespace and strips punctuation.
    This preserves Emojis (🔥) and accents while removing commas/periods.
    """
    if not text:
        return set()
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Split by whitespace (handles tabs, newlines, spaces)
    raw_tokens = text.split()
    
    # 3. Strip punctuation from edges (e.g. "shoes," -> "shoes")
    # We use string.punctuation for a robust list of symbols
    clean_tokens = set()
    for t in raw_tokens:
        t = t.strip(string.punctuation)
        if t: # Only add if not empty
            clean_tokens.add(t)
            
    return clean_tokens

def build_search_index(products: List[Product]):
    global SEARCH_INDEX, IS_INDEX_BUILT
    SEARCH_INDEX.clear()
    
    for product in products:
        content = f"{product.name} {product.description} {product.brand} {product.category}"
        tokens = normalize_tokens(content)
        
        for token in tokens:
            if token not in SEARCH_INDEX:
                SEARCH_INDEX[token] = set()
            SEARCH_INDEX[token].add(product.id)
            
    IS_INDEX_BUILT = True

def search_with_index(query: str, all_products: List[Product]) -> List[Product]:
    global IS_INDEX_BUILT
    
    # Lazy Load
    if not IS_INDEX_BUILT or not SEARCH_INDEX:
        build_search_index(all_products)
    
    query_tokens = normalize_tokens(query)
    
    # EDGE CASE FIX:
    # If user provided a search string (e.g. "!!!") but tokens are empty,
    # it means no valid words were found. Return NO results.
    if not query_tokens:
        return []

    candidate_ids: Optional[Set[str]] = None
    
    for token in query_tokens:
        matches = SEARCH_INDEX.get(token, set())
        
        if candidate_ids is None:
            candidate_ids = matches
        else:
            candidate_ids = candidate_ids.intersection(matches)
            
        if not candidate_ids:
            return []

    return [p for p in all_products if p.id in candidate_ids]

# --- MAIN SERVICE ---

def filter_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None
) -> List[Product]:
    
    products = get_all_products()

    # 1. SEARCH
    if search:
        # Optimization: specific check for whitespace-only strings
        if not search.strip():
            # If search is just "   ", return all products (or empty? Standard is ignore)
            pass 
        else:
            products = search_with_index(search, products)

    # 2. FILTER
    if category:
        products = [p for p in products if p.category.lower() == category.lower()]
    
    if brand:
        products = [p for p in products if p.brand.lower() == brand.lower()]

    if min_price is not None:
        products = [p for p in products if p.price >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]

    # 3. SORT
    if sort_by == "price_asc":
        products.sort(key=lambda p: p.price)
    elif sort_by == "price_desc":
        products.sort(key=lambda p: p.price, reverse=True)
    elif sort_by == "rating":
        products.sort(key=lambda p: p.rating, reverse=True)
    elif sort_by == "popular":
        products.sort(key=lambda p: p.popularity_score, reverse=True)

    return products

def get_filter_options():
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