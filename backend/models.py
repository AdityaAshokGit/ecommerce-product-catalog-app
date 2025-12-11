from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List, Optional, Any
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    """
    Base model that automatically converts snake_case (Python)
    to camelCase (JSON) for the frontend.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class Product(CamelModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    brand: str
    rating: float
    in_stock: bool
    image_url: str
    tags: List[str] = []
    
    # This field isn't in the JSON, but we will calculate it.
    # We default to 0 so the model doesn't crash on load.
    popularity_score: int = 0

class OrderItem(CamelModel):
    product_id: str
    quantity: int
    price: float

class Order(CamelModel):
    order_id: str
    date: str  # We keep as string for simplicity, or use datetime
    customer_id: str
    items: List[OrderItem]
    total: float