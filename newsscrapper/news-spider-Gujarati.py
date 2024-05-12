from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from newsscrapper.spiders.news_scrapper import NewsSpiderGujarati
from twisted.internet import reactor
from scrapy.mail import MailSender

# process = CrawlerProcess(get_project_settings())
# process.crawl(NewsSpider)
# process.start()

def crawl_job():
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    print("crawl job Gujarati")

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(NewsSpiderGujarati)

def schedule_next_crawl(null,sleep_time):
    """
    Schedule the next crawl
    """
    print('sleeping for 1 min----------------------')
    reactor.callLater(sleep_time, crawl)

def crawl():
    """
    A "recursive" function that schedules a crawl 30 seconds after
    each successful crawl.
    """
    # crawl_job() returns a Deferred
    d = crawl_job()
    # call schedule_next_crawl(<scrapy response>, n) after crawl job is complete
    d.addCallback(schedule_next_crawl, 1)
    d.addErrback(catch_error)

def catch_error(failure):
    mailer = MailSender()
    mailer.send(to=["kanika.meliorist@gmail.com"], subject="NewsSpider Scrapy Error", body=failure.value)
    print("error")
    print(failure.value)

if __name__=="__main__":
    print("enter in main")
    crawl()
    reactor.run()

