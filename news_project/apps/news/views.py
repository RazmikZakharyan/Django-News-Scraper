import requests

from django.views.generic import TemplateView
from config.settings import CHATGPT_API_KEY

from .models import ReportModel
from .tasks import scrapy_task


class ScrapeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not ReportModel.objects.all().exists():
            scrapy_task.delay()

        reports = []
        reports_text = []
        for report in ReportModel.objects.all().values():
            sub_text = report['sub_text']
            report['sub_text'] = self.limit_to_50_words(sub_text)
            if len(reports_text) == 5:
                report['summary_report'] = self.get_summary_report(
                    ' '.join(reports_text)
                )
                reports_text = []

            reports_text.append(sub_text)
            reports.append(report)

        if reports_text:
            reports[-1]['summary_report'] = self.get_summary_report(
                    ' '.join(reports_text)
                )

        return self.render_to_response(
            {
                'reports': reports
            }
        )

    @staticmethod
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
        return response.json()['choices'][0]['message']['content']

    @staticmethod
    def limit_to_50_words(text):
        words = text.split()
        limited_words = ' '.join(words[:50])
        return limited_words
