import sys
import os

from scrapy_djangoitem import DjangoItem

sys.path.append(os.path.dirname(os.path.abspath('.')))

from apps.news.models import ReportModel


class ReportItem(DjangoItem):
    django_model = ReportModel
