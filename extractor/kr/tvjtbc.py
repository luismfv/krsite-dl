import requests
import re
import datetime
from bs4 import BeautifulSoup
import down.directory as dir

def from_tvjtbc(hd):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('h3', class_='veiw_tit').text.strip()
    post_date = soup.find('div', class_='view_info_txt').find_all('span')[2].text.replace('-', '')
    post_date_short = post_date[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y%m%d %p %I:%M:%S')
    content = soup.find('div', class_='view_cont_txt')

    img_list = []

    for item in content.findAll('img'):
        img_list.append(item.get('src'))

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    dir.dir_handler_alt(img_list, post_title, post_date_short, post_date)