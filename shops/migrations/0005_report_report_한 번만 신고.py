# Generated by Django 4.1 on 2022-09-22 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0004_cert_active_cert_quantity_alter_cert_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_user', to=settings.AUTH_USER_MODEL)),
                ('reported_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='report',
            constraint=models.UniqueConstraint(fields=('report_user', 'reported_user'), name='한 번만 신고'),
        ),
    ]
