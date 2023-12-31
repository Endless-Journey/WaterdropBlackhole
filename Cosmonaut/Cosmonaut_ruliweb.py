# -*- coding: utf-8 -*-
#Cosmonaut_example ver2.000.20230730
#Last update : 20230730

from Utils.Cosmonaut_processor import processor_class
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
from Info import Secure_core
import math
import re

site = "ruliweb"

def infinite_loop():
    cnt_loop = 1
    while True:
        print("### Cosmonaut :",  site, ", Loop : ", cnt_loop)
        method_cosmonaut()
        cnt_loop += 1

        time.sleep(300)

def method_cosmonaut():
    print("*゜  (\ (\\")
    print("c(⌒(_*´ㅅ`)_")
    print("### method start")
    module_info = Secure_core.Info_module
    headers = {"User-Agent": module_info["user-agent"] }
    col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #---default info---

    domain = "https://bbs.ruliweb.com/"
    rd = 1
    page_str = "&page="
    list_URL = [
        "https://bbs.ruliweb.com/community/board/300143?cate=497",
                ]
    list_category = [
        "Humor"
    ]
    cnt_last = 180
    article_num = 28
    page_start = 1
    page_end = math.ceil(cnt_last/(article_num*len(list_category)))
    if page_end == 1 or page_end == 2:
        page_end = 3
    #page_end = 7                    #TODO : Number of last page
    list_start = 1
    cnt = 1                          #Count
    #---info---

    p_class = processor_class(site, list_URL, list_category, rd, page_str)
    # ---Cosmonaut_processor declare---

    status_start = "start"
    p_class.status_logging(col_date, status_start, 0)
    # ---logging---

    p_class.create_table()
    # ---table create---

    p_class.create_dir()
    #---directory create---

    for k0 in range(0, len(list_URL)):
        article_url_list = []
        recent_article_url = p_class.select_recent_article(k0)
        # ---select data for duplicaion check---

        for k1 in range(page_start, page_end):
            print("### Cosmonaut :", site, ", ", "page : ", k1, ", total : ", cnt)
            URL_1 = list_URL[k0] + str(k1)
            response_1 = requests.get(URL_1, headers=headers)
            #response_1.encoding = 'UTF-8'
            #'UTF-8' or 'EUC-KR'
            html_1 = response_1.text
            soup_1 = BeautifulSoup(html_1, 'html.parser')


            list_articles = soup_1.find_all("tr", {"class" : "table_body blocktarget"})
            #---load article list---

            #list_articles = p_class.delete_notice(list_articles, '<span class="notice">')
            #---delete notice---
            article_num = len(list_articles)

            for k2 in range(list_start, len(list_articles)):
                #print("cosmonaut_%s"%site, k0+1, "-", k1, "-", k2, "total :", cnt)
                #rd = random.randrange(1, 2, 1)

                try:
                    col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #print("col_date: ", col_date)
                    # ---col_date---

                    category = list_articles[k2].find("td", {"class" : "divsn text_over"})
                    category = category.find("a")
                    category = category.get_text()
                    #category = list_category[k0]
                    #print("category: ", category)
                    # ---category---

                    article_URL = list_articles[k2].find("a", {"class" : "deco"})
                    article_URL = article_URL.attrs['href']
                    URL_2 = article_URL
                    #print("article_url: ", URL_2)
                    # ---article_url---

                    check = p_class.duplication_check_sql(k1, recent_article_url, URL_2)
                    if check == True:
                        break
                    # ---duplication check for sql---

                    article_compare = p_class.duplication_check(k1, URL_2, article_url_list, article_num)
                    if article_compare == True:
                        continue
                    # ---duplication check---

                    article_title = list_articles[k2].find("a", {"class" : "deco"})
                    article_title = article_title.get_text()
                    #article_title = article_title.strip()
                    #print("article_title: ", article_title)
                    # ---article_title---

                    hits = list_articles[k2].find("td", {"class" : "hit"})                                              #TODO : Check
                    hits = hits.get_text()
                    hits = hits.replace(",", "")
                    if hits == u"\xa0":
                        hits = None
                    hits = re.sub(r'[^0-9]', '', hits)
                    #print("hits: ", hits)
                    # ---hits---

                    response_2 = requests.get(URL_2, headers=headers)
                    #response_2.encoding = 'UTF-8'
                    html_2 = response_2.text
                    soup_2 = BeautifulSoup(html_2, 'html.parser')
                    # ---link to second page---

                    # ---------------------
                    # --- Enter article ---
                    # ---------------------

                    good = soup_2.find("span", {"class" : "like_value"})
                    good = good.get_text()
                    good = good.replace(",", "")
                    if good == u"\xa0":
                        good = None
                    #print("good: ", good)
                    # ---good---

                    bad = soup_2.find("span", {"class" : "dislike_value"})
                    bad = bad.get_text()
                    bad = bad.replace(",", "")
                    if bad == u"\xa0":
                        bad = None
                    #bad = None
                    #print("bad: ", bad)
                    # ---bad---

                    main_div = soup_2.find("div", {"class" : "view_content autolink"})
                    #main_div.find("div", {"id": "article-relation-link"}).decompose()
                    #---main_div---

                    article_text = main_div.get_text()
                    article_text = p_class.text_analyze(article_text)
                    #print("article_text: ", article_text)
                    # ---article_text---

                    try:
                        image_src = main_div.find("img")
                        image_src = image_src.attrs['src']
                        image_dir = p_class.image_process(image_src, col_date, domain)

                    except Exception as e:
                        #print("*Exception_image_process : ", e)
                        image_dir = None
                    #print("article_img : ", image_dir)
                    #---image---

                    try:
                        article_comment = ""
                        ar_co = soup_2.find("div", {"class" : "comment_view normal"})
                        ar_co = ar_co.find_all("tr")
                        for k2_3 in ar_co:
                            k2_3 = k2_3.find("span", {"class" : "text"})
                            k2_3 = k2_3.get_text()
                            k2_3 = p_class.text_analyze(k2_3)
                            article_comment += k2_3 + "\n"
                    except:
                        article_comment = None
                    #print("article_comment: ", article_comment)
                    # ---article_comment---

                    p_class.save_info(k1, col_date, category, URL_2, article_title, good, bad, hits, article_text, article_comment, image_dir)
                    # ---save into table for check---

                    cnt += 1
                    #print("---------------------------------------------------")

                except Exception as e:
                    error = "Exception_1 : " + str(e)
                    p_class.err_report(col_date, error)

                if cnt == cnt_last:
                    break

            if cnt == cnt_last:
                break

            if check == True:
                break
            time.sleep(rd)

        p_class.duplication_reset(k0, article_num)
        # ---database reset---

        if cnt == cnt_last:
            break

    status_end = "end"
    p_class.status_logging(col_date, status_end, cnt)
    print("*゜  (\ (\\")
    print("c(⌒(_*'ㅅ')_")
    print("### method end")
    # ---logging---

if __name__ == '__main__':
    method_cosmonaut()


