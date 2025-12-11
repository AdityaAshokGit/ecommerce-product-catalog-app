from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from contextlib import asynccontextmanager
from pydantic import ValidationError
import time

from backend.logger import setup_logging, get_logger
from backend.product_service import filter_products, get_faceted_metadata
from backend.database import load_data, get_recommended_product_ids, get_all_products
from backend.models import Product

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting application...")
    load_data()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.3f}s"
    )
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input data", "errors": exc.errors()}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"Value error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again later."}
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/products")
def get_products(
    q: str = Query(None, max_length=200, description="Search query"),
    category: List[str] = Query(None, description="Filter by categories"),
    brand: List[str] = Query(None, description="Filter by brands"),
    minPrice: float = Query(None, ge=0, le=1000000, description="Minimum price"),
    maxPrice: float = Query(None, ge=0, le=1000000, description="Maximum price"),
    sort: str = Query(None, description="Sort order"),
    availability: str = Query(None, pattern="^(in-stock|sold-out)$", description="Availability filter"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
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
    q: str = Query(None, max_length=200, description="Search query"),
    category: List[str] = Query(None, description="Filter by categories"),
    brand: List[str] = Query(None, description="Filter by brands"),
    minPrice: float = Query(None, ge=0, le=1000000, description="Minimum price"),
    maxPrice: float = Query(None, ge=0, le=1000000, description="Maximum price"),
    availability: str = Query(None, pattern="^(in-stock|sold-out)$", description="Availability filter")
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