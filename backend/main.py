from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import load_data, get_all_products
from backend.product_service import filter_products, get_filter_options

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
    category: str = Query(None),
    brand: str = Query(None),
    minPrice: float = Query(None),
    maxPrice: float = Query(None),
    sort: str = Query(None, pattern="^(price_asc|price_desc|rating|popular)$")
):
    """
    Returns filtered and sorted products.
    """
    return filter_products(
        search=q,
        category=category,
        brand=brand,
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