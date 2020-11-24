import urllib.request
from bs4 import BeautifulSoup

response = urllib.request.urlopen('https://www.walmart.com/reviews/product/709776123?page1')
html = response.read()

soup = BeautifulSoup(html)

print(soup.find_all('div', {"class" : "Rating"}, {"class" : "Date"}, {"class" : "Comment"}))