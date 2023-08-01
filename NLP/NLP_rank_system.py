import pymysql

from Info import Secure_core
from NLP.NLP_upgrade import NLP_class

login_info = Secure_core.Info_db
NLP = NLP_class()
db = pymysql.connect(host=login_info["host"],
                          port=login_info["port"],
                          user=login_info["user"],
                          passwd=login_info["passwd"],
                          charset=login_info["charset"],
                          db='db_ruliweb')

curs = db.cursor()
sql = """
SELECT article_title, article_text, article_comment FROM db_ruliweb_20230801 WHERE col_date >= '2023-08-01 18:20:00' AND col_date <= '2023-08-01 21:20:00';
"""
curs.execute(sql)
result = curs.fetchall()

NLP_list = []

for items in result:
    article_contents = ""

    items0 = items[0]
    if items0 is not None:
        article_contents += items[0]

    items1 = items[1]
    if items1 is not None:
        article_contents += items[1]

    items2 = items[2]
    if items2 is not None:
        article_contents += items[2]

    NLP_result = NLP.NLP_upgrade_module_NOUNS(article_contents)

    NLP_list += NLP_result

dict_origin = {}

for noun in NLP_list:
    if dict_origin.get(noun) is None:
        dict_origin[noun] = 1
    else:
        cnt = dict_origin[noun]
        dict_origin[noun] = cnt + 1

dict_sort = sorted(dict_origin.items(), key=lambda x : x[1])
dict_sort.reverse()
print(dict_sort)
