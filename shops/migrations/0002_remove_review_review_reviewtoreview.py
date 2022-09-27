# Generated by Django 4.1 on 2022-09-19 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review',
        ),
        migrations.CreateModel(
            name='ReviewToReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('review', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.review')),
            ],
        ),
    ]
