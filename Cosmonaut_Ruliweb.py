import requests
from bs4 import BeautifulSoup
import pymysql
import time
from datetime import date, datetime
import os
import Cosmonaut_processor
import Secure_core


def method_ruliweb():
    print("*゜  (\ (\\")
    print("c(⌒(_*´ㅅ`)_")
    print("###method start")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    login_info = Secure_core.Info
    col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_Ymd = date.today().strftime('%Y%m%d')
    cnt = 0
    #------

    site = "ruliweb"
    module_name = "Cosmonaut_" + site
    mkdir_path = "E:/Database_img/DB_img_%s" % site
    mkdir_name = site + "_" + date_Ymd
    table_1 = "db_%s_1_" % site + date_Ymd
    rd = 1
    page_str = "?page="
    # ?p= or ?page= or &page= or
    list_start = 1
    page_end = 20
    cnt_last = 180
    #default : 2
    list_URL = ["https://bbs.ruliweb.com/allbbs?page="]
    list_category = ["category_1"]
    article_num = 30
    #---info---

    status_start = "start"
    Cosmonaut_processor.status_logging(col_date, module_name, status_start, 0)
    # ---logging---

    db = pymysql.connect(host=login_info["host"],
                         port=login_info["port"],
                         user=login_info["user"],
                         passwd=login_info["passwd"],
                         charset=login_info["charset"],
                         db='db_%s' % site)
    db.set_charset("utf8mb4")
    curs = db.cursor()
    try:
        sql_1 = """
            CREATE TABLE %s
            (id MEDIUMINT(6) UNSIGNED AUTO_INCREMENT NOT NULL, col_date DATETIME NOT NULL, category VARCHAR(20) NOT NULL,  
            article_url TEXT NOT NULL, article_title TEXT NOT NULL, good MEDIUMINT(8) NULL, bad MEDIUMINT(8) NULL, hits MEDIUMINT(8) NULL,
            article_text TEXT NULL, article_comment TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
            """ % table_1
        curs.execute(sql_1)
        db.commit()
        print("###CREATE TABLE###")
    except Exception as e:
        print("*Exception_0_1 : ", e)
        print("###table already exist")
    # ---table create---

    try:
        os.makedirs(os.path.join(mkdir_path, mkdir_name))
    except Exception as e:
        print("*Exception_0_2 : ", e)
        print("###directory already exist")
    #---directory create---


    for k0 in range(0, len(list_URL)):
        recent_article_url = []
        article_url_list = []
        try:
            sql_2_1 = """
                SELECT article_url FROM db_%s_duplication_check;
                """%site
            sql_2_2 = """
                SELECT article_url FROM db_%s_duplication_check WHERE (category = '%s');
                """ % (site, list_category[k0])
            if len(list_category) == 1:
                curs.execute(sql_2_1)
            else:
                curs.execute(sql_2_2)
            recent_article_url = curs.fetchall()
            print("###load data for duplication check from sql")
        except Exception as e:
            print("*Exception_0_2 : ", e)
            error = "Exception_0_2 : " + str(e)
            Cosmonaut_processor.err_report(col_date, module_name, error)
        # ---load data for duplicaion check---

        for k1 in range(1, page_end):
            #print("###", k1, "page start###")
            URL_1 = list_URL[k0] + str(k1)
            response_1 = requests.get(URL_1, headers=headers)
            html_1 = response_1.text
            soup_1 = BeautifulSoup(html_1, 'html.parser')
            list_articles = soup_1.find_all("tr", {"class":"table_body"})
            #---load article list---

            """
            for k1_1 in list_articles:
                k1_fi = str(k1_1).find('<a class="vrow notice notice-service"')
                # type 'bs4.element.Tag' >>> type 'str'
                if k1_fi >= 0:
                    list_index = list_articles.index(k1_1)
                    del list_articles[list_index]
                    list_articles.insert(list_index, "deletedelete")

            for k1_2 in range(0, list_articles.count("deletedelete")):
                list_articles.remove("deletedelete")
            # ---delete notice---
            """
            article_num = len(list_articles)


            for k2 in range(list_start, len(list_articles)):
                print(module_name, k0, "-", k1, "-", k2, "total :", cnt)
                #rd = random.randrange(1, 2, 1)

                try:
                    col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # ---col_date---

                    category = list_articles[k2].find("td", {"class": "board_name text_over padding_w_10"})
                    category = category.attrs["title"]
                    # ---category---

                    x_3 = list_articles[k2].find("a", {"class":"deco"})
                    x_3 = x_3.attrs['href']
                    URL_2 = "https://bbs.ruliweb.com" + x_3
                    #print("article_url: ", URL_2)
                    # ---article_url---

                    check = False
                    before = page_str + str(k1)
                    try:
                        for k2_1 in range(0, len(recent_article_url)):
                            URL_2_temp_1 = URL_2.replace(before, "")
                            recent_article_url_temp = recent_article_url[k2_1][0]
                            recent_article_url_temp = recent_article_url_temp.replace(page_str + "1", "").replace(
                                page_str + "2", "")
                            if URL_2_temp_1 == recent_article_url_temp:
                                check = True
                                print("###duplication detected in db!")
                                # print(URL_2, "v", recent_article_url_temp)
                                print("###break crawling")
                                break
                            else:
                                check = False
                    except Exception as e:
                        print("*Exception_2_1 : ", e)
                        error = "Exception_2_1 : " + str(e)
                        Cosmonaut_processor.err_report(col_date, module_name, error)
                    if check == True:
                        break
                    # ---duplication check for sql---

                    article_compare = False
                    URL_2_temp_2 = URL_2.replace(before, "")
                    for k2_2 in article_url_list:
                        if k2_2 == URL_2_temp_2:
                            article_compare = True
                            break
                    if article_compare == True:
                        print("###duplication detected!")
                        #print(k2_2, "v", URL_2_temp_2)
                        print("---------------------------------------------------")
                        continue
                    else:
                        pass
                    if len(article_url_list) == article_num * 3:
                        article_url_list.pop(0)
                    article_url_list.append(URL_2_temp_2)
                    # ---duplication check---

                    article_title = list_articles[k2].find("a", {"class":"deco"})
                    article_title = article_title.get_text()
                    #print("article_title: ", article_title)
                    # ---article_title---

                    response_2 = requests.get(URL_2, headers=headers)
                    html_2 = response_2.text
                    soup_2 = BeautifulSoup(html_2, 'html.parser')
                    # ---link to second page---

                    good = soup_2.find("span", {"class":"like_value"})
                    good = good.get_text()
                    good = good.replace(",", "")
                    #print("good: ", good)
                    # ---good---

                    try:
                        bad = soup_2.find("span", {"class": "dislike_value"})
                        bad = bad.get_text()
                        bad = bad.replace(",", "")
                    except:
                        bad = None
                    #print("bad: ", bad)
                    # ---bad---

                    try:
                        hits = soup_2.find("div", {"class": "user_info"})
                        hits = hits.find_all("p")[4]
                        hits = hits.get_text()
                        hits_loc = hits.find("조회")
                        hits_temp = ""
                        for k2_4 in range(0, 100):
                            if hits[hits_loc+3+k2_4].isdigit() == True:
                                hits_temp += hits[hits_loc+3+k2_4]
                            else:
                                break
                        hits = hits_temp
                        hits = hits.replace(",", "")
                    except:
                        hits = None
                    # ---hits---

                    article_text = soup_2.find("div", {"class":"view_content"})
                    article_text = article_text.get_text()
                    article_text = Cosmonaut_processor.text_analyze(article_text)
                    # ---article_text---

                    try:
                        article_comment = ""
                        ar_co = soup_2.find_all("tr", {"class": "comment_element normal parent"})
                        for k2_3 in ar_co:
                            k2_3 = k2_3.find("span", {"class":"text"})
                            k2_3 = k2_3.get_text()
                            article_comment += k2_3 + "\n"
                    except:
                        article_comment = None
                    # ---article_comment---

                    try:
                        image_src = soup_2.find("div", {"class": "view_content"})
                        # ------

                        image_src = image_src.find("img")
                        image_src = image_src.attrs['src']
                        image_name = "img_%s_"%site + datetime.now().strftime('%Y%m%d%H%M%S')
                        path = mkdir_path + "/" + mkdir_name
                        hashed_image_name = Cosmonaut_processor.image_sizedown(image_src, path, image_name)
                        image_dir = path + "/" + hashed_image_name
                    except Exception as e:
                        #print("*Exception_2_2 : ", e)
                        image_dir = None
                    #---image---


                    sql_3 = """
                            INSERT INTO %s""" % table_1 + """(col_date, category, article_url, article_title, good, bad, hits, article_text, article_comment, article_image)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                    curs.execute(sql_3, (col_date, category, URL_2, article_title, good, bad, hits, article_text, article_comment, image_dir))
                    db.commit()
                    # ---save into normal table---

                    sql_4 = """
                            INSERT INTO db_%s_duplication_check"""%site + """(col_date, category, article_url)
                            VALUES (%s, %s, %s)
                            """
                    if k1 == 1 or k1 == 2:
                        curs.execute(sql_4, (col_date, category, URL_2))
                        db.commit()
                    # ---save into table for check---

                    #print("col_date: ", col_date)
                    #print("category: ", category)



                    #print("bad: ", bad)
                    #print("hits: ", hits)
                    #print("article_text: ", article_text)
                    #print("article_comment: ", article_comment)
                    #print("article_img : ", image_dir)
                    cnt += 1
                    #print("---------------------------------------------------")
                    # ---logging---
                    time.sleep(rd)

                except Exception as e:
                    print("Exception_1 :", e)
                    print("---------------------------------------------------")
                    error = "Exception_1 : " + str(e)
                    Cosmonaut_processor.err_report(col_date, module_name, error)
                    time.sleep(rd)

                if cnt == cnt_last:
                    break

            if cnt == cnt_last:
                break

            if check == True:
                break
            time.sleep(rd)

        sql_5_1 = """
                DELETE FROM db_%s_duplication_check WHERE (col_date <
                ( SELECT MIN(col_date) FROM (SELECT col_date FROM db_%s_duplication_check ORDER BY col_date DESC LIMIT %s) AS min_col_data));
                """ % (site, site, str(article_num * 2 + 1))
        sql_5_2 = """
                DELETE FROM db_%s_duplication_check WHERE (col_date <
                ( SELECT MIN(col_date) FROM (SELECT col_date FROM db_%s_duplication_check where category = '%s' ORDER BY col_date DESC LIMIT %s) AS min_col_data)) and (category = '%s');
                """ % (site, site, list_category[k0], str(article_num * 2 + 1), list_category[k0])
        if len(list_category) == 1:
            curs.execute(sql_5_1)
        else:
            curs.execute(sql_5_2)
        db.commit()
        print("###db duplication check table reset")
        # ---database reset---
        time.sleep(rd)

        if cnt == cnt_last:
            break

    status_end = "end"
    Cosmonaut_processor.status_logging(col_date, module_name, status_end, cnt)
    # ---logging---

if __name__ == '__main__':
    method_ruliweb()


