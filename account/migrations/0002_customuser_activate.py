# Generated by Django 4.1 on 2022-09-22 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activate',
            field=models.BooleanField(null=True),
        ),
    ]