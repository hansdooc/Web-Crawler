from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from utilities.Models import SortOptions
from API.mongodb import connect_to_mongo, close_mongo_connection
import scheduler.scheduler as schedule
import os

load_dotenv()
#change BOOK_COLLECTION to TEST_COLLECTION for test crawling
collection_name = os.getenv("BOOK_COLLECTION")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Application is starting up!")
    global database
    database = await connect_to_mongo()
    yield
    # Shutdown logic
    await close_mongo_connection()
    print("Application is shutting down!")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/all_books")
async def read_items():
    items = await database[collection_name].find().to_list()
    return items

@app.get("/books")
async def get_books(
    category: Optional[str] = Query(None, description="Filter products by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price for filtering"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price for filtering"),
    ratings: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    sort_by: Optional[SortOptions] = Query(None, description="Sort order for books"),
):
    items = database[collection_name]

    products = {}

    if category is not None:
        products["category"] = category
    if min_price is not None:
        products["inc_tax"] = {"$gte": min_price}
    if max_price is not None:
        products["inc_tax"] = {"$lte": max_price}
    if ratings is not None:
        products["rating"] = ratings

    output = items.find(products)

    if sort_by is not None:
        if sort_by == SortOptions.price_asc:
            output.sort({"inc_tax" : 1})
        elif sort_by == SortOptions.price_desc:
            output.sort({"inc_tax" : -1})
        elif sort_by == SortOptions.ratings_asc:
            output.sort({"rating" : 1})
        elif sort_by == SortOptions.ratings_desc:
            output.sort({"rating" : -1})
        elif sort_by == SortOptions.reviews_asc:
            output.sort({"reviews" : 1})
        elif sort_by == SortOptions.reviews_desc:
            output.sort({"reviews" : -1})

    output = await output.to_list()
    return [item for item in output]

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    item = await database[collection_name].find_one({"_id": item_id})
    return item

@app.get("/changes")
async def get_changes():
    change = await database['changelog'].find().to_list()
    return [str(item) for item in change]

@app.get("/scrape/")
async def run_scrape():
    schedule.run_spider()
    return "Scraper is running"