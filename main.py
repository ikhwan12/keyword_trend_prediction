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
import sys

def main(list_name, future_period=12):
    dir = 'save_temp'
    #list_name = 'skincare'
    
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
                df = prediction(dir,filename,ctr, future_period=future_period)
            else:
                df = pd.concat([df, prediction(dir,filename,ctr)], axis=1, sort=False)
            ctr +=1
    df = pd.DataFrame()
    df.to_csv('{}/keyword_prediction_for_{}.csv'.format(list_name,list_name))

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Oops Wrong syntax, refer below:')
        print('python main.py [list name] [future period in week]')
    else :
        try:
            if len(sys.argv) == 3:
                main(sys.argv[1], sys.argv[2])
            else :
                main(sys.argv[1])
        except KeyboardInterrupt:
            print('Aborted')
