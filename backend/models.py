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
    id: str = Field(min_length=1, description="Unique product identifier")
    name: str = Field(min_length=1, max_length=500, description="Product name")
    description: str = Field(max_length=5000, description="Product description")
    price: float = Field(ge=0, le=1000000, description="Product price")
    category: str = Field(min_length=1, max_length=100, description="Product category")
    brand: str = Field(min_length=1, max_length=100, description="Product brand")
    rating: float = Field(ge=0, le=5, description="Product rating")
    in_stock: bool = Field(description="Stock availability")
    image_url: str = Field(description="Product image URL")
    tags: List[str] = Field(default_factory=list, description="Product tags")
    
    # This field isn't in the JSON, but we will calculate it.
    # We default to 0 so the model doesn't crash on load.
    popularity_score: int = Field(default=0, ge=0, description="Popularity score")

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