import asyncio
from scrapy.utils.reactor import install_reactor
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from ritamdigitalscrapper.spiders.spider import RssSpiderSpider
from twisted.internet import reactor
from scrapy.mail import MailSender

def crawl_job():
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    print("crawl job ritam.com")

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(RssSpiderSpider)

def schedule_next_crawl(null,sleep_time):

    """
    Schedule the next crawl
    """
    print('sleeping for 5 min----------------------')
    reactor.callLater(sleep_time*60, crawl)

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
    error_message = str(failure.value)

    mailer.send(
        to=["kanika.meliorist@gmail.com"],
        subject="Market Status Scrapy Error",
        body=error_message
    )

    print("Error")
    print(error_message)

if __name__=="__main__":
    print("enter in main")
    crawl()
    reactor.run()
