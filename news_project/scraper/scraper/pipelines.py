from apps.news.models import ReportModel
from asgiref.sync import sync_to_async
from .items import ReportItem
from django.core.files.base import ContentFile


class ScraperPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        image_bytes = item.pop('image_bytes')
        image_url = item.pop('image_url').split('/')[-1]
        report = ReportItem(**item).instance

        report.image.save(
            image_url,
            ContentFile(image_bytes),
            save=False
        )

        report.save()

        return item
