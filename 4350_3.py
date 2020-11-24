# -*- coding: utf-8 -*-
"""4350.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10fvMyRX_j-B488xQYzylTIfUJ1NS6tJe
"""

import requests 
from selectorlib import Extractor
from dateutil import parser as dateinterpreter
import json 
from time import sleep
import csv

# Scrape more Amazon product reviews and save it to csv file.
# Import numbers of libraries in advance.
# Including requests, Extractor, parser, json, sleep, csv.

# The Url combination, by observing the similarity of different comment url pages.
url7 = "https://www.amazon.com/Nintendo-Switch-Lite-Turquoise/product-reviews/B07V4GCFP9/ref=cm_cr_dp_d_show_all_btm"
url8 = "?ie=UTF8&pageNumber="
url9 = "&reviewerType=all_reviews"

# Read the YAML file and make Extractor.
e = Extractor.from_yaml_file('selectors.yml')

# To access amazon.
def webscraping(webpageUrl3):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Print the downloading message out.
    print("Downloading %s"%webpageUrl3)
    abc3 = requests.get(webpageUrl3, headers=headers)
    # This is to check whether the pages are blocked or not (Usually 503).
    if abc3.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in abc2.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%webpageUrl2)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(webpageUrl2,abc2.status_code))
        return None
    # Pass the HTML of the page and create.
    return e.extract(abc3.text)

# Creating list of urls by adding the page number using 'for' loop.
with open('website3.txt','w') as outfile:
    for i in range (1,200):
        outfile.write(url7 + str(i) + url8 + str(i) + url9 + '\n')

# Save results to the csv file and paste the content one by one.
with open("website3.txt",'r') as urllist, open('data3.csv','w') as outfile:
    writer3 = csv.DictWriter(outfile, fieldnames=["rating","date","content","title","variant","images","verified","author","product","url"],quoting=csv.QUOTE_ALL)
    writer3.writeheader()
    for webpageUrl3 in urllist.readlines():
        temp3 = webscraping(webpageUrl3)
        if temp3:
            if temp3['reviews'] is not None:
                for abc3 in temp3['reviews']:
                    abc3["product"] = temp3["product_title"]
                    abc3['url'] = webpageUrl3
                    abc3['rating'] = abc3['rating'].split(' out of')[0]
                    date_posted = abc3['date'].split('on ')[-1]
                    if abc3['images']:
                        abc3['images'] = "\n".join(abc3['images'])
                    abc3['date'] = dateinterpreter.parse(date_posted).strftime('%d-%b-%Y')
                    writer3.writerow(abc3)
                #sleep(1000)