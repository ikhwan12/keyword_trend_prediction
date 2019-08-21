#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:12:19 2019

@author: ikhwan
"""

import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
from time import clock
import pandas as pd

# starting url. replace google with your own url.
#starting_url = 'https://www.anthemusb.com/'
iterate = ['pet_care']
for name in iterate :
    email_coll = []
    time_limit = 2
    
    web_list = pd.read_csv('{}.csv'.format(name))
    
    for index, starting_url in web_list.iterrows():
        # a queue of urls to be crawled
        unprocessed_urls = deque([starting_url['web_url']])
        
        # set of already crawled urls for email
        processed_urls = set()
        
        # a set of fetched emails
        emails = set()
        
        start = clock()
        temp = []
        str_temp = ''
        start = clock()
        # process urls one by one from unprocessed_url queue until queue is empty
        while len(unprocessed_urls):
            # move next url from the queue to the set of processed urls
            url = unprocessed_urls.popleft()
            processed_urls.add(url)
        
            # extract base url to resolve relative links
            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
            # get url's content
            print("Crawling URL %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
                # ignore pages with errors and continue with next url
                continue
            end = clock()
            if end - start >= time_limit:
                break
            # extract all email addresses and add them into the resulting set
            # You may edit the regular expression as per your requirement
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)
            print(emails)
            
            # create a beutiful soup for the html document
            soup = BeautifulSoup(response.text, 'lxml')
        
            # Once this document is parsed and processed, now find and process all the anchors i.e. linked urls in this document
            for anchor in soup.find_all("a"):
                # extract link url from the anchor
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                # resolve relative links (starting with /)
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                # add the new url to the queue if it was not in unprocessed list nor in processed list yet
                if not link in unprocessed_urls and not link in processed_urls:
                    unprocessed_urls.append(link)
                end = clock()
                if end - start >= time_limit:
                    break
            end = clock()
            if end - start >= time_limit:
                break
        for i in range(len(emails)):
            str_temp = '{}  {}'.format(str_temp,emails.pop())
        email_coll.append(str_temp)
        
    df_save = pd.DataFrame({'URL':list(web_list.web_url),'Email':email_coll})
    df_save.to_csv('{}_email_list.csv'.format(name))

        