from selenium import webdriver
# 웹 드라이버
from bs4 import BeautifulSoup
import time as ti
import re
import pymysql
import urllib.request
import numpy as np
import base64
from datetime import datetime, date
import hashlib
import requests
from PIL import Image
# 이미지 수집을 위한
import os
from selenium.webdriver.common.by import By
from datetime import datetime

search_list_1 = ["100", "101", "102", "103", "104", "105", "106"]
search_list_2 = ["politics", "economy", "society", "culture", "world", "it", "entertainment", "sports"]
search_list_politics = ["264", "265", "266", "267", "268", "269"]
search_list_economy = ["260", "259", "259", "261", "262", "263", "771", "310"]
search_list_society = ["249", "250", "251", "252", "254", "59b", "256", "276", "257", "255"]
search_list_culture = ["237", "239", "240", "241", "242", "243", "244", "245", "238", "376", "248"]
search_list_world = ["231", "232", "233", "234", "322"]
search_list_it = ["226", "228", "229", "283", "230", "731", "227", "732", "228"]
#비우면 바로 k1 : 7로 넘어감
search_list_entertainment = ["221", "224", "225", "7a5", "309"]
search_list_sports = ["kbaseball", "wbaseball", "kfootball", "wfootball", "basketball", "volleyball", "golf", "general", "esports"]



# 100 정치 경제 101 사회 102 문화 103 세계 104 it 105 오피니언 110 연예 106

date_one_1 = datetime.now()
date_one_2 = "20" + date_one_1.strftime('%y%m%d')
date_one = "20220206"

class p_data_collect:
    print("***데이터 수집을 시작합니다.***")





    def main_method(self):
        driver = webdriver.Chrome('D:/Chromedriver/chromedriver.exe')
        driver.implicitly_wait(30)
        URL_general_article = "https://news.naver.com/main/list.naver?mode=LS2D&mid=sec&sid2="
        URL_entertainment_article = "https://entertain.naver.com/now?sid="
        URL_sports_article = "https://sports.news.naver.com/"

        for k1 in range(0, 8):
        #k1 : 카테고리
            self.generate_table(k1)
            mkdir_path = "E:/Database_img_naver/%s/"%search_list_2[k1] + "%s_%s" % (search_list_2[k1], date_one)
            try:
                os.makedirs(mkdir_path)
            except Exception as e:
                print("*Exception : ", e)
                print("###directory already exist")
            # ---directory create---

            table_name = "log_%s" % search_list_2[k1] + "_" + date_one
            f = open("E:/Log/nnews_collector/%s.txt" % table_name, 'a', encoding= 'UTF-8')
            #한글이 포함될 경우 encoding을 해주어야 함.
            if k1 < 6:
                now_time = datetime.now()
                print(search_list_2[k1], "주제의 수집을 시작합니다. ", "k1 : [%s]" % now_time)
                v1 = globals()['search_list_{}'.format(search_list_2[k1])]



                for k2 in v1:
                #k2 : 서브 카테고리
                    now_time = datetime.now()
                    print("k2 : [%s]"%now_time)

                    article_url_list = []
                    for k3 in range(1, 10):
                    #k3 : 페이지
                        now_time = datetime.now()
                        print(k3, "페이지 수집 시작합니다.", "k3 : [%s]" % now_time)

                        URL_complete = URL_general_article + k2 + "&sid1=" + search_list_1[k1] + "&date=" + date_one + "&page=" + "%s"%k3
                        #print("article_list_URL : ", URL_complete)


                        driver.get(URL_complete)
                        ti.sleep(0.5)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')

                        connect_page_list = soup.find("div", {"class":"list_body newsflash_body"})
                        connect_page_list_1 = connect_page_list.find("ul", {"class":"type06_headline"})
                        connect_page_list_1 = connect_page_list_1.find_all("li")
                        try:
                            connect_page_list_2 = connect_page_list.find("ul", {"class":"type06"})
                            connect_page_list_2 = connect_page_list_2.find_all("li")
                        except:
                            connect_page_list_2 = []
                        connect_page_list = connect_page_list_1 + connect_page_list_2
                        page_num = len(connect_page_list)

                        article_compare = False
                        for k4 in range(0, page_num):
                            connect_def_1 = connect_page_list[k4].find("a")
                            connect_def_2 = connect_def_1.attrs['href']
                            #print("article_URL : ", connect_def_2)

                            URL_2_temp_2 = connect_def_2
                            for k2_2 in article_url_list:
                                if k2_2 == URL_2_temp_2:
                                    article_compare = True
                                    break
                            if article_compare == True:
                                print("###duplication detected!")
                                # print(k2_2, "v", URL_2_temp_2)
                                break
                            else:
                                if len(article_url_list) == 20:
                                    article_url_list.pop(0)
                                article_url_list.append(URL_2_temp_2)
                            #---duplication check---

                            driver.get(connect_def_2)
                            ti.sleep(0.2)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            try:
                                self.analyze_article(soup, k1, k2, connect_def_2)
                            except Exception as e:
                                print(e)
                                pass

                        if article_compare == True:
                            break


            #-------------------------일반 기사 리스트 수집 ----------------------------------------


            elif k1 == 6:
                print("entertainment 수집 시작")
                for k2 in search_list_entertainment:
                    article_url_list = []
                    for k3 in range(1,10):
                        now_time = datetime.now()
                        print(k3, "페이지 수집 시작합니다.", "k3 : [%s]" % now_time)
                        date_for_enter = date_one[0:4] + "-" + date_one[4:6] + "-" + date_one[6:8]
                        URL_complete = URL_entertainment_article + k2 + "#sid=" + k2 + "&date=" + date_for_enter + "&page=" + "%s" % k3
                        #print("article_list_URL : ", URL_complete)
                        driver.get(URL_complete)
                        ti.sleep(0.5)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')

                        connect_page_list = soup.find("ul", {"class": "news_lst news_lst2"})
                        connect_page_list = connect_page_list.find_all("li")
                        page_num = len(connect_page_list)

                        for k4 in range(0, page_num):
                            connect_def_1 = connect_page_list[k4].find("a")
                            breaker_1 = False
                            if connect_def_1 == None:
                                breaker_1 = True
                                break


                            connect_def_2 = connect_def_1.attrs['href']
                            connect_def_3 = "https://entertain.naver.com/" + connect_def_2
                            #print("article_URL : ", connect_def_3)


                            driver.get(connect_def_3)
                            ti.sleep(0.2)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            try:
                                self.analyze_article(soup, k1, k2, connect_def_3)
                            except:
                                pass

                        if breaker_1 == True:
                            break

            #--------------------연예 기사 리스트 수집 ------------------------------------------


            else:
                print("sports 수집 시작")
                for k2 in search_list_sports:

                    if k2 == "esports":
                        now_time = datetime.now()
                        print("esports 수집 시작합니다.", "k3 : [%s]" % now_time)
                        URL_complete = "https://game.naver.com/esports/news/all?date=" + "%s-%s-%s"%(date_one[0:4], date_one[4:6], date_one[6:8])
                        driver.get(URL_complete)
                        ti.sleep(0.5)
                        driver.find_element(By.CLASS_NAME, "news_list_more_btn__3QwSl").click()
                        ti.sleep(0.2)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')

                        connect_page_list = soup.find("div", {"class": "news_list_container__1L7tH"})
                        connect_page_list = connect_page_list.find_all("li", {"class":"news_card_item__2lh4o"})
                        page_num = len(connect_page_list)
                        article_compare = False
                        for k4 in range(0, page_num):
                            connect_def_1 = connect_page_list[k4].find("a")
                            connect_def_2 = connect_def_1.attrs['href']
                            connect_def_3 = connect_def_2
                            #print("article_URL : ", connect_def_2)

                            driver.get(connect_def_3)
                            ti.sleep(0.2)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            try:
                                self.analyze_article(soup, k1, k2, connect_def_3)
                            except:
                                pass

                        if article_compare == True:
                            break

                        break

                        continue

                    article_url_list = []
                    for k3 in range(1, 10):
                        URL_complete = URL_sports_article + k2 + "/news/index?isphoto=N&date=" + "&date=" + date_one + "&page=" + "%s" % k3
                        now_time = datetime.now()
                        print(k3, "페이지 수집 시작합니다.", "k3 : [%s]" % now_time)
                        driver.get(URL_complete)
                        ti.sleep(0.5)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')

                        connect_page_list = soup.find("div", {"class": "news_list"})
                        connect_page_list = connect_page_list.find_all("li")
                        page_num = len(connect_page_list)

                        article_compare = False
                        for k4 in range(0, page_num):
                            connect_def_1 = connect_page_list[k4].find("a")
                            connect_def_2 = connect_def_1.attrs['href']
                            connect_def_3 = "https://sports.news.naver.com" + connect_def_2
                            # print("article_URL : ", connect_def_2)

                            URL_2_temp_2 = connect_def_3
                            for k2_2 in article_url_list:
                                if k2_2 == URL_2_temp_2:
                                    article_compare = True
                                    break
                            if article_compare == True:
                                print("###duplication detected!")
                                # print(k2_2, "v", URL_2_temp_2)
                                break
                            else:
                                if len(article_url_list) == 20:
                                    article_url_list.pop(0)
                                article_url_list.append(URL_2_temp_2)
                            # ---duplication check---

                            driver.get(connect_def_3)
                            ti.sleep(0.5)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            try:
                                self.analyze_article(soup, k1, k2, connect_def_3)
                            except:
                                pass

                        if article_compare == True:
                            break


    def generate_table(self, k1):
        self.k1 = k1

        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='mysql0788',
                             db='nnews_%s'%search_list_2[k1],
                             charset='utf8')
        table_name = "%s_"%search_list_2[k1] + date_one

        if k1 < 6:
            try:
                curs = db.cursor()
                sql = """
                        CREATE TABLE %s (id SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT, article_id CHAR(13) NULL, sub_category CHAR(3) NULL, write_date DATETIME NULL, 
                        good SMALLINT(5) UNSIGNED NULL, warm SMALLINT(5) UNSIGNED NULL, sad SMALLINT(5) UNSIGNED NULL, angry SMALLINT(5) UNSIGNED NULL, want SMALLINT(5) UNSIGNED NULL, total SMALLINT(5) UNSIGNED NULL,
                        man TINYINT(3) UNSIGNED NULL, woman TINYINT(3) UNSIGNED NULL,
                        age_10 TINYINT(3) UNSIGNED NULL, age_20 TINYINT(3) UNSIGNED NULL, age_30 TINYINT(3) UNSIGNED NULL, age_40 TINYINT(3) NULL, age_50 TINYINT(3) NULL, age_60 TINYINT(3) NULL,
                        title VARCHAR(100) NULL, main_text TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
                        """ % table_name
                # 테이블을 만들경우 USE를 사용하면 안됨. 이 형식을 사용하여야 함.
                curs.execute(sql)
                db.commit()
                print(table_name, "테이블을 생성하였습니다.")
            except Exception as e:
                print(e)
                print("테이블이 이미 존재합니다.")

        #일반 기사 테이블
        elif k1 == 6:
            try:
                curs = db.cursor()
                sql = """
                        CREATE TABLE %s (id SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT, article_id CHAR(13) NULL, sub_category CHAR(3) NULL, write_date DATETIME NULL, 
                        good SMALLINT(5) UNSIGNED NULL, cheer SMALLINT(5) UNSIGNED NULL, congrats SMALLINT(5) UNSIGNED NULL, expect SMALLINT(5) UNSIGNED NULL, surprise SMALLINT(5) UNSIGNED NULL, sad SMALLINT(5) UNSIGNED NULL, total SMALLINT(5) UNSIGNED NULL,
                        title VARCHAR(100) NULL, main_text TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
                        """ % table_name
                # 테이블을 만들경우 USE를 사용하면 안됨. 이 형식을 사용하여야 함.
                curs.execute(sql)
                db.commit()
                print(table_name, "테이블을 생성하였습니다.")
            except:
                print("테이블이 이미 존재합니다.")
        #연예 기사 테이블

        else:
            try:
                curs = db.cursor()
                sql = """
                        CREATE TABLE %s (id SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT, article_id CHAR(13) NULL, sub_category CHAR(10) NULL, write_date DATETIME NULL, 
                        good SMALLINT(5) UNSIGNED NULL, sad SMALLINT(5) UNSIGNED NULL, angry SMALLINT(5) UNSIGNED NULL, fan SMALLINT(5) UNSIGNED NULL, want SMALLINT(5) UNSIGNED NULL, total SMALLINT(5) UNSIGNED NULL,
                        title VARCHAR(100) NULL, main_text TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
                        """ % table_name
                # 테이블을 만들경우 USE를 사용하면 안됨. 이 형식을 사용하여야 함.
                curs.execute(sql)
                db.commit()
                print(table_name, "테이블을 생성하였습니다.")
            except:
                print("테이블이 이미 존재합니다.")
        #스포츠 기사 테이블


    #테이블을 생성하는 메소드
    #---------------------------------------- 기사 번호 ----------------------------------------


    def analyze_article(self, soup, k1, k2, URL):
        self.soup = soup
        self.k1 = k1
        self.k2 = k2
        self.URL = URL


        table_name = "%s_" % search_list_2[k1] + date_one
        f = open("E:/Log/nnews_collector/log_%s.txt" % table_name, 'a', encoding= 'UTF-8')

        article_id = URL
        article_id_1 = article_id.find("oid")
        article_id_2 = article_id.find("aid")
        article_id_all = article_id[article_id_1 + 4:article_id_1 + 7] + article_id[article_id_2 + 4:article_id_2 + 14]
        #print("article_id : ", article_id_all)
        #oid 뒤는 언론사 코드 #aid 뒤는 기사번호

        try:
            sub_category_1 = k2
            #print("sub_category : ", sub_category_1)
        except:
            sub_category_1 = None
            #print("sub_category 에러 발생")

        write_date_v3 = None
        try:
            write_date_v1 = soup.find("div", {"class": "article_info"})
            write_date_v2 = write_date_v1.find("span", {"class": "t11"})
            write_date_v3 = write_date_v2.find(string=True)
        except:
            write_date_v3 = None


        if write_date_v3 == None:
            try:
                write_date_v1 = soup.find("div", {"class": "article_info"})
                write_date_v2 = write_date_v1.find("span", {"class": "author"})
                write_date_v2 = write_date_v2.find("em")
                write_date_v3 = write_date_v2.find(string=True)
            except:
                write_date_v3=None

        if write_date_v3 == None:
            try:
                write_date_v1 = soup.find("div", {"class": "info"})
                write_date_v2 = write_date_v1.find("span")
                write_date_v3 = write_date_v2.find(string=True)
            except:
                write_date_v3 =None






        numbers = re.sub(r'[^0-9]', '', write_date_v3)
        fi_forenoon = write_date_v3.find("오전")
        fi_afternoon = write_date_v3.find("오후")
        if len(numbers) == 11 and fi_forenoon >= 0:
            Year = int(numbers[0:4])
            month = int(numbers[4:6])
            days = int(numbers[6:8])
            hour = int(numbers[8:9])
            minute = int(numbers[9:11])
            second = 0
            write_date = datetime(Year, month, days, hour, minute, second)
        elif len(numbers) == 12 and fi_forenoon >= 0 and int(numbers[8:10]) == 12:
            Year = int(numbers[0:4])
            month = int(numbers[4:6])
            days = int(numbers[6:8])
            hour = int(numbers[8:10]) - 12
            minute = int(numbers[10:12])
            second = 0
            write_date = datetime(Year, month, days, hour, minute, second)
        elif len(numbers) == 12 and fi_forenoon >= 0:
            Year = int(numbers[0:4])
            month = int(numbers[4:6])
            days = int(numbers[6:8])
            hour = int(numbers[8:10])
            minute = int(numbers[10:12])
            second = 0
            write_date = datetime(Year, month, days, hour, minute, second)
        elif len(numbers) == 11 and fi_afternoon >= 0:
            Year = int(numbers[0:4])
            month = int(numbers[4:6])
            days = int(numbers[6:8])
            hour = int(numbers[8:9]) + 12
            minute = int(numbers[9:11])
            second = 0
            write_date = datetime(Year, month, days, hour, minute, second)
        elif len(numbers) == 12 and fi_afternoon >= 0 and int(numbers[8:10]) == 12:
            Year = int(numbers[0:4])
            month = int(numbers[4:6])
            days = int(numbers[6:8])
            hour = int(numbers[8:10])
            minute = int(numbers[10:12])
            second = 0
            write_date = datetime(Year, month, days, hour, minute, second)
        elif len(numbers) == 12 and fi_afternoon >= 0:
            Year = int(numbers[0:4])
            month = int(numbers[4:6])
            days = int(numbers[6:8])
            hour = int(numbers[8:10]) + 12
            minute = int(numbers[10:12])
            second = 0
            write_date = datetime(Year, month, days, hour, minute, second)
        write_date3 = write_date
        #---------------------------------------- 기사 작성 날짜 ----------------------------------------

        try:
            good_1 = soup.find("a", {"data-type": "like"})
            good_2 = good_1.find("span", {"class": "u_likeit_list_count _count"})
            good_3 = good_2.find(string=True)
            good_4 = re.sub(",", "", good_3)
            #String으로 하면 None 뜬다 string으로 해야한다.
        except:
            #print("평가 예외 발생(good)")
            good_4 = None

        try:
            warm_1 = soup.find("a", {"data-type": "warm"})
            warm_2 = warm_1.find("span", {"class": "u_likeit_list_count _count"})
            warm_3 = warm_2.find(string=True)
            warm_4 = re.sub(",", "", warm_3)
        except:
            #print("평가 예외 발생(warm)")
            warm_4 = None

        try:
            sad_1 = soup.find("a", {"data-type": "sad"})
            sad_2 = sad_1.find("span", {"class": "u_likeit_list_count _count"})
            sad_3 = sad_2.find(string=True)
            sad_4 = re.sub(",", "", sad_3)
        except:
            #print("평가 예외 발생(except)")
            sad_4 = None


        try:
            angry_1 = soup.find("a", {"data-type": "angry"})
            angry_2 = angry_1.find("span", {"class": "u_likeit_list_count _count"})
            angry_3 = angry_2.find(string=True)
            angry_4 = re.sub(",", "", angry_3)
        except:
            #print("평가 예외 발생(angry)")
            angry_4 = None

        try:
            want_1 = soup.find("a", {"data-type": "want"})
            want_2 = want_1.find("span", {"class": "u_likeit_list_count _count"})
            want_3 = want_2.find(string=True)
            want_4 = re.sub(",", "", want_3)
        except:
            #print("평가 예외 발생(want)")
            want_4 = None
        #일반 기사들

        try:
            cheer_1 = soup.find("a", {"data-type": "cheer"})
            cheer_2 = cheer_1.find("span", {"class": "u_likeit_list_count _count"})
            cheer_3 = cheer_2.find(string=True)
            cheer_4 = re.sub(",", "", cheer_3)
        except:
            #print("평가 예외 발생(cheer)")
            cheer_4 = None

        try:
            congrats_1 = soup.find("a", {"data-type": "congrats"})
            congrats_2 = congrats_1.find("span", {"class": "u_likeit_list_count _count"})
            congrats_3 = congrats_2.find(string=True)
            congrats_4 = re.sub(",", "", congrats_3)
        except:
            #print("평가 예외 발생(congrats)")
            congrats_4 = None

        try:
            expect_1 = soup.find("a", {"data-type": "expect"})
            expect_2 = expect_1.find("span", {"class": "u_likeit_list_count _count"})
            expect_3 = expect_2.find(string=True)
            expect_4 = re.sub(",", "", expect_3)
        except:
            #print("평가 예외 발생(expect)")
            expect_4 = None

        try:
            surprise_1 = soup.find("a", {"data-type": "surprise"})
            surprise_2 = surprise_1.find("span", {"class": "u_likeit_list_count _count"})
            surprise_3 = surprise_2.find(string=True)
            surprise_4 = re.sub(",", "", surprise_3)
        except:
            #print("평가 예외 발생(suprise)")
            surprise_4 = None

        #연예기사

        try:
            fan_1 = soup.find("a", {"data-type": "fan"})
            fan_2 = fan_1.find("span", {"class": "u_likeit_list_count _count"})
            fan_3 = fan_2.find(string=True)
            fan_4 = re.sub(",", "", fan_3)
        except:
            #print("평가 예외 발생(fan)")
            fan_4 = None
        #스포츠 기사


        #print("평가 : ", good_4, warm_4, sad_4, angry_4, want_4, cheer_4, congrats_4, expect_4, surprise_4, fan_4, file=f)
        #print("평가 : ", good_4, warm_4, sad_4, angry_4, want_4, cheer_4, congrats_4, expect_4, surprise_4, fan_4)
        #---------------------------------------- 기사 평가 항목 ----------------------------------------

        try:
            evaluation_total_1 = soup.find("span", {"class": "u_likeit_text _count num"})
            evaluation_total_2 = evaluation_total_1.find(string=True)
            evaluation_total_3 = re.sub(",", "", evaluation_total_2)
            #print("평가 합계 : ", evaluation_total_3)
        except:
            evaluation_total_3 = None
        #--------------------------------------- 기사 평가 항목 합계 ---------------------------------------

        try:
            man_1 = soup.find("div", {"class": "u_cbox_chart_progress u_cbox_chart_male"})
            man_2 = man_1.find(string=True)
            woman = 100-int(man_2)
            #print("남녀비율 : ", man_2, ":", woman)

            age_1 = soup.find("div", {"class": "u_cbox_chart_age"})
            age_2 = age_1.findAll("span", {"class": "u_cbox_chart_per"})

            age_10 = age_2[0].find(string=True)
            age_20 = age_2[1].find(string=True)
            age_30 = age_2[2].find(string=True)
            age_40 = age_2[3].find(string=True)
            age_50 = age_2[4].find(string=True)
            age_60 = age_2[5].find(string=True)
            #print("나이비율 : ", age_10, age_20, age_30, age_40, age_50, age_60)
        except:
            age_10 = None
            age_20 = None
            age_30 = None
            age_40 = None
            age_50 = None
            age_60 = None
            man_2 = None
            woman = None
            #""를 이용하여 공백을 만들시 sql에서 오류 발생
            #print("남녀비율, 나이비율 없음")
        #---------------------------------------- 남녀, 나이 비율 ----------------------------------------

        if k1 < 6:
            title_1 = soup.find("h3", {"id": "articleTitle"})
            title_2 = title_1.find(string=True)
            title_2 = title_2.strip()
        elif k1 == 6:
            title_1 = soup.find("h2", {"class": "end_tit"})
            title_2 = title_1.find(string=True)
            title_2 = title_2.strip()
        else:
            title_1 = soup.find("h4", {"class": "title"})
            title_2 = title_1.find(string=True)
            title_2 = title_2.strip()

        #print("제목 : ", title_2)
        #일반뉴스 h3 class tts_head
        #연예뉴스 h2 class end_tit
        #스포츠뉴스 h4 class title
        #------------------------------------------- 기사 제목 -------------------------------------------

        main_text_1 = soup.find("div", {"class": "_article_body_contents"})
        if main_text_1 == None:
            main_text_1 = soup.find("div", {"class": "article_body font1 size3"})
            if main_text_1 == None:
                main_text_1 = soup.find("div", {"class": "news_end font1 size3"})

        main_text_2 = str(main_text_1)
        main_text_3 = re.sub('<script.+?/script>', '', main_text_2, 0, re.I | re.S)
        main_text_4 = re.sub('<em.+?/em>', '', main_text_3)
        main_text_5 = re.sub('<.+?>', '', main_text_4, 0, re.I | re.S)
        main_text_6 = re.sub('\\n', '', main_text_5)
        main_text_7 = main_text_6.strip()
        #print("내용 : ", main_text_7)

        #------------------------------------------- 기사 제목 -------------------------------------------

        try:
            image_1 = soup.find("div" , {"class" : "_article_body_contents"})
            if image_1 == None:
                image_1 = soup.find("div" , {"class" : "article_body font1 size3"})
                if image_1 == None:
                    image_1 = soup.find("div", {"class": "news_end font1 size3"})
            image_2 = image_1.find("span", {"class": "end_photo_org"})
            image_3 = image_2.find("img")
            image_4 = image_3.attrs['src']

            col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            image_name = search_list_2[k1] + col_date
            image_name = hashlib.md5(image_name.encode()).hexdigest()
            image_path = "E:/Database_img_naver/%s/"%search_list_2[k1] + "%s_%s"%(search_list_2[k1], date_one)

            image_loc = image_path + "/" + str(image_name) + ".jpg"
            image_PIL = Image.open(requests.get(image_4, stream=True).raw)
            image_PIL.save(image_loc)

        except:
            image_loc = None
            #print("이미지가 존재하지 않습니다.")

        db = pymysql.connect(host="localhost",
                             port=3306,
                             user='root',
                             passwd='mysql0788',
                             db='nnews_%s' % search_list_2[k1],
                             charset='utf8')

        table_name = "%s_" % search_list_2[k1] + date_one

        try:

            if k1 < 6:
                curs = db.cursor()
                sql1 = """INSERT INTO %s""" % table_name + """(article_id, sub_category, write_date, good, warm, sad, angry, want, total, man, woman, 
                age_10, age_20, age_30, age_40, age_50, age_60, `title`, main_text, article_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                curs.execute(sql1, (article_id_all, sub_category_1, write_date3, good_4, warm_4, sad_4, angry_4, want_4, evaluation_total_3, man_2, woman, age_10, age_20, age_30, age_40, age_50, age_60, title_2, main_text_7, image_loc))
                db.commit()
                #print("데이터베이스에 저장완료 #1")
                ti.sleep(0.1)

            elif k1 == 6:
                curs = db.cursor()
                sql1 = """INSERT INTO %s""" % table_name + """(article_id, sub_category, write_date, good, cheer, congrats, expect, surprise, sad, total, `title`, main_text, article_image) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                curs.execute(sql1, (
                article_id_all, sub_category_1, write_date3, good_4, cheer_4, congrats_4, expect_4, surprise_4, sad_4, evaluation_total_3,title_2, main_text_7, image_loc))
                db.commit()
                #print("데이터베이스에 저장완료 #2")
                ti.sleep(0.1)

            else:
                curs = db.cursor()
                sql1 = """INSERT INTO %s""" % table_name + """(article_id, sub_category, write_date, good, sad, angry, fan, want, total, `title`, main_text, article_image) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                curs.execute(sql1, (
                    article_id_all, sub_category_1, write_date3, good_4, sad_4, angry_4, fan_4, want_4,
                    evaluation_total_3, title_2, main_text_7, image_loc))
                db.commit()
                #print("데이터베이스에 저장완료 #3")
                ti.sleep(0.1)

            #print("-------------------------------------------------------------------------------------------")

        except Exception as e:
            print("Exception : ", e)

        print(sub_category_1, "/",  article_id_all, "/", write_date3)

start = p_data_collect()
start.main_method()
#시동 걸기

