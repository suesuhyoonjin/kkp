from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from summary.models import Summary
import matplotlib.pyplot as plt
import io
import urllib, base64
import matplotlib.pyplot as plt
import re
import pymysql
import functools
import operator
import requests

from rest_framework import generics, serializers
from rest_framework.response import Response
from .models import StockMktNews, Trendingstocks, Trendingissues

class StockMktNewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMktNews
        fields = ('section', 'title', 'contents_summary', 'category', 'publisher', 'url', 'timestamp')


class StockMktNewsListView(generics.ListAPIView):
    queryset = StockMktNews.objects.all().order_by('-timestamp')
    serializer_class = StockMktNewsListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class KeywordsNewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMktNews
        fields = ('section', 'title', 'contents_summary', 'category', 'publisher', 'url', 'timestamp')


class KeywordsNewsListView(generics.ListAPIView):
    queryset = StockMktNews.objects.all().order_by('-timestamp')
    serializer_class = KeywordsNewsListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class TrendingstocksListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trendingstocks
        fields = ('timestamp', 'keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5')


class TrendingissuesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trendingissues
        fields = ('issue1', 'issue2', 'issue3', 'issue4', 'issue5', 'timestamp')

@login_required
def home_page(request):
    # Summary 내용
    qs = StockMktNews.objects.all().order_by('-timestamp')[:10]
    ts = Trendingstocks.objects.all().order_by('-timestamp')[:1]
    ti = Trendingissues.objects.all().order_by('-timestamp')[:1]

    con = pymysql.connect(host='127.0.0.1', port = 3306, user='suejin', password='10230717', charset='utf8')
    cur = con.cursor()
    cur.execute("use stockwatch")
    cur.execute("select * from TrendingIssues ORDER BY Timestamp DESC LIMIT 1")
    issues_list = list(cur.fetchall())

    issue1 = str(functools.reduce(operator.add, (issues_list[0][0]))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    issue2 = str(functools.reduce(operator.add, (issues_list[0][1]))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    issue3 = str(functools.reduce(operator.add, (issues_list[0][2]))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    issue4 = str(functools.reduce(operator.add, (issues_list[0][3]))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    issue5 = str(functools.reduce(operator.add, (issues_list[0][4]))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')

    kn1 = StockMktNews.objects.filter(contents_summary__contains = '{}'.format(issue1)).order_by('-timestamp')[:15]
    kn2 = StockMktNews.objects.filter(contents_summary__contains = '{}'.format(issue2)).order_by('-timestamp')[:15]
    kn3 = StockMktNews.objects.filter(contents_summary__contains = '{}'.format(issue3)).order_by('-timestamp')[:15]
    kn4 = StockMktNews.objects.filter(contents_summary__contains = '{}'.format(issue4)).order_by('-timestamp')[:15]
    kn5 = StockMktNews.objects.filter(contents_summary__contains = '{}'.format(issue5)).order_by('-timestamp')[:15]

    # 오늘 스톡워치 기사 개수
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

    # Trending Keyword List
    cur.execute("select * from TrendingStocks ORDER BY Timestamp DESC LIMIT 1")
    keywords_list = list(cur.fetchall())

    # Keyword Names
    query1 = "select Name_Eng FROM StockCode WHERE StockCode.Code = '{}'".format(keywords_list[0][1])
    cur.execute(query1)
    keyword1_name = list(cur.fetchall())
    try:
        keyword1_name = str(functools.reduce(operator.add, (keyword1_name))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    except:
        keyword1_name = '신규 상장!'

    query2 = "select Name_Eng FROM StockCode WHERE StockCode.Code = '{}'".format(keywords_list[0][2])
    cur.execute(query2)
    keyword2_name = list(cur.fetchall())
    try:
        keyword2_name = str(functools.reduce(operator.add, (keyword2_name))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    except:
        keyword2_name = '신규 상장!'

    query3 = "select Name_Eng FROM StockCode WHERE StockCode.Code = '{}'".format(keywords_list[0][3])
    cur.execute(query3)
    keyword3_name = list(cur.fetchall())
    try:
        keyword3_name = str(functools.reduce(operator.add, (keyword3_name))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    except:
        keyword3_name = '신규 상장!'

    query4 = "select Name_Eng FROM StockCode WHERE StockCode.Code = '{}'".format(keywords_list[0][4])
    cur.execute(query4)
    keyword4_name = list(cur.fetchall())
    try:
        keyword4_name = str(functools.reduce(operator.add, (keyword4_name))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    except:
        keyword4_name = '신규 상장!'

    query5 = "select Name_Eng FROM StockCode WHERE StockCode.Code = '{}'".format(keywords_list[0][5])
    cur.execute(query5)
    keyword5_name = list(cur.fetchall())
    try:
        keyword5_name = str(functools.reduce(operator.add, (keyword5_name))).replace('(', '').replace(')', '').replace("'", '').replace(",", '')
    except:
        keyword5_name = '신규 상장!'

    url1 = 'https://finance.yahoo.com/quote/{}?p={}'.format(str(keywords_list[0][1]).replace('(', '').replace(')', '').replace("'", ''), str(keywords_list[0][1]).replace('(', '').replace(')', '').replace("'", ''))
    url2 = 'https://finance.yahoo.com/quote/{}?p={}'.format(str(keywords_list[0][2]).replace('(', '').replace(')', '').replace("'", ''), str(keywords_list[0][2]).replace('(', '').replace(')', '').replace("'", ''))
    url3 = 'https://finance.yahoo.com/quote/{}?p={}'.format(str(keywords_list[0][3]).replace('(', '').replace(')', '').replace("'", ''), str(keywords_list[0][3]).replace('(', '').replace(')', '').replace("'", ''))
    url4 = 'https://finance.yahoo.com/quote/{}?p={}'.format(str(keywords_list[0][4]).replace('(', '').replace(')', '').replace("'", ''), str(keywords_list[0][4]).replace('(', '').replace(')', '').replace("'", ''))
    url5 = 'https://finance.yahoo.com/quote/{}?p={}'.format(str(keywords_list[0][5]).replace('(', '').replace(')', '').replace("'", ''), str(keywords_list[0][5]).replace('(', '').replace(')', '').replace("'", ''))

    # 모아서 출력!
    context = {'StockMktNews_list': qs,  'today_articles': today_articles,
               'cum_articles': cum_articles, 'today_publishers': today_publishers, 'Trendingstocks_list': ts, 'Trendingissues_list': ti,
               'keyword1_name': keyword1_name, 'keyword2_name': keyword2_name, 'keyword3_name': keyword3_name,
               'keyword4_name': keyword4_name, 'keyword5_name': keyword5_name,
               'url1': url1, 'url2': url2, 'url3': url3, 'url4': url4, 'url5': url5,
               'kn1': kn1, 'kn2': kn2, 'kn3': kn3, 'kn4': kn4, 'kn5': kn5,
                }
    return render(request, "home/index.html", context)