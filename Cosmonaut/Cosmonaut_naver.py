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

search_list_major_1 = ["politics", "economy", "society", "culture", "world", "it", "entertainment", "sports"]
search_list_major_2 = ["100", "101", "102", "103", "104", "105"]
# 100 : 정치, 101 : 경제, 102 : 사회, 103 : 문화, 104 : 세계, 105 : IT
search_list_politics = ["264", "265", "266", "267", "268", "269"]
# 264 : 대통령실, 265 : 국회/정당, 266 : 행정, 267 : 국방/외교, 268 : 북한, 269 : 정치일반
search_list_economy = ["258", "259", "260", "261", "262", "263", "310", "771"]
# 258 : 증권, 259 : 금융, 260 : 부동산, 261 : 산업/재계, 262 : 글로벌경제, 263 : 경제일반, 310 : 생활경제, 771 : 중기/벤처
search_list_society = ["249", "250", "251", "252", "254", "255", "256", "257", "276", "59b"]
# 249 : 사건사고, 250 : 교육, 251 : 노동, 252 : 환경, 254 : 언론, 255 : 식품/의료, 256 : 지역, 257 : 사회 일반, 276 : 인물, 59b : 인권/복지
search_list_culture = ["237", "238", "239", "240", "241", "242", "243", "244", "245", "248", "376"]
# 237 : 여행/레저, 238 : 음식/맛집, 239 : 자동차/시승기, 240 : 도로/교통, 241 : 건강정보, 242 : 공연/전시, 243 : 책, 244 : 종교, 245 : 생활문화 일반, 248 : 날씨, 376 : 패션/뷰티
search_list_world = ["231", "232", "233", "234", "322"]
# 231 : 아시아/호주, 232 : 미국/중남미, 233 : 유럽, 234 : 중동/아프리카, 322 : 세계일반
search_list_it = ["226", "228", "229", "283", "230", "731", "227", "732", "228"]
# 226 : 인터넷/SNS, 227 : 통신/뉴미니어, 228 : 과학일반, 229 : 게임/리뷰, 230 : IT일반, 283 : 컴퓨터, 731 : 모바일, 732 : 보안/해킹
search_list_entertainment = ["221", "224", "225", "7a5", "309"]
# 221 : 연예가화제, 224 : 방송/TV, 225 : 드라마, 309 : 해외뮤직, 7a5 : 뮤직
search_list_sports = ["kbaseball", "wbaseball", "kfootball", "wfootball", "basketball", "volleyball", "golf", "general", "esports"]

class p_data_collect:
    def __init__(self, date_one):
        self.date_one = date_one

    print("### Cosmonaut_naver start###")

    def main_method(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(100)
        URL_general_article = "https://news.naver.com/main/list.naver?mode=LS2D&mid=sec&sid2="
        URL_entertainment_article = "https://entertain.naver.com/now?sid="
        URL_sports_article = "https://sports.news.naver.com/"

        for k1 in range(0, 8):
        #k1 : 카테고리
            # Create table
            self.create_table(k1)
            # ---------------------------------------------------------

            # Create image directory
            mkdir_path = "E:/Data/Data_img/Data_img_naver/%s/"%search_list_major_1[k1] + "%s_%s" % (search_list_major_1[k1], self.date_one)
            try:
                os.makedirs(mkdir_path)
            except Exception as e:
                print("*Exception : ", e)
                #print("### Img directory already exist ###")
            # ---------------------------------------------------------

            if k1 < 6:
                now_time = datetime.now()
                print("*゜  (\ (\\")
                print("c(⌒(_*´ㅅ`)_")
                print("Category :", search_list_major_1[k1], "start, time : [%s]" % now_time)
                v1 = globals()['search_list_{}'.format(search_list_major_1[k1])]

                for k2 in v1:
                #k2 : 서브 카테고리
                    now_time = datetime.now()
                    print("Subcategory :", k2, "start, time : [%s]" % now_time)

                    article_url_list = []
                    for k3 in range(1, 10):
                    #k3 : 페이지
                        now_time = datetime.now()
                        print("Page :", k3, "start, time : [%s]" % now_time)

                        URL_complete = URL_general_article + k2 + "&sid1=" + search_list_major_2[k1] + "&date=" + self.date_one + "&page=" + "%s"%k3
                        #print("article_list_URL : ", URL_complete)

                        driver.get(URL_complete)
                        ti.sleep(1)
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
                now_time = datetime.now()
                print("Subcategory :", k2, "start, time : [%s]" % now_time)

                for k2 in search_list_entertainment:
                    article_url_list = []
                    for k3 in range(1,10):
                        now_time = datetime.now()
                        print("Page :", k3, "start, time : [%s]" % now_time)

                        date_for_enter = self.date_one[0:4] + "-" + self.date_one[4:6] + "-" + self.date_one[6:8]
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

            elif k1 == 7:
                now_time = datetime.now()
                print("Subcategory :", k2, "start, time : [%s]" % now_time)

                for k2 in search_list_sports:
                    if k2 == "esports":
                        now_time = datetime.now()
                        print("esports start, time : [%s]" % now_time)

                        URL_complete = "https://game.naver.com/esports/news/all?date=" + "%s-%s-%s"%(self.date_one[0:4], self.date_one[4:6], self.date_one[6:8])
                        driver.get(URL_complete)
                        ti.sleep(0.5)
                        try:
                            driver.find_element(By.CLASS_NAME, "news_list_more_btn__3QwSl").click()
                        except:
                            print("Last Page")
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
                        URL_complete = URL_sports_article + k2 + "/news/index?isphoto=N&date=" + "&date=" + self.date_one + "&page=" + "%s" % k3

                        now_time = datetime.now()
                        print("Page :", k3, "start, time : [%s]" % now_time)

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


    def create_table(self, k1):
        self.k1 = k1

        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='mysql0788',
                             db='nnews_%s'%search_list_major_1[k1],
                             charset='utf8')
        table_name = "%s_"%search_list_major_1[k1] + self.date_one

        if k1 < 6:
            try:
                curs = db.cursor()
                sql = """
                        CREATE TABLE %s (id SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT, article_url TEXT NULL, sub_category CHAR(3) NULL, write_date DATETIME NULL, 
                        good SMALLINT(5) UNSIGNED NULL, warm SMALLINT(5) UNSIGNED NULL, sad SMALLINT(5) UNSIGNED NULL, angry SMALLINT(5) UNSIGNED NULL, want SMALLINT(5) UNSIGNED NULL,
                        man TINYINT(3) UNSIGNED NULL, woman TINYINT(3) UNSIGNED NULL,
                        age_10 TINYINT(3) UNSIGNED NULL, age_20 TINYINT(3) UNSIGNED NULL, age_30 TINYINT(3) UNSIGNED NULL, age_40 TINYINT(3) NULL, age_50 TINYINT(3) NULL, age_60 TINYINT(3) NULL,
                        article_title VARCHAR(100) NULL, main_text TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
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
                        CREATE TABLE %s (id SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT, article_url TEXT NULL, sub_category CHAR(3) NULL, write_date DATETIME NULL, 
                        good SMALLINT(5) UNSIGNED NULL, cheer SMALLINT(5) UNSIGNED NULL, congrats SMALLINT(5) UNSIGNED NULL, expect SMALLINT(5) UNSIGNED NULL, surprise SMALLINT(5) UNSIGNED NULL, sad SMALLINT(5) UNSIGNED NULL,
                        article_title VARCHAR(100) NULL, main_text TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
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
                        CREATE TABLE %s (id SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT, article_url TEXT NULL, sub_category CHAR(10) NULL, write_date DATETIME NULL, 
                        good SMALLINT(5) UNSIGNED NULL, sad SMALLINT(5) UNSIGNED NULL, angry SMALLINT(5) UNSIGNED NULL, fan SMALLINT(5) UNSIGNED NULL, want SMALLINT(5) UNSIGNED NULL,
                        article_title VARCHAR(100) NULL, main_text TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
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

        article_url = URL
        print("article_url :", article_url)

        sub_category = k2
        #print("sub_category :", sub_category)

        write_date = None
        good_4 = None
        warm_4 = None
        sad_4 = None
        angry_4 = None
        want_4 = None
        cheer_4 = None
        congrats_4 = None
        expect_4 = None
        surprise_4 = None
        fan_4 = None
        man_2 = None
        woman = None
        age_10 = None
        age_20 = None
        age_30 = None
        age_40 = None
        age_50 = None
        age_60 = None

        if k1 < 6:
            # -----------------------
            # 0 : politics
            # 1 : economy
            # 2 : society
            # 3 : culture
            # 4 : world
            # 5 : it
            # -----------------------

            # 기사 작성일
            try:
                write_date = soup.find("span", {"class" : "media_end_head_info_datestamp_time _ARTICLE_DATE_TIME"})
                write_date = write_date.attrs["data-date-time"]
            except:
                write_date = None
            #print("write_date : ", write_date)
            # ---------------------------------------------------------

            # 기사 평가 수집
            # 2022년 4월 27일 기점으로 기사의 평가 방식이 변경됨. 2022년 4월 27일 이후로는 기사 평가가 크게 의미있지 않기 때문에 수집하지 않음.
            if int(self.date_one) <= 20220427:
                try:
                    good_1 = soup.find("a", {"data-type": "like"})
                    good_2 = good_1.find("span", {"class": "u_likeit_list_count _count"})
                    good_3 = good_2.find(string=True)
                    good_4 = re.sub(",", "", good_3)
                    # String으로 하면 None 뜬다 string으로 해야한다.
                except:
                    # print("평가 예외 발생(good)")
                    good_4 = None

                try:
                    warm_1 = soup.find("a", {"data-type": "warm"})
                    warm_2 = warm_1.find("span", {"class": "u_likeit_list_count _count"})
                    warm_3 = warm_2.find(string=True)
                    warm_4 = re.sub(",", "", warm_3)
                except:
                    # print("평가 예외 발생(warm)")
                    warm_4 = None

                try:
                    sad_1 = soup.find("a", {"data-type": "sad"})
                    sad_2 = sad_1.find("span", {"class": "u_likeit_list_count _count"})
                    sad_3 = sad_2.find(string=True)
                    sad_4 = re.sub(",", "", sad_3)
                except:
                    # print("평가 예외 발생(except)")
                    sad_4 = None

                try:
                    angry_1 = soup.find("a", {"data-type": "angry"})
                    angry_2 = angry_1.find("span", {"class": "u_likeit_list_count _count"})
                    angry_3 = angry_2.find(string=True)
                    angry_4 = re.sub(",", "", angry_3)
                except:
                    # print("평가 예외 발생(angry)")
                    angry_4 = None

                try:
                    want_1 = soup.find("a", {"data-type": "want"})
                    want_2 = want_1.find("span", {"class": "u_likeit_list_count _count"})
                    want_3 = want_2.find(string=True)
                    want_4 = re.sub(",", "", want_3)
                except:
                    # print("평가 예외 발생(want)")
                    want_4 = None

            else:
                good_4 = None
                warm_4 = None
                sad_4 = None
                angry_4 = None
                want_4 = None
            #print("# 기사평가 : ", good_4, warm_4, sad_4, angry_4, want_4)
            # ---------------------------------------------------------

            try:
                man_1 = soup.find("div", {"class": "u_cbox_chart_progress u_cbox_chart_male"})
                man_2 = man_1.find(string=True)
                woman = 100 - int(man_2)
                # print("남녀비율 : ", man_2, ":", woman)

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
                # ""를 이용하여 공백을 만들시 sql에서 오류 발생
                #print("남녀비율, 나이비율 없음")
            # ---------------------------------------- 남녀, 나이 비율 ----------------------------------------

        elif k1 == 6:
            # -----------------------
            #  : entertainment
            # -----------------------
            try:
                write_date = soup.find("div", {"class": "article_info"})
                write_date = write_date.find("span", {"class": "author"})
                write_date = write_date.find("em")
                write_date = write_date.find(string=True)
            except:
                write_date = None

            numbers = re.sub(r'[^0-9]', '', write_date)
            fi_forenoon = write_date.find("오전")
            fi_afternoon = write_date.find("오후")
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

            #print("write_date : ", write_date)

            try:
                good_1 = soup.find("a", {"data-type": "like"})
                good_2 = good_1.find("span", {"class": "u_likeit_list_count _count"})
                good_3 = good_2.find(string=True)
                good_4 = re.sub(",", "", good_3)
                # String으로 하면 None 뜬다 string으로 해야한다.
            except:
                # print("평가 예외 발생(good)")
                good_4 = None

            try:
                cheer_1 = soup.find("a", {"data-type": "cheer"})
                cheer_2 = cheer_1.find("span", {"class": "u_likeit_list_count _count"})
                cheer_3 = cheer_2.find(string=True)
                cheer_4 = re.sub(",", "", cheer_3)
            except:
                # print("평가 예외 발생(cheer)")
                cheer_4 = None

            try:
                congrats_1 = soup.find("a", {"data-type": "congrats"})
                congrats_2 = congrats_1.find("span", {"class": "u_likeit_list_count _count"})
                congrats_3 = congrats_2.find(string=True)
                congrats_4 = re.sub(",", "", congrats_3)
            except:
                # print("평가 예외 발생(congrats)")
                congrats_4 = None

            try:
                expect_1 = soup.find("a", {"data-type": "expect"})
                expect_2 = expect_1.find("span", {"class": "u_likeit_list_count _count"})
                expect_3 = expect_2.find(string=True)
                expect_4 = re.sub(",", "", expect_3)
            except:
                # print("평가 예외 발생(expect)")
                expect_4 = None

            try:
                surprise_1 = soup.find("a", {"data-type": "surprise"})
                surprise_2 = surprise_1.find("span", {"class": "u_likeit_list_count _count"})
                surprise_3 = surprise_2.find(string=True)
                surprise_4 = re.sub(",", "", surprise_3)
            except:
                # print("평가 예외 발생(suprise)")
                surprise_4 = None

            try:
                sad_1 = soup.find("a", {"data-type": "sad"})
                sad_2 = sad_1.find("span", {"class": "u_likeit_list_count _count"})
                sad_3 = sad_2.find(string=True)
                sad_4 = re.sub(",", "", sad_3)
            except:
                # print("평가 예외 발생(except)")
                sad_4 = None

        elif k1 == 7:
            # -----------------------
            #  : sports
            # -----------------------
            try:
                write_date = soup.find("div", {"class": "info"})
                write_date = write_date.find("span")
                write_date = write_date.find(string=True)
            except:
                write_date = None

            numbers = re.sub(r'[^0-9]', '', write_date)
            fi_forenoon = write_date.find("오전")
            fi_afternoon = write_date.find("오후")
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

            #print("write_date : ", write_date)

            try:
                good_1 = soup.find("a", {"data-type": "like"})
                good_2 = good_1.find("span", {"class": "u_likeit_list_count _count"})
                good_3 = good_2.find(string=True)
                good_4 = re.sub(",", "", good_3)
                # String으로 하면 None 뜬다 string으로 해야한다.
            except:
                # print("평가 예외 발생(good)")
                good_4 = None

            try:
                sad_1 = soup.find("a", {"data-type": "sad"})
                sad_2 = sad_1.find("span", {"class": "u_likeit_list_count _count"})
                sad_3 = sad_2.find(string=True)
                sad_4 = re.sub(",", "", sad_3)
            except:
                # print("평가 예외 발생(except)")
                sad_4 = None

            try:
                angry_1 = soup.find("a", {"data-type": "angry"})
                angry_2 = angry_1.find("span", {"class": "u_likeit_list_count _count"})
                angry_3 = angry_2.find(string=True)
                angry_4 = re.sub(",", "", angry_3)
            except:
                # print("평가 예외 발생(angry)")
                angry_4 = None

            try:
                fan_1 = soup.find("a", {"data-type": "fan"})
                fan_2 = fan_1.find("span", {"class": "u_likeit_list_count _count"})
                fan_3 = fan_2.find(string=True)
                fan_4 = re.sub(",", "", fan_3)
            except:
                #print("평가 예외 발생(fan)")
                fan_4 = None

            try:
                want_1 = soup.find("a", {"data-type": "want"})
                want_2 = want_1.find("span", {"class": "u_likeit_list_count _count"})
                want_3 = want_2.find(string=True)
                want_4 = re.sub(",", "", want_3)
            except:
                # print("평가 예외 발생(want)")
                want_4 = None


        if k1 < 6:
            title_1 = soup.find("h2", {"id": "title_area"})
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

        #print("article_title : ", title_2)
        #일반뉴스 h2 id title_area
        #일반뉴스 h3 class tts_head
        #연예뉴스 h2 class end_tit
        #스포츠뉴스 h4 class title
        #------------------------------------------- 기사 제목 -------------------------------------------

        main_text_1 = soup.find("div", {"class": "go_trans _article_content"})
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
        #print("main_text : ", main_text_7)

        #------------------------------------------- 기사 제목 -------------------------------------------

        try:
            image_1 = soup.find("div" , {"class" : "go_trans _article_content"})
            if image_1 == None:
                image_1 = soup.find("div" , {"class" : "article_body font1 size3"})
                if image_1 == None:
                    image_1 = soup.find("div", {"class": "news_end font1 size3"})
            image_2 = image_1.find("span", {"class": "end_photo_org"})
            image_3 = image_2.find("img")
            image_4 = image_3.attrs['src']

            col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            image_name = search_list_major_1[k1] + col_date
            image_name = hashlib.md5(image_name.encode()).hexdigest()
            image_path = "E:/Data/Data_img/Data_img_naver/%s/"%search_list_major_1[k1] + "%s_%s"%(search_list_major_1[k1], self.date_one)

            image_loc = image_path + "/" + str(image_name) + ".jpg"
            image_PIL = Image.open(requests.get(image_4, stream=True).raw)
            image_PIL.save(image_loc)
            #print("article_img :", image_loc)

        except:
            image_loc = None
            #print("이미지가 존재하지 않습니다.")

        db = pymysql.connect(host="localhost",
                             port=3306,
                             user='root',
                             passwd='mysql0788',
                             db='nnews_%s' % search_list_major_1[k1],
                             charset='utf8')

        table_name = "%s_" % search_list_major_1[k1] + self.date_one

        try:

            if k1 < 6:
                curs = db.cursor()
                sql1 = """INSERT INTO %s""" % table_name + """(article_url, sub_category, write_date, good, warm, sad, angry, want, man, woman, 
                age_10, age_20, age_30, age_40, age_50, age_60, article_title, main_text, article_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                curs.execute(sql1, (article_url, sub_category, write_date, good_4, warm_4, sad_4, angry_4, want_4, man_2, woman, age_10, age_20, age_30, age_40, age_50, age_60, title_2, main_text_7, image_loc))
                db.commit()
                #print("데이터베이스에 저장완료 #1")
                ti.sleep(0.1)

            elif k1 == 6:
                curs = db.cursor()
                sql1 = """INSERT INTO %s""" % table_name + """(article_url, sub_category, write_date, good, cheer, congrats, expect, surprise, sad, article_title, main_text, article_image) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                curs.execute(sql1, (
                article_url, sub_category, write_date, good_4, cheer_4, congrats_4, expect_4, surprise_4, sad_4, title_2, main_text_7, image_loc))
                db.commit()
                #print("데이터베이스에 저장완료 #2")
                ti.sleep(0.1)

            elif k1 == 7:
                curs = db.cursor()
                sql1 = """INSERT INTO %s""" % table_name + """(article_url, sub_category, write_date, good, sad, angry, fan, want, article_title, main_text, article_image) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                curs.execute(sql1, (
                    article_url, sub_category, write_date, good_4, sad_4, angry_4, fan_4, want_4, title_2, main_text_7, image_loc))
                db.commit()
                #print("데이터베이스에 저장완료 #3")
                ti.sleep(0.1)

            #print("-------------------------------------------------------------------------------------------")

        except Exception as e:
            print("Exception : ", e)

if __name__ == '__main__':
    date_list = ["20180103", "20180104"]
    for date in date_list:
        MainClass = p_data_collect(date)
        MainClass.main_method()


