from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from summary.models import Summary
import matplotlib.pyplot as plt
import io
import urllib, base64
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
import nltk
# nltk.download('stopwords')
import pymysql
import functools
import operator
import requests


@login_required
def archive_page(request):
    # Summary 내용
    qs = StockMktNews.objects.all().order_by('-timestamp')

    # 오늘 스톡워치 기사 개수
    con = pymysql.connect(host='127.0.0.1', port = 3306, user='suejin', password='10230717', charset='utf8')
    cur = con.cursor()
    cur.execute("use stockwatch")
    cur.execute("SELECT Contents_summary FROM StockMktNews WHERE Timestamp > SUBDATE(Now(), INTERVAL 1 DAY)")
    articles = list(cur.fetchall())
    today_articles = len(articles)

    # 지금까지 스톡워치 기사 개수
    cur.execute("SELECT Contents_summary FROM StockMktNews")
    articles2 = list(cur.fetchall())
    cum_articles = len(articles2)

    # 오늘 스톡워치가 분석한 신문사는?
    cur.execute("SELECT Publisher FROM StockMktNews WHERE Timestamp > SUBDATE(Now(), INTERVAL 1 DAY)")
    articles3 = list(cur.fetchall())
    today_publishers = len(set(articles3))

    # 모아서 출력!
    context = {'StockMktNews_list': qs, 'today_articles': today_articles,
               'cum_articles': cum_articles, 'today_publishers': today_publishers}
    return render(request, "archive/index.html", context)


from rest_framework import generics, serializers
from rest_framework.response import Response
from .models import StockMktNews

class StockMktNewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMktNews
        fields = ('section', 'title', 'contents_summary', 'category', 'publisher', 'url', 'timestamp')