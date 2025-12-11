from typing import List, Optional, Dict, Set
from backend.models import Product
from backend.database import get_all_products
import re

# --- INVERTED INDEX STORAGE ---
SEARCH_INDEX: Dict[str, Set[str]] = {}
IS_INDEX_BUILT = False

# --- 1. SEARCH NORMALIZER (Tokenization) ---
def normalize_tokens(text: str) -> Set[str]:
    """
    Splits text into atomic, searchable words.
    
    Logic:
    1. Lowercase.
    2. Replace punctuation with SPACE (Preserves compound word boundaries).
       "All-Clad" -> "all clad"
    3. Split by whitespace.
       Result: {"all", "clad"}
    """
    if not text:
        return set()
    
    text = text.lower()
    # Regex: Replace any character that is NOT a word char or whitespace with a space.
    # This preserves Emojis and foreign scripts (\w includes them in Python 3).
    text = re.sub(r'[^\w\s]', ' ', text)
    
    return set(text.split())

# --- 2. FILTER NORMALIZER (Key Standardization) ---
def normalize_key(text: str) -> str:
    """
    Standardizes a string for strict equality checks in Filters.
    
    Logic:
    1. Lowercase.
    2. Replace punctuation with SPACE.
    3. Collapse multiple spaces into one.
    
    Examples:
    "All-Clad"   -> "all clad"
    "All Clad"   -> "all clad" (Match ✅)
    "the-rest"   -> "the rest"
    "therest"    -> "therest"  (No Collision ✅)
    """
    if not text:
        return ""
    
    text = text.lower()
    # Replace punctuation/symbols with space
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Split and Join to collapse multiple spaces (e.g. "all   clad" -> "all clad")
    return " ".join(text.split())

# --- INDEXING LOGIC ---
def build_search_index(products: List[Product]):
    global SEARCH_INDEX, IS_INDEX_BUILT
    SEARCH_INDEX.clear()
    
    for product in products:
        # Index Name, Description, Brand, and Category
        content = f"{product.name} {product.description} {product.brand} {product.category}"
        tokens = normalize_tokens(content)
        
        for token in tokens:
            if token not in SEARCH_INDEX:
                SEARCH_INDEX[token] = set()
            SEARCH_INDEX[token].add(product.id)
            
    IS_INDEX_BUILT = True

def search_with_index(query: str, all_products: List[Product]) -> List[Product]:
    global IS_INDEX_BUILT
    if not IS_INDEX_BUILT or not SEARCH_INDEX:
        build_search_index(all_products)
    
    query_tokens = normalize_tokens(query)
    
    # If the user's query contained no valid tokens (e.g. "!!!"), return nothing.
    if not query_tokens:
        return []

    candidate_ids: Optional[Set[str]] = None
    
    for token in query_tokens:
        matches = SEARCH_INDEX.get(token, set())
        
        if candidate_ids is None:
            candidate_ids = matches
        else:
            # Intersection: Find products that contain ALL tokens (AND logic)
            candidate_ids = candidate_ids.intersection(matches)
            
        # Optimization: Fail fast if no intersection
        if not candidate_ids:
            return []

    return [p for p in all_products if p.id in candidate_ids]

# --- MAIN SERVICE ---

def filter_products(
    search: Optional[str] = None,
    categories: Optional[List[str]] = None,
    brands: Optional[List[str]] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None,
    availability: Optional[str] = None
) -> List[Product]:
    
    products = get_all_products()

    # 1. SEARCH
    if search:
        if not search.strip():
            # If search is just whitespace, ignore it (return all)
            pass 
        else:
            products = search_with_index(search, products)

    # 2. FILTER (Multi-Select with Robust Normalization)
    if categories:
        # Pre-normalize targets into a Set for O(1) lookup
        target_cats = {normalize_key(c) for c in categories}
        # Check if normalized product category exists in the target set
        products = [p for p in products if normalize_key(p.category) in target_cats]
    
    if brands:
        # Pre-normalize targets
        target_brands = {normalize_key(b) for b in brands}
        products = [p for p in products if normalize_key(p.brand) in target_brands]

    if min_price is not None:
        products = [p for p in products if p.price >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]

    if availability:
        if availability == "in-stock":
            products = [p for p in products if p.in_stock]
        elif availability == "sold-out":
            products = [p for p in products if not p.in_stock]

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