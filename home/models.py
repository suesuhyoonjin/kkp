from django.db import models
from django.utils import timezone

class StockMktNews(models.Model):
    pk_url = models.CharField(db_column='Pk_url', primary_key=True, max_length=250)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=30)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=999)  # Field name made lowercase.
    contents_summary = models.TextField(db_column='Contents_summary')  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=20)  # Field name made lowercase.
    publisher = models.CharField(db_column='Publisher', max_length=300)  # Field name made lowercase.
    url = models.TextField(db_column='Url')  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StockMktNews'


class Trendingstocks(models.Model):
    timestamp = models.DateTimeField(db_column='Timestamp', primary_key=True)  # Field name made lowercase.
    keyword1 = models.CharField(db_column='Keyword1', max_length=30)  # Field name made lowercase.
    keyword2 = models.CharField(db_column='Keyword2', max_length=30)  # Field name made lowercase.
    keyword3 = models.CharField(db_column='Keyword3', max_length=30)  # Field name made lowercase.
    keyword4 = models.CharField(db_column='Keyword4', max_length=30)  # Field name made lowercase.
    keyword5 = models.CharField(db_column='Keyword5', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrendingStocks'


class Trendingissues(models.Model):
    issue1 = models.CharField(db_column='Issue1', max_length=100)  # Field name made lowercase.
    issue2 = models.CharField(db_column='Issue2', max_length=100)  # Field name made lowercase.
    issue3 = models.CharField(db_column='Issue3', max_length=100)  # Field name made lowercase.
    issue4 = models.CharField(db_column='Issue4', max_length=100)  # Field name made lowercase.
    issue5 = models.CharField(db_column='Issue5', max_length=100)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrendingIssues'


# python manage.py inspectdb 와우!!
