from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    title: str
    description: str
    category: str
    inc_tax: float
    exc_tax: float
    availability: int
    reviews: int
    img_url: str
    rating: int
    _id: str
    crawl_date: datetime
    status: int


class SortOptions(str, Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    ratings_asc = "ratings_asc"
    ratings_desc = "ratings_desc"
    reviews_asc = "reviews_asc"
    reviews_desc = "reviews_desc"