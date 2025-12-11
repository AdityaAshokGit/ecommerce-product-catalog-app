from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from contextlib import asynccontextmanager # NEW IMPORT

# Import the new logic functions
from backend.product_service import filter_products, get_faceted_metadata
from backend.database import load_data, get_recommended_product_ids, get_all_products
from backend.models import Product

# --- FIX: LIFESPAN HANDLER (Replaces @app.on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load data on startup
    load_data()
    yield
    # Clean up on shutdown (if needed)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/products")
def get_products(
    q: str = Query(None),
    category: List[str] = Query(None),
    brand: List[str] = Query(None),
    minPrice: float = Query(None),
    maxPrice: float = Query(None),
    sort: str = Query(None),
    availability: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100)
):
    return filter_products(
        search=q,
        categories=category,
        brands=brand,
        min_price=minPrice,
        max_price=maxPrice,
        sort_by=sort,
        availability=availability,
        page=page,
        limit=limit
    )

@app.get("/api/metadata")
def get_metadata(
    q: str = Query(None),
    category: List[str] = Query(None),
    brand: List[str] = Query(None),
    minPrice: float = Query(None),
    maxPrice: float = Query(None),
    availability: str = Query(None)
):
    return get_faceted_metadata(
        search=q,
        categories=category,
        brands=brand,
        min_price=minPrice,
        max_price=maxPrice,
        availability=availability
    )

@app.get("/api/products/{product_id}/recommendations", response_model=List[Product])
def get_recommendations(product_id: str):
    rec_ids = get_recommended_product_ids(product_id, limit=3)
    all_products = get_all_products()
    recs = [p for p in all_products if p.id in rec_ids]
    return recs