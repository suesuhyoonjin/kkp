# Generated by Django 3.1.3 on 2020-11-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockSymbolCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_code', models.CharField(blank=True, max_length=200)),
                ('stock_en_name', models.CharField(blank=True, max_length=200)),
                ('stock_ko_name', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
