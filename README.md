# Web-Crawler

For scraping scrapy framework was chosen. As for the IDE, Pycharm was used to start the scrapy project and then uploaded here in github.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/28462792-2769-4846-8b8f-64e36d155f6f" />



For API, FastAPI was used and as for database, MongoDB is selected.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e00ae3db-b42c-431c-a4ef-93a3f7400104" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/44c7b4c2-3eb7-445b-9df7-db730883a7c0" />

The API endpoints are configured to follow the requirements of the project

# Running
To setup, clone this repository and download project dependencies.

Check and update .env to your liking. However, test credentials for test crawling is provided using an empty MongoDB database. 

In the terminal, run API using "uvicorn main:app --reload"
run scraper in the /scrape endpoint

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a65c7045-c6a6-4a8e-a575-43bdb6b9e16b" />


scheduler is configured to start every 24 hours

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6857cef5-1ae5-4bad-bede-262e6179fb4a" />


Crawled data sample in FastAPI endpoint

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e047401b-6f97-4df3-bea3-372b46859a24" />
