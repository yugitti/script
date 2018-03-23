import time
import urllib2
from bs4 import BeautifulSoup
import requests
import pandas as pd

PATH_INPUT_IMAGE_URL = "./images/test/images-face.csv"
PATH_OUT_IMAGE = "./images/test/img/"

# URL = "http://www.yahoo.co.jp"
# USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
#      'AppleWebKit/537.36 (KHTML, like Gecko) '\
#      'Chrome/55.0.2883.95 Safari/537.36 '
#
# req = urllib2.Request(URL)
# req.add_header("User-agent", USERAGENT)
#
# html = urllib2.urlopen(req)
# soup = BeautifulSoup(html, "html.parser")
#
# topicsindex = soup.find('div', attrs= {'class': 'topicsindex'})
# topics = topicsindex.find_all('li')
#
# for top in topics:
#      print top.find('a').contents[1]


read = pd.read_csv(PATH_INPUT_IMAGE_URL)
url = read['OriginalURL']
print url[0:10]

fName = url[0].split('/')[-1]
suffix = fName.split('.')[-1]
file_name = 0

for img in url:
     print img
     image_name = img.split('/')[-1]
     suffix = image_name.split('.')[-1]
     re = requests.get(img)
     with open(PATH_OUT_IMAGE + '%05d'%file_name + suffix, 'wb') as f:
          f.write(re.content)
     file_name += 1

     time.sleep(1)
