from apps.news.models import ReportModel
from asgiref.sync import sync_to_async
from .items import ReportItem


class ScraperPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        ReportItem(**item).save()

        return item
