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
