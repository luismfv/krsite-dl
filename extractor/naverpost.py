import time
import datetime
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import down.directory as dir

def from_naverpost(hd):
    print("Url: %s" % hd)
    opt = Options()
    opt.add_argument('--headless')
    w = wd.Chrome(options=opt)

    def naverpost_search(hd):
        w.get(hd)

        post_list = set()

        btn = w.find_element(By.CLASS_NAME, '_more')

        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False

                for i in w.find_elements(By.CLASS_NAME, 'link_end'):
                    post_list.add(i.get_attribute('href'))

        print("Found %s post(s)" % len(post_list))

        for i in post_list:
            naverpost_post(i)


    def naverpost_series(hd):
        w.get(hd)

        series_list = set()
        
        sender_name = w.find_element(By.CLASS_NAME, 'name').text
        print("Sender: %s" % sender_name)

        btn = w.find_element(By.CLASS_NAME, '_more')

        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False

                for i in w.find_elements(By.CLASS_NAME, 'link'):
                    series_list.add(i.get_attribute('href'))
        
        print("Found %s series" % len(series_list))
        print("------------------\n")

        for i in series_list:
            naverpost_list(i)


    def naverpost_list(hd):
        w.get(hd)
        
        post_list = set()

        btn = w.find_element(By.CLASS_NAME, '_more')

        stat = True
        while stat == True:
            try:
                btn.click()
                time.sleep(2)
            except:
                stat = False
                for i in w.find_elements(By.CLASS_NAME, 'spot_post_area'):
                    post_list.add(i.get_attribute('href'))

        print("Found %s post(s)" % len(post_list))
        
        for i in post_list:
            naverpost_post(i)


    def naverpost_post(hd):
        opt = Options()
        opt.add_argument('--headless')
        w = wd.Chrome(options=opt)
        w.get(hd)

        try:
            post_series = w.find_element(By.CLASS_NAME, 'se_series').text[3:]
            post_title = w.find_element(By.CLASS_NAME, 'se_textarea').text.replace('\n', ' ')
            post_date = w.find_element(By.CLASS_NAME, 'se_publishDate').text
            post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d. %H:%M')
            post_date_short = post_date.strftime('%y%m%d')
        except NoSuchElementException:
            post_series = w.find_element(By.CLASS_NAME, 'series').text
            post_title = w.find_element(By.CLASS_NAME, 'title').text.replace('\n', ' ')
            post_date = w.find_element(By.CLASS_NAME, 'post_date').text
            post_date = datetime.datetime.strptime(post_date, '%Y.%m.%d. %H:%M')
            post_date_short = post_date.strftime('%y%m%d')

        img_list = []

        print("\nSeries: %s" % post_series)
        print("Title: %s" % post_title)
        print("Date: %s" % post_date_short)

        for i in w.find_elements(By.CLASS_NAME, 'se_mediaImage'):
            if 'storep' not in i.get_attribute('src'):
                img_list.append(str(i.get_attribute('src').split('?')[0]))

        for i in w.find_elements(By.CLASS_NAME, 'img_attachedfile'):
            if 'storep' not in i.get_attribute('src'):
                img_list.append(str(i.get_attribute('src').split('?')[0]))

        w.quit()

        print("Found %s image(s)" % len(img_list))

        dir.dir_handler_naver(img_list, post_title, post_date_short, post_series, post_date)

    if 'my.naver' in hd:
        print("Naver Post Main Page")
        naverpost_search(hd)
    elif 'authorPost.naver' in hd:
        print("Naver Post Search Result")
        naverpost_search(hd)
    elif 'series.naver' in hd:
        print("Naver Post Series Page")
        naverpost_series(hd)
    elif 'detail.naver' in hd:
        print("Naver Post Series List")
        naverpost_list(hd)
    elif 'postView.naver' in hd:
        print("Naver Post Page")
        naverpost_post(hd)