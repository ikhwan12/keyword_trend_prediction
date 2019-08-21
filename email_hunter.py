#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:25:24 2019

@author: ikhwan
"""
import pandas as pd
from pyhunter import PyHunter

hunter = PyHunter('c4d2eab17b086e9bbd65531c7b81a0b5e6e4beb7')

web_list = pd.read_csv('pet_care.csv')

for index, url in web_list.iterrows():
    df_profile = pd.DataFrame()
    mailList = hunter.domain_search(url['web_url'])
    #print(email)
    
    for key, value in mailList.items():
        if key == 'emails':
            email = value
            
    for mail in email:
        del mail['sources']
        if df_profile.empty:
            df_profile = pd.DataFrame.from_dict(mail, orient='index')
        else :
            temp = pd.DataFrame.from_dict(mail, orient='index')
            df_profile = pd.concat([df_profile, temp], axis=1, join='inner')
            
    df_save = df_profile.transpose()
    df_save.to_csv('profile_{}.csv'.format(url['web_url']))