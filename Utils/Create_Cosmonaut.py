import pymysql
from Info import Secure_core
import os

#웹사이트 수집을 위한 파일 생성

site_name = "dogdrip"
login_info = Secure_core.Info_db

#1. 크롤링 스크립트 생성

try:
    py_cosmonaut = open("Cosmonaut_example.py", encoding="UTF-8")
    py_cosmonaut_data = py_cosmonaut.read()
    py_name = "../Cosmonaut/Cosmonaut_" + site_name + ".py"
    f = open(py_name, 'w', encoding="UTF-8")
    f.write(py_cosmonaut_data)
    f.close()
    print("create [python pile] success")
except Exception as e:
    print("python pile already exist Error :", e)


#-------------------------------------------------------------------------

#2. 스키마 생성
try:
    db = pymysql.connect(host=login_info["host"],
                         port=login_info["port"],
                         user=login_info["user"],
                         passwd=login_info["passwd"],
                         charset=login_info["charset"])
    db.set_charset("utf8mb4")
    curs = db.cursor()
    schema_name = "db_" + site_name

    sql = """CREATE SCHEMA %s;"""%schema_name
    curs.execute(sql)
    db.commit()
    print("create [schema] success")
except Exception as e:
    print("db already exist Error :", e)

#-------------------------------------------------------------------------

#3. 중복 체크 테이블 생성
try:
    db_table = pymysql.connect(host=login_info["host"],
                               port=login_info["port"],
                               user=login_info["user"],
                               passwd=login_info["passwd"],
                               charset=login_info["charset"],
                               db=schema_name)
    db_table.set_charset("utf8mb4")
    curs_table = db_table.cursor()

    sql_table = """CREATE TABLE db_%s_duplication_check 
    (id MEDIUMINT(6) UNSIGNED AUTO_INCREMENT NOT NULL, col_date DATETIME NOT NULL, category VARCHAR(20) NOT NULL, article_url TEXT NOT NULL, PRIMARY KEY(`id`));
    """%site_name
    curs_table.execute(sql_table)
    db_table.commit()
    print("create [table] success")
except Exception as e:
    print("table already exist Error :", e)

#-------------------------------------------------------------------------

#4. 이미지 저장 폴더 생성
try:
    mkdir_path = "E:\Data\Data_img"
    mkdir_name = "Data_img_%s"%site_name
    os.makedirs(os.path.join(mkdir_path, mkdir_name))
except Exception as e:
    print("create [img directory] success Error :", e)