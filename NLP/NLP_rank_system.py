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
SELECT article_text FROM db_ruliweb_20230730;
"""
curs.execute(sql)
result = curs.fetchall()

NLP_list = ""

for items in result:
    NLP_list += items[0]
    #print(items[0])

NLP = NLP_class()
result = NLP.NLP_upgrade_module_NOUNS(NLP_list)
print(result)
print(result.sort())

dict_origin = {}


for noun in result:
    if dict_origin.get(noun) is None:
        dict_origin[noun] = 1
    else:
        cnt = dict_origin[noun]
        dict_origin[noun] = cnt + 1

dict_sort = sorted(dict_origin.items(), key=lambda x : x[1])
dict_sort.reverse()
print(dict_sort)
