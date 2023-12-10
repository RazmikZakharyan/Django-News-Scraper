import requests

from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scraper.scraper.spiders.report_spider import ReportSpider
from scrapy import signals

from config.settings import CHATGPT_API_KEY
from .models import ReportModel


def get_summary_report(report_text):
    chatgpt_api_url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
    }
    data = {
        'messages': [
            {
                'role': 'system',
                'content': 'Summarize the following report.'
            },
            {'role': 'user', 'content': report_text}],
        "model": "gpt-3.5-turbo"
    }
    response = requests.post(chatgpt_api_url, headers=headers, json=data)
    response_data = response.json()
    if response_data.get('choices'):
        return response.json()['choices'][0]['message']['content']
    return "Try later"


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

    reports_text = []
    report = None
    for result in results:
        report = ReportModel(**result)
        if len(reports_text) == 5:
            report.summary_report = get_summary_report(
                ' '.join(reports_text)
            )
            reports_text = []

        report.save()
        reports_text.append(result.get('sub_text'))

    if reports_text and report:
        report.summary_report = get_summary_report(
            ' '.join(reports_text)
        )

    return True
