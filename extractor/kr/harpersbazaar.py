import requests
import datetime
from bs4 import BeautifulSoup
import down.directory as dir

def from_harpersbazaar(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date_short = post_date.replace('-','')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S')

    content = soup.find('div', class_='atc_content')

    img_list = []
    for item in content.findAll('img'):
        if item.get('lazy') is not None or item.get('src') is not None:
            img_list.append(item.get('lazy') or item.get('src'))

    head_img = soup.find('div', class_='article_head')
    
    if head_img.get('style') is not None:
        img_list.append(head_img['style'].split('url(')[1].split(')')[0].replace('"',''))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler(img_list, post_title, post_date_short, post_date, loc, folder_name)