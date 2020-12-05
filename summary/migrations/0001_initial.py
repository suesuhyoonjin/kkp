# Generated by Django 3.1.3 on 2020-11-26 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=1000, null=True)),
                ('category_name', models.CharField(max_length=1000, null=True)),
                ('summary_name', models.TextField(null=True)),
                ('publisher_name', models.CharField(max_length=1000, null=True)),
                ('url', models.CharField(max_length=4000, null=True)),
                ('date', models.DateTimeField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d', verbose_name='썸네일')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]