from datetime import datetime, date
from PIL import Image
import requests
import hashlib
import os
import pymysql
import Secure_core
import re
import urllib.request
import time
import io
import cv2
import numpy as np


class processor_class:
    def __init__(self, site, list_URL, list_category, rd, page_str):
        self.site = site
        self.list_URL = list_URL
        self.list_category = list_category
        self.rd = rd
        self.page_str = page_str
        # ---변수---
        self.col_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.date_Ymd = date.today().strftime('%Y%m%d')
        self.module_name = "Cosmonaut_" + self.site
        self.login_info = Secure_core.Info_db
        self.table_1 = "db_%s_1_" % self.site + self.date_Ymd

        self.db = pymysql.connect(host=self.login_info["host"],
                                  port=self.login_info["port"],
                                  user=self.login_info["user"],
                                  passwd=self.login_info["passwd"],
                                  charset=self.login_info["charset"],
                                  db='db_%s' % self.site)
        self.db.set_charset("utf8mb4")
        self.curs = self.db.cursor()

    def create_table(self):
        try:
            sql_1 = """
                CREATE TABLE %s
                (id MEDIUMINT(6) UNSIGNED AUTO_INCREMENT NOT NULL, col_date DATETIME NOT NULL, category VARCHAR(20) NOT NULL,  
                article_url TEXT NOT NULL, article_title TEXT NOT NULL, good MEDIUMINT(8) NULL, bad MEDIUMINT(8) NULL, hits MEDIUMINT(8) NULL,
                article_text TEXT NULL, article_comment TEXT NULL, article_image TEXT NULL, PRIMARY KEY(`id`));
                """ % self.table_1
            self.curs.execute(sql_1)
            self.db.commit()
            print("###CREATE TABLE###")
        except Exception as e:
            print("*Exception_0_1 : ", e)
            print("###table already exist")
        # ---table create---

    def create_dir(self):
        mkdir_path = "E:/Data/Data_img/Data_img_%s" % self.site
        mkdir_name = self.site + "_" + self.date_Ymd
        try:
            os.makedirs(os.path.join(mkdir_path, mkdir_name))
        except Exception as e:
            print("*Exception_0_2 : ", e)
            print("###directory already exist")
        # ---directory create---

    def select_recent_article(self, k0):
        recent_article_url = []
        try:
            sql_2_1 = """
                SELECT article_url FROM db_%s_duplication_check;
                """ % self.site
            sql_2_2 = """
                SELECT article_url FROM db_%s_duplication_check WHERE (category = '%s');
                """ % (self.site, self.list_category[k0])
            if len(self.list_category) == 1:
                self.curs.execute(sql_2_1)
            else:
                self.curs.execute(sql_2_2)
            recent_article_url = self.curs.fetchall()
            print("###load data for duplication check from sql")
        except Exception as e:
            error = "Exception_0_2 : " + str(e)
            self.err_report(self.col_date, error)
        return recent_article_url

    def duplication_check_sql(self, k1, recent_article_url, URL_2):
        check = False
        before = self.page_str + str(k1)
        try:
            for k2_1 in range(0, len(recent_article_url)):
                URL_2_temp_1 = URL_2.replace(before, "")
                recent_article_url_temp = recent_article_url[k2_1][0]
                recent_article_url_temp = recent_article_url_temp.replace(self.page_str + "0", "").replace(
                    self.page_str + "1", "").replace(self.page_str + "2", "")
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
        # ---duplication check for sql---
        return check

    def duplication_check(self, k1, URL_2, article_url_list, article_num):
        article_compare = False
        before = self.page_str + str(k1)
        URL_2_temp_2 = URL_2.replace(before, "")
        for k2_2 in article_url_list:
            if k2_2 == URL_2_temp_2:
                article_compare = True
                break
        if article_compare == True:
            print("###duplication detected!")
            # print(k2_2, "v", URL_2_temp_2)
            return
        else:
            if len(article_url_list) == article_num * 3:
                article_url_list.pop(0)
            article_url_list.append(URL_2_temp_2)

    def save_info(self, k1, col_date, category, URL_2, article_title, good, bad, hits, article_text, article_comment,
                  image_dir):
        sql_3 = """
                INSERT INTO %s""" % self.table_1 + """(col_date, category, article_url, article_title, good, bad, hits, article_text, article_comment, article_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        self.curs.execute(sql_3, (
        col_date, category, URL_2, article_title, good, bad, hits, article_text, article_comment, image_dir))
        self.db.commit()
        # ---save into normal table---

        sql_4 = """
                INSERT INTO db_%s_duplication_check""" % self.site + """(col_date, category, article_url)
                VALUES (%s, %s, %s)
                """
        if k1 == 0 or k1 == 1 or k1 == 2:
            self.curs.execute(sql_4, (col_date, category, URL_2))
            self.db.commit()
        time.sleep(self.rd)

    def duplication_reset(self, k0, article_num):
        sql_5_1 = """
        DELETE FROM db_%s_duplication_check WHERE (col_date <
        ( SELECT MIN(col_date) FROM (SELECT col_date FROM db_%s_duplication_check ORDER BY col_date DESC LIMIT %s) AS min_col_data));
        """ % (self.site, self.site, str(article_num * 2 + 1))
        sql_5_2 = """
        DELETE FROM db_%s_duplication_check WHERE (col_date <
        ( SELECT MIN(col_date) FROM (SELECT col_date FROM db_%s_duplication_check where category = '%s' ORDER BY col_date DESC LIMIT %s) AS min_col_data)) and (category = '%s');
        """ % (self.site, self.site, self.list_category[k0], str(article_num * 2 + 1), self.list_category[k0])
        if len(self.list_category) == 1:
            self.curs.execute(sql_5_1)
        else:
            self.curs.execute(sql_5_2)
        self.db.commit()
        print("###db duplication check table reset")
        time.sleep(self.rd)

    def status_logging(self, col_date, status, data_num):
        login_info = Secure_core.Info_db
        db = pymysql.connect(host=login_info["host"],
                             port=login_info["port"],
                             user=login_info["user"],
                             passwd=login_info["passwd"],
                             charset=login_info["charset"],
                             db="cosmonaut_log")
        db.set_charset("utf8mb4")
        curs = db.cursor()
        sql_e = """
                    INSERT INTO cosmonaut_log""" + """(col_date, module_name, module_status, article_num)
                    VALUES (%s, %s, %s, %s)
                    """
        curs.execute(sql_e, (col_date, self.module_name, status, data_num))
        db.commit()

    def delete_notice(self, list_articles, tag):
        for k1_1 in list_articles:
            k1_fi = str(k1_1).find(tag)
            # type 'bs4.element.Tag' >>> type 'str'
            if k1_fi >= 0:
                list_index = list_articles.index(k1_1)
                del list_articles[list_index]
                list_articles.insert(list_index, "deletedelete")

        for k1_2 in range(0, list_articles.count("deletedelete")):
            list_articles.remove("deletedelete")
        # ---delete notice---

        return list_articles

    def image_process(self, img_src, col_date, domain):
        if img_src[0:4] == "http":
            img_src = img_src
        elif img_src[0:2] == "//":
            img_src = "https:" + img_src
        else:
            img_src = domain + img_src

        png_check_1 = img_src.find("png")
        png_check_2 = img_src.find("PNG")
        png_check = 0
        if (png_check_1 >= 0 or png_check_2 >= 0) == 1:
            png_check = 1

        gif_check = img_src.find(".gif")

        img_name = "img_%s_" % self.site + col_date
        img_name = hashlib.md5(img_name.encode()).hexdigest()

        mkdir_path = "E:/Data/Data_img/Data_img_%s" % self.site
        mkdir_name = self.site + "_" + self.date_Ymd
        path = mkdir_path + "/" + mkdir_name

        img_dir = path + "/" + img_name

        try:
            image_PIL = Image.open(requests.get(img_src, stream=True).raw)
            height, width = image_PIL.height, image_PIL.width

            if gif_check >= 0:
                return None

            if height >= width:
                dx = 150 / width
                width_resize = round(width * dx)
                height_resize = round(height * dx)
                image_resize = image_PIL.resize((width_resize, height_resize))
            else:
                dy = 150 / height
                width_resize = round(width * dy)
                height_resize = round(height * dy)
                image_resize = image_PIL.resize((width_resize, height_resize))

            if png_check == 1:
                image_loc = path + "/" + str(img_name) + ".png"
                image_resize.convert('RGB')
                image_resize.save(image_loc)
            else:
                image_loc = path + "/" + str(img_name) + ".jpg"
                image_resize.save(image_loc)
        except:
            if png_check == 1:
                image_loc = path + "/" + str(img_name) + ".png"
            else:
                image_loc = path + "/" + str(img_name) + ".jpg"

            resp = urllib.request.urlopen(img_src)
            image = np.asarray(bytearray(resp.read()), dtype='uint8')
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            height, width = image.shape[0], image.shape[1]

            if height >= width:
                dx = 150 / width
                width_resize = round(width * dx)
                height_resize = round(height * dx)
                image_resize = cv2.resize(image, (width_resize, height_resize))
            else:
                dy = 150 / height
                width_resize = round(width * dy)
                height_resize = round(height * dy)
                image_resize = cv2.resize(image, (width_resize, height_resize))

            cv2.imwrite(image_loc, image_resize)

        return img_dir

    def err_report(self, col_date, error):
        print(error)
        print("---------------------------------------------------")
        db = pymysql.connect(host=self.login_info["host"],
                             port=self.login_info["port"],
                             user=self.login_info["user"],
                             passwd=self.login_info["passwd"],
                             charset=self.login_info["charset"],
                             db="cosmonaut_log")
        db.set_charset("utf8mb4")
        curs = db.cursor()
        sql_e = """
                INSERT INTO cosmonaut_error_log""" + """(col_date, module_name, error_exp)
                VALUES (%s, %s, %s)
                """
        curs.execute(sql_e, (col_date, self.module_name, error))
        db.commit()
        time.sleep(self.rd)

    def text_analyze(self, article_text):
        text_delete = ["귀하의 브라우저는 html5 video를 지원하지 않습니다\.",
                       "죄송합니다, 회원에게만 공개된 글입니다로그인 후 이용해 주세요 (즉시 가입 가능) 로그인   회원가입",
                       "이 브라우저는 비디오태그를 지원하지 않습니다. 크롬을 사용 권장합니다\.",
                       "Video 태그를 지원하지 않는 브라우저입니다\.",
                       "[삭제 되었습니다]",
                       "비디오 태그를 지원하지 않는 브라우저입니다",
                       "(본인이 직접 삭제한 댓글입니다)",
                       "사진 터치 후 저장하세요",
                       "죄송합니다, 회원에게만 공개된 글입니다로그인 후 이용해 주세요 (즉시 가입 가능) 로그인   회원가입"]

        article_text = article_text.strip()
        for k in text_delete:
            article_text = re.sub(k, "", article_text)

        return article_text
