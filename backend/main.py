from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import load_data, get_all_products
from backend.product_service import filter_products, get_filter_options
from typing import List
from backend.database import load_data, get_recommended_product_ids, get_all_products
from backend.models import Product

# Lifecycle event to load data on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load data
    load_data()
    yield
    # Shutdown: Clean up (nothing to do here)

app = FastAPI(title="E-commerce API", lifespan=lifespan)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/api/products")
def get_products(
    q: str = Query(None, description="Search query"),
    category: List[str] = Query(None), # Accepts ?category=A&category=B
    brand: List[str] = Query(None),    # Accepts ?brand=A&brand=B
    minPrice: float = Query(None),
    maxPrice: float = Query(None),
    sort: str = Query(None, pattern="^(price_asc|price_desc|rating|popular)$")
):
    """
    Returns filtered and sorted products.
    """
    return filter_products(
        search=q,
        categories=category,
        brands=brand,
        min_price=minPrice,
        max_price=maxPrice,
        sort_by=sort
    )

@app.get("/api/metadata")
def get_metadata():
    """
    Returns available filter options (categories, brands) for the sidebar.
    """
    return get_filter_options()

@app.get("/api/products/{product_id}/recommendations", response_model=List[Product])
def get_recommendations(product_id: str):
    """
    Returns top 3 products frequently bought with the given product.
    """
    # 1. Get IDs from the Graph (O(1) lookup + Sort)
    rec_ids = get_recommended_product_ids(product_id, limit=3)
    
    # 2. Resolve IDs to full Product objects
    # In a DB, this would be `SELECT * WHERE ID IN (...)`
    # Here, we scan the list. O(N) but negligible for N=2000.
    all_products = get_all_products()
    
    # Filter to get the full objects
    recs = [p for p in all_products if p.id in rec_ids]
    
    return recs