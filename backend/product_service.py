from typing import List, Optional, Dict, Set, Any
from backend.models import Product
from backend.database import get_all_products
import re
import traceback

# --- INVERTED INDEX STORAGE ---
SEARCH_INDEX: Dict[str, Set[str]] = {}
IS_INDEX_BUILT = False

# --- NORMALIZATION LOGIC ---
def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = str(text).lower() # Ensure string
    text = re.sub(r'[^\w\s]', ' ', text)
    return " ".join(text.split())

def normalize_tokens(text: str) -> Set[str]:
    normalized = normalize_text(text)
    return set(normalized.split())

def normalize_key(text: str) -> str:
    return normalize_text(text)

# --- INDEXING LOGIC ---
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
    if not IS_INDEX_BUILT or not SEARCH_INDEX:
        build_search_index(all_products)
    
    query_tokens = normalize_tokens(query)
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

# --- MAIN SERVICES ---

def filter_products(
    search: Optional[str] = None,
    categories: Optional[List[str]] = None,
    brands: Optional[List[str]] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None,
    availability: Optional[str] = None,
    page: int = 1,   
    limit: int = 15   
    ) -> Dict[str, Any]:   
    
    products = get_all_products()

    if search and search.strip():
        products = search_with_index(search, products)

    if categories:
        target_cats = {normalize_key(c) for c in categories}
        products = [p for p in products if normalize_key(p.category) in target_cats]
    
    if brands:
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

    if sort_by == "price_asc":
        products.sort(key=lambda p: p.price)
    elif sort_by == "price_desc":
        products.sort(key=lambda p: p.price, reverse=True)
    elif sort_by == "rating":
        products.sort(key=lambda p: p.rating, reverse=True)
    elif sort_by == "popular":
        products.sort(key=lambda p: p.popularity_score, reverse=True)

    total_count = len(products)
    start = (page - 1) * limit
    end = start + limit
    paginated_items = products[start:end]

    return {
        "items": paginated_items,
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit
    }

def get_faceted_metadata(
    search: Optional[str] = None,
    categories: Optional[List[str]] = None,
    brands: Optional[List[str]] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    availability: Optional[str] = None
) -> Dict[str, Any]:
    
    all_products = get_all_products()
    
    # 1. Base Context: Search
    if search and search.strip():
        base_products = search_with_index(search, all_products)
    else:
        base_products = all_products

    # 2. Global Filters Helper
    # Added ignore_price flag to help with the fix
    def apply_filters(products_list, ignore_avail=False, ignore_price=False):
        filtered = products_list
        
        # Apply Availability (unless ignored)
        if availability and not ignore_avail:
            if availability == "in-stock":
                filtered = [p for p in filtered if p.in_stock]
            elif availability == "sold-out":
                filtered = [p for p in filtered if not p.in_stock]
        
        # Apply Price (unless ignored)
        if not ignore_price:
            if min_price is not None:
                filtered = [p for p in filtered if p.price >= min_price]
            if max_price is not None:
                filtered = [p for p in filtered if p.price <= max_price]
        
        return filtered

    # Standard Global Context (Includes Price & Avail) - Used for Brands/Cats
    global_context = apply_filters(base_products)

    # --- A. BRAND COUNTS (Ignore Brand Filter) ---
    brand_calc_context = global_context
    if categories:
        target_cats = {normalize_key(c) for c in categories}
        brand_calc_context = [p for p in brand_calc_context if normalize_key(p.category) in target_cats]

    brand_counts = {}
    for p in brand_calc_context:
        brand_counts[p.brand] = brand_counts.get(p.brand, 0) + 1
    
    brand_facets = [
        {"name": k, "count": v} 
        for k, v in sorted(brand_counts.items())
    ]

    # --- B. CATEGORY COUNTS (Ignore Category Filter) ---
    cat_calc_context = global_context
    if brands:
        target_brands = {normalize_key(b) for b in brands}
        cat_calc_context = [p for p in cat_calc_context if normalize_key(p.brand) in target_brands]

    cat_counts = {}
    for p in cat_calc_context:
        cat_counts[p.category] = cat_counts.get(p.category, 0) + 1

    cat_facets = [
        {"name": k, "count": v} 
        for k, v in sorted(cat_counts.items())
    ]

    # --- C. AVAILABILITY COUNTS (Ignore Availability Filter) ---
    avail_context = apply_filters(base_products, ignore_avail=True)
    
    if categories:
        t = {normalize_key(c) for c in categories}
        avail_context = [p for p in avail_context if normalize_key(p.category) in t]
    if brands:
        t = {normalize_key(b) for b in brands}
        avail_context = [p for p in avail_context if normalize_key(p.brand) in t]

    in_stock_count = sum(1 for p in avail_context if p.in_stock)
    sold_out_count = sum(1 for p in avail_context if not p.in_stock)

    avail_facets = [
        {"name": "In Stock", "value": "in-stock", "count": in_stock_count},
        {"name": "Sold Out", "value": "sold-out", "count": sold_out_count}
    ]

    # --- D. PRICE BOUNDS (Ignore Price Filter) ---
    # FIX: We use apply_filters with ignore_price=True
    # This ensures the bounds reflect the "Available Range" based on other filters,
    # NOT the "Selected Range".
    price_context = apply_filters(base_products, ignore_price=True)
    
    if categories:
        t = {normalize_key(c) for c in categories}
        price_context = [p for p in price_context if normalize_key(p.category) in t]
    if brands:
        t = {normalize_key(b) for b in brands}
        price_context = [p for p in price_context if normalize_key(p.brand) in t]

    if price_context:
        prices = [p.price for p in price_context]
        calc_min = min(prices)
        calc_max = max(prices)
    else:
        calc_min = 0
        calc_max = 0

    return {
        "categories": cat_facets,
        "brands": brand_facets,
        "availability": avail_facets,
        "minPrice": calc_min,
        "maxPrice": calc_max
    }
