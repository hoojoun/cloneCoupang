# Generated by Django 4.1 on 2022-09-22 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0005_report_report_한 번만 신고'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.review'),
        ),
        migrations.AddField(
            model_name='report',
            name='reviewtoreview',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.reviewtoreview'),
        ),
    ]
