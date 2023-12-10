from django.db import models


class ReportModel(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='report_image/%Y/%m/%d/')
    text = models.TextField()
    sub_text = models.TextField()
    summary_report = models.TextField(null=True)
