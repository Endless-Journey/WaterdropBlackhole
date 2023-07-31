import pymysql
from Info import Secure_core, Site_info

login_info = Secure_core.Info_db
module_dict = Site_info.Info

date_Ymd = "20230730"
module_list = []
module_list_original = list(module_dict.keys())
for k1 in module_list_original:
    k1 = k1.replace("Cosmonaut_", "")
    module_list.append(k1)


db_save = pymysql.connect(host=login_info["host"],
                          port=login_info["port"],
                          user=login_info["user"],
                          passwd=login_info["passwd"],
                          charset=login_info["charset"],
                          db="nlp_program")
curs_save = db_save.cursor()


for k2 in module_list:
    db = pymysql.connect(host=login_info["host"],
                         port=login_info["port"],
                         user=login_info["user"],
                         passwd=login_info["passwd"],
                         charset=login_info["charset"],
                         db='db_%s' %k2)
    curs = db.cursor()
    table_name = "db_%s_%s"%(k2, date_Ymd)
    try:
        sql = """
        SELECT article_title, article_text, article_comment FROM %s LIMIT 200;
        """ % (table_name)
        curs.execute(sql)
        result = curs.fetchall()
    except:
        continue

    text_list = []
    for k4 in result:
        text_all = ""
        for k5 in range(0, 3):
            if k4[k5] == None:
                continue
            text_all += k4[k5]

        sql_save = """INSERT INTO text_for_nlp (article_text) VALUES (%s);
        """
        curs_save.execute(sql_save, (text_all))
        db_save.commit()

        text_list.append(text_all)


    #print(text_list)



