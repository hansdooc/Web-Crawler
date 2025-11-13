from datetime import datetime

import scrapy
from utilities.items import BookItem


class BookCrawler(scrapy.Spider):
    name = 'bookcrawler'
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com/'
    ]

    def parse(self, response, **kwargs):

        book_elements = response.css('article.product_pod')

        for book in book_elements:
            relative_url = book.css('h3 a::attr(href)').get()

            book_url = self.check_catalogue(relative_url)

            yield scrapy.Request(
                book_url,
                callback=self.parse_book_page,
                errback=self.log_error,
            )

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:

            next_page_url = self.check_catalogue(next_page)
            self.logger.info(
                f"Navigating to next page with URL {next_page_url}."
            )
            yield response.follow(next_page_url, callback=self.parse, errback=self.log_error,)

    def parse_book_page(self, response):
        books = response.css('.page_inner')
        book_item = BookItem()


        book_item['title'] = books.css('h1::text').get()
        book_item['description'] = books.css('#product_description+ p::text').get()
        book_item['category'] = books.css('li~ li+ li a::text').get()
        book_item['exc_tax'] = books.css('tr:nth-child(3) td::text').get()
        book_item['inc_tax'] = books.css('tr:nth-child(4) td::text').get()
        book_item['availability'] = books.css('tr:nth-child(6) td::text').get()
        book_item['reviews'] = books.css('tr:nth-child(7) td::text').get()
        book_item['img_url'] = books.css('img::attr(src)').get()
        book_item['rating'] = books.css('p.star-rating').attrib['class']

        #Metadata
        book_item['crawl_date'] = datetime.now().isoformat()
        book_item['url'] = response.url
        book_item['status'] = response.status

        yield book_item

    def check_catalogue(self, relative_url):

        if 'catalogue/' in relative_url:
            book_url = 'https://books.toscrape.com/' + relative_url

        else:
            book_url = 'https://books.toscrape.com/catalogue/' + relative_url

        return book_url

    def log_error(self, failure):
        self.logger.error(repr(failure))