from django.views.generic import TemplateView

from .models import ReportModel
from .tasks import scrapy_task


class ScrapeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not ReportModel.objects.all().exists():
            scrapy_task.delay()

        reports = []
        for report in ReportModel.objects.all().values():
            sub_text = report['sub_text']
            report['sub_text'] = self.limit_to_50_words(sub_text)
            reports.append(report)

        return self.render_to_response(
            {
                'reports': reports
            }
        )

    @staticmethod
    def limit_to_50_words(text):
        words = text.split()
        limited_words = ' '.join(words[:50])
        return limited_words
