from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.bookspider import BookCrawler

def get_jobs(sched):
    jobs = sched.get_jobs()
    print("Crawler has started again\n")
    for job in jobs:
        print(f"Job ID: {job.id}")
        print(f"Next run time: {job.next_run_time}")
        print(f"Trigger: {job.trigger}")
        print(f"Function: {job.func_ref}\n")

        print("-" * 20 + "\n")

def run_spider():
    scheduler = TwistedScheduler()
    try:
        scheduler.start()
        process = CrawlerProcess(get_project_settings())


        process.crawl(BookCrawler)
        print("Crawler has started\n")

        scheduler.add_job(process.crawl, 'interval', args=[BookCrawler], hours=24)


        get_jobs(scheduler)

        process.start(False)

    except Exception as e:
        print(e)
    finally:
        scheduler.shutdown()

run_spider()