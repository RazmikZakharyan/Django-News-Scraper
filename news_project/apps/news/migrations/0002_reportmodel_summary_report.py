# Generated by Django 4.1.2 on 2023-12-10 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportmodel',
            name='summary_report',
            field=models.TextField(null=True),
        ),
    ]
