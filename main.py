#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:29:16 2019

@author: ikhwan
"""

from keyword_extractor import extract
from trend import prediction
import pandas as pd
import os

dir = 'save_temp'
list_name = 'pet_care'

#remove all files in save_temp
for filename in os.listdir(dir):
    if filename.endswith(".csv"):
        os.remove('{}/{}'.format(dir,filename))

#extract the keywords
extract(list_name)

#load extracted keywords into the prediction
ctr = 0
for filename in os.listdir(dir):
    print(filename)
    if filename.endswith(".csv"):
        if ctr == 0:
            df = prediction(dir,filename)
        else:
            df = pd.concat([df, prediction(dir,filename)], axis=1, sort=False)
        ctr +=1
df.to_csv('{}/keyword_prediction_for_{}.csv'.format(list_name,list_name))
