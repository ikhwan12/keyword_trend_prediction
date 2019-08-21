#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:07:33 2019

@author: ikhwan
"""

import fbprophet
import pandas as pd
from pytrends.request import TrendReq
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
#from fbprophet.diagnostics import cross_validation

def prediction(dir, kw_loc, num, future_period):
    future_period = int(future_period)
    df_kw = pd.read_csv('{}/{}'.format(dir,kw_loc))
    pytrend = TrendReq(hl='en-US',tz=360)
    #kw_list = ['oem product']
    print('(***) Get trend from Google Trend')
    pytrend.build_payload(df_kw.keyword, cat=0, timeframe='today 5-y',geo='US')
    search_df = pytrend.interest_over_time()
    # =============================================================================
    # search_df = pytrend.get_historical_interest(kw_list, year_start=2018, month_start=7,
    #                                             year_end=2019, month_end=7, hl='zh-TW',
    #                                             geo='TW')
    # =============================================================================
    
    #import data
    data = search_df
    if 'isPartial' in data.columns:
        data = data.drop(['isPartial'], axis=1)
    data.to_csv('lll.csv')
    data = pd.read_csv('lll.csv')
    df = pd.DataFrame()
    ctr = 0
    df_kw_pred = pd.DataFrame()
    #df_cv = []
    df_cv = pd.DataFrame({'keyword':[], 'R2':[],
                              'MSE':[], 'MAE':[]})
    for name in data.columns.values[1:]:
        results = []
        df['ds'] = data['date']
        df['id'] = data['date']
        df['y'] = data[name]
        df.loc[:,'y'] = data.loc[:,name]
        df.set_index('id')
        m = fbprophet.Prophet(seasonality_mode='multiplicative', mcmc_samples = 300)
        m.fit(df)
        future = m.make_future_dataframe(periods=future_period,freq='M')
        forecast = m.predict(future)
        m.plot(forecast,xlabel='Date', ylabel='Interest of {}'.format(name));
        metric_df = forecast.set_index('ds')[['yhat']].join(df.set_index('ds').y).reset_index()
        metric_df.dropna(inplace=True)
        arr_r2 = r2_score(metric_df.y, metric_df.yhat)
        arr_mse = mean_squared_error(metric_df.y, metric_df.yhat)
        arr_mae = mean_absolute_error(metric_df.y, metric_df.yhat)
        df_cv = df_cv.append({'keyword':name, 'R2':arr_r2,
                              'MSE':arr_mse, 'MAE':arr_mae}, ignore_index=True)
        df_cv.to_csv('{}/cv_{}.csv'.format(dir,num))
        ff = forecast.yhat.values
        for i in ff[:] :
            results.append(int(i))
        df_kw_pred = pd.DataFrame({name : results}) if ctr == 0 else pd.concat([df_kw_pred,pd.DataFrame({name : results})],axis=1, sort=False)
        ctr+=1
    return df_kw_pred
