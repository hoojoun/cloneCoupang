# Generated by Django 4.1 on 2022-09-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0011_blacklisthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasehistory',
            name='Delivery',
            field=models.BooleanField(null=True),
        ),
    ]
