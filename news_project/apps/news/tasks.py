from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scraper.scraper.spiders.report_spider import ReportSpider
from scrapy import signals

from twisted.internet import asyncioreactor
# asyncioreactor.install()
from twisted.internet import reactor

from .models import ReportModel


@shared_task
def scrapy_task():
    ReportModel.objects.all().delete()

    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    process = CrawlerProcess(get_project_settings())
    process.crawl(ReportSpider)
    process.start()

    for result in results:
        ReportModel(**result).save()

    return True
