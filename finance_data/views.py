from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from finance_data.models import StockSymbolCode
import FinanceDataReader as fdr
from django.http import JsonResponse
import json
import pandas as pd
from datetime import datetime, timedelta

# https://financedata.github.io/posts/finance-data-reader-users-guide.html
# https://github.com/FinanceData/FinanceDataReader

@login_required
def get_finance_data(request):
    dates = []
    for i in range(0, 7):
        tmp = (datetime.now() - timedelta(days=7) + timedelta(days=i))
        if tmp.weekday() < 5:
            dates.append(tmp.strftime('%Y-%m-%d'))

    start_date = dates[0]
    end_date = dates[4]

    stock_list = [
        ["S&P 500", "US500"],
        ["NASDAQ Futures", "IXIC"],
        ["DOW Futures", "DJI"],
        ["USD/KRW", "USD/KRW"]
    ]

    df_list = [fdr.DataReader(code, start_date, end_date)['Close'] for name, code in stock_list]
    # print(len(df_list))

    df = pd.concat(df_list, axis=1)
    df.columns = [name for name, code in stock_list]

    us500_df = fdr.DataReader('US500', start_date, end_date)['Close']
    nas_df = fdr.DataReader('IXIC', start_date, end_date)['Close']
    dji_df = fdr.DataReader('DJI', start_date, end_date)['Close']
    usd_krw_df = fdr.DataReader('USD/KRW', start_date, end_date)['Close']

    us500_df = us500_df.to_frame().reset_index()
    nas_df = nas_df.to_frame().reset_index()
    dji_df = dji_df.to_frame().reset_index()
    usd_krw_df = usd_krw_df.to_frame().reset_index()

    # us500_json = us500_df.reset_index().to_json(orient='records')
    # nas_json = nas_df.reset_index().to_json(orient='records')
    # dji_json = dji_df.reset_index().to_json(orient='records')
    # usd_krw_json = usd_krw_df.reset_index().to_json(orient='records')

    # us500_res, nas_res, dji_res, usd_krw_res = []

    us500_df['Date'] = us500_df['Date'].apply(lambda x: x.isoformat())
    us500_json = us500_df.to_dict(orient='records')

    nas_df['Date'] = nas_df['Date'].apply(lambda x: x.isoformat())
    nas_json = nas_df.to_dict(orient='records')

    dji_df['Date'] = dji_df['Date'].apply(lambda x: x.isoformat())
    dji_json = dji_df.to_dict(orient='records')

    usd_krw_df['Date'] = usd_krw_df['Date'].apply(lambda x: x.isoformat())
    usd_krw_json = usd_krw_df.to_dict(orient='records')

    # us500_res = json.loads(us500_json)
    # nas_res = json.loads(nas_json)
    # dji_res = json.loads(dji_json)
    # usd_krw_res = json.loads(usd_krw_json)

    # date1 = dates[0]
    # date2 = dates[1]
    # date3 = dates[2]
    # date4 = dates[3]
    # date5 = dates[4]

    context = {
        'us500': us500_res,
        'nas': nas_res,
        'dji': dji_res,
        'usd_krw': usd_krw_res,
        'start_date': start_date,
        'end_date': end_date,
        # 'dates': dates,
        "result": "success"
    }

    return JsonResponse(context, safe=False)
