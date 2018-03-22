import cv2
import urllib2
from bs4 import BeautifulSoup

URL = "http://www.yahoo.co.jp"
USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
     'AppleWebKit/537.36 (KHTML, like Gecko) '\
     'Chrome/55.0.2883.95 Safari/537.36 '

req = urllib2.Request(URL)
req.add_header("User-agent", USERAGENT)

html = urllib2.urlopen(req)
soup = BeautifulSoup(html, "html.parser")

topicsindex = soup.find('div', attrs= {'class': 'topicsindex'})
topics = topicsindex.find_all('li')

for top in topics:
     print top.find('a').contents[1]











