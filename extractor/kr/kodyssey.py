import requests
import re
import datetime
from bs4 import BeautifulSoup
import down.directory as dir

def from_kodyssey(hd):
    r = requests.get(hd)

    soup = BeautifulSoup(r.text, 'html.parser')

    img_list = []

    post_title = soup.find('div', class_='viewTitle').find('h1').text.strip()
    post_date = soup.find('div', class_='dd').text.strip()
    post_date_short = re.sub('[\u3131-\uD7A3]+|\/|-|\s', '', post_date)[2:8]
    content = soup.find('div', class_='sliderkit-panels')

    for i in content.find_all('img'):
        img_list.append('https://k-odyssey.com' + i['src'].replace('_thum', ''))


    post_date = re.sub('[\u3131-\uD7A3]+|\/|-|\s+', '', post_date)
    post_date = post_date[:8] + ' ' + post_date[8:]
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %H:%M:%S')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date_short)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)