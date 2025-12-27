# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
from urllib.parse import urljoin
from datetime import datetime
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from utilities.settings import MONGO_URI, MONGO_DATABASE

class BookcrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strings --> remove white spaces from strings except description and non-string fields
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name not in ['description', 'status', 'crawl_date', '_id']:
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Prices --> remove special characters in prices and convert to float
        price_keys = ['exc_tax', 'inc_tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ## Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        ## Reviews --> convert string to number
        reviews_string = adapter.get('reviews')
        adapter['reviews'] = int(reviews_string)

        ## Image URL --> join the base url to taken url
        base_url = 'https://books.toscrape.com/'
        image_url = adapter.get('img_url')
        adapter['img_url'] = urljoin(base_url, image_url)

        ## Rating --> remove star-rating and convert text to number
        stars_string = adapter.get('rating')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['rating'] = 0
        elif stars_text_value == "one":
            adapter['rating'] = 1
        elif stars_text_value == "two":
            adapter['rating'] = 2
        elif stars_text_value == "three":
            adapter['rating'] = 3
        elif stars_text_value == "four":
            adapter['rating'] = 4
        elif stars_text_value == "five":
            adapter['rating'] = 5

        return item

class MongoPipeline:
    COLLECTION_NAME = "books"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.COLLECTION_NAME]

    def process_item(self, item, spider):
        item_id = self.compute_item_id(item)
        if self.collection.find_one({"_id": item_id}):
            changes = self.detect_changes(item, item_id)
            if changes:
                self.log_changes(item_id, changes)
                # Update the existing document
                self.collection.update_one({'_id': item_id}, {'$set': item})
        else:
            item["_id"] = item_id
            self.collection.insert_one(ItemAdapter(item).asdict())
            return item

    def compute_item_id(self, item):
        url = item["url"]
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def detect_changes(self, current_item, existing_item):
        changes = {}
        for field, value in current_item.items():
            if field in existing_item and existing_item[field] != value:
                changes[field] = {
                    'old': existing_item[field],
                    'new': value
                }
        return changes

    def log_changes(self, unique_id, changes):
        # Store changes in a separate log collection
        log_entry = {
            'product_id': unique_id,
            'timestamp': datetime.now(),
            'changes': changes
        }
        self.db['changelog'].insert_one(log_entry)


