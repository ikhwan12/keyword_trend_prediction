#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:59:18 2019

@author: ikhwan
"""
import logging
import pandas as pd
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import math
from socket import timeout

delay = 120

def get_data(url_name):
    webpage ='http://www.ourland.com.tw'
    try:
        webpage = urlopen('{}'.format(url_name), timeout=200).read()
    except timeout:
        logging.error('socket timed out - URL %s', url_name)
    except (urllib.error.HTTPError) as err:
        print(err.code)
        if(err.code == 403 or err.code == 104):
            return None
            pass
    except (ConnectionResetError) as err2:
        print(err2)
        return None
        pass
    except urllib.error.URLError as err3:
        print(err3)
        return None
        pass
    soup = BeautifulSoup(webpage, "lxml")
    keyword = soup.find('meta',attrs={"name": "keywords"})
    print(keyword['content'] if keyword else "No meta keyword is given")
    return keyword['content'] if keyword else None

def extract(data):
    kw_list = []
    #kw_list = pd.read_csv('suggested_keywords.csv').values.tolist()
    print('(*) Read data from web list')
    web_list = pd.read_csv('{}.csv'.format(data))
    for index, url in web_list.iterrows():
        print(url['web_url'])
        temp = get_data(url['web_url'])
        if temp != None:
            if temp.count(',') > 0 :
                for t in range(0,temp.count(',')):
                    if(len(temp.split(',')[t])<50):
                        kw_list.append(temp.split(',')[t])
            else:
                kw_list.append(temp.split(',')[0] if temp.find(',') else temp)
    print('(*) Keyword Extracted')
    print('(**) Clean the List')
    temp_list = [x for x in kw_list if x]
    kw_list = temp_list
    kw_list = list(dict.fromkeys(kw_list))
    n_run = math.ceil(len(kw_list)/5)
    for run in range(0,n_run):
        temp = []
        start = run*5
        end = start+4
        for i in range(start,end):
            temp.append(kw_list[i])
        df = pd.DataFrame({'keyword':temp})
        df.to_csv('save_temp/keyword_list_{}.csv'.format(run))    
    print('All keywords files are extracted')
    df = pd.DataFrame({'keyword':kw_list})
    df.to_csv('keyword_list_{}.csv'.format(data))