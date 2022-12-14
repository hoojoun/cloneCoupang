# Generated by Django 4.1 on 2022-09-26 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0010_report_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('blacklist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blacklist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
