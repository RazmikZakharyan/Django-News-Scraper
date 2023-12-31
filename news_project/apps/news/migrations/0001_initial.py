# Generated by Django 4.1.2 on 2023-12-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('image', models.ImageField(upload_to='report_image/%Y/%m/%d/')),
                ('text', models.TextField()),
                ('sub_text', models.TextField()),
            ],
        ),
    ]
