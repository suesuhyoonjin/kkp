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



@login_required
def home_page(request):
    # Summary 내용
    qs = Summary.objects.all()

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

    # # 워드클라우드
    # con = pymysql.connect(host='127.0.0.1', port=3306, user='suejin', password='10230717', charset='utf8')
    # cur = con.cursor()
    # cur.execute("use stockwatch")
    # cur.execute("SELECT Contents_summary FROM StockMktNews WHERE Timestamp > SUBDATE(Now(), INTERVAL 1 DAY)")
    # articles = list(cur.fetchall())
    #
    # texts = []
    # for row in articles:
    #     tmp = functools.reduce(operator.add, (row))
    #     texts.append(tmp)
    #
    # total = []
    # for row in texts:
    #     total.append(row.split())
    #
    # result = []
    # for i in total:
    #     result.extend(i)
    #
    # result2 = []
    # for i in result:
    #     tmp = i.replace('."', ' ').replace('.', ' ')
    #     result2.append(tmp)
    #
    # result3 = ' '.join(result2)
    # result4 = result3.split()
    #
    # tmp = []
    # for item in result4:
    #     tmp.append(re.sub('[".?,*“”:]', '', item))
    #
    # tmp2 = ' '.join(tmp)
    #
    # text_dict = {}
    # for idx, cont in enumerate(tmp):
    #     for word in cont.split():
    #         if (text_dict.get(word) == None):
    #             text_dict[word] = 1
    #         else:
    #             text_dict[word] += 1
    #
    # wc = WordCloud(  # font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc',
    #     width=1000,
    #     height=1000,
    #     background_color="white"
    # )
    # wc = wc.generate_from_frequencies(text_dict)
    #
    # text_list = tmp2.split()
    #
    # from nltk.corpus import stopwords
    # text_no = [w for w in text_list if not w in stopwords.words('english')]
    # stopwords = ['In', 'like', 'could', 'would', 'since', 'also', 'recent', 'the', 'said',
    #              'The', '*', 'U.S.', 'THE', 'market', 'stocks', 'investors', 'company',
    #              'near', 'thursday,', 'stock', 'with', '--', 'monday', 'price',
    #              'tuesday', 'wednesday', 'friday', 'saturday', 'Benzinga', 'shares', 'and',
    #              'Wednesday', 'U', 'today', 'S', 'O', '0', '00', 'bought', 'trader', 'per', 'year',
    #              'higher', 'last', '1', 'A', 'November', '2020', 'companies', 'trading', 'trade', 'growth']
    # text_nostop = [w for w in text_no if not w in stopwords]
    #
    # text_dict = {}
    # for idx, cont in enumerate(text_nostop):
    #     for word in cont.split():
    #         if (text_dict.get(word) == None):
    #             text_dict[word] = 1
    #         else:
    #             text_dict[word] += 1
    #
    # wc = wc.generate_from_frequencies(text_dict)
    #
    # plt.figure(figsize=(10, 10))
    # plt.axis("off")
    # plt.imshow(wc)
    # #image = io.BytesIO()
    # #plt.savefig(image, format='png')
    # plt.savefig('/home/ubuntu/kkp/media/image.png', bbox_inches='tight', pad_inches=0, transparent=True)#, format='png')
    #
    # #image.seek(0)  # rewind the data
    # #string = base64.b64encode(image.read())
    # #image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)

    # 모아서 출력!
    context = {'summary_list': qs,  'today_articles': today_articles,
               'cum_articles': cum_articles, 'today_publishers': today_publishers}

    return render(request, "home/index.html", context)

#
# from rest_framework import generics, serializers
# from rest_framework.response import Response
#
# from .models import wordCloud
#
#
#
# class wordCloudListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = wordCloud
#         fields = ('img', 'created_date')
#
#
# class wordCloudListView(generics.ListAPIView):
#     queryset = wordCloud.objects.all()
#     serializer_class = wordCloudListSerializer
#
#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer_class = self.get_serializer_class()
#         serializer = serializer_class(queryset, many=True)
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         return Response(serializer.data)