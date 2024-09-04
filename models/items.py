from pydantic import BaseModel
from typing import Optional


# Product Creation Schema
class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    inventory_count: int
    category: Optional[str]


# Product Update Schema
class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    inventory_count: Optional[int]
    category: Optional[str]
