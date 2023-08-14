from datetime import datetime, timedelta
import pymysql
from Alpha.Public import Secure_core, Site_info
import pandas as pd
import matplotlib.pyplot as plt
import os


#pd.set_option('display.max_columns', None)

login_info = Secure_core.Info
Year = "2022"
month = "02"
day = "13"

date_Ymd = Year + month + day

report_path = "E:\Database_report"
report_name = "Daily_report_" + date_Ymd + ".txt"
#f = open(os.path.join(report_path, report_name), "w")

module_dict = Site_info.Info

module_list = []
df_list_1 = []
df_list_2 = []
module_list_original = list(module_dict.keys())


for k1 in module_list_original:
    k1 = k1.replace("Cosmonaut_", "")
    module_list.append(k1)


for k2 in module_list:
    db = pymysql.connect(host=login_info["host"],
                         port=login_info["port"],
                         user=login_info["user"],
                         passwd=login_info["passwd"],
                         charset=login_info["charset"],
                         db="db_%s"%k2)
    curs = db.cursor()
    table_name = "db_%s_1_%s"%(k2, date_Ymd)
    sql = """
    SELECT COUNT(id) FROM %s"""%table_name
    curs.execute(sql)
    result = curs.fetchall()
    temp = "%s : %s"%(k2, result[0][0])
    df_list_1.append(temp)

    time_range_0 = datetime(int(Year), int(month.replace("0", "")), int(day.replace("0", "")), 0, 0, 0)
    time_range_1 = datetime(int(Year), int(month.replace("0", "")), int(day.replace("0", "")), 0, 9, 59)
    df_list_2_temp = []
    for k3 in range(0, 144):


        sql_2 = """
        SELECT COUNT(id) FROM %s WHERE col_date BETWEEN '%s' AND '%s';"""%(table_name, time_range_0, time_range_1)
        curs.execute(sql_2)
        temp_2 = curs.fetchall()
        df_list_2_temp.append(temp_2[0][0])

        time_range_0 += timedelta(minutes=10)
        time_range_1 += timedelta(minutes=10)


    df_list_2.append(df_list_2_temp)

    db_path = "E:\Database\Data\db_%s"
    db_name = "db_%s_1_%s"%(k2, date_Ymd)


df_list_2 = pd.DataFrame(df_list_2, index = module_list_original)
print(df_list_2)
count_all = []
for k4 in range(0, 144):
    list_temp = df_list_2.loc[:,k4]

    temp = 0
    for k5 in list_temp:
        temp += k5
    count_all.append(temp)


df_count_all = pd.DataFrame(count_all).transpose()

print(df_count_all)
plt_name = "plt_%s"%date_Ymd
plt.figure(figsize=(16, 6))
plt.bar(df_count_all.columns, df_count_all.loc[0,:])
#plt.hist(df_count_all[1:2], bins = 1)
plt.savefig(os.path.join(report_path, plt_name))
plt.show()



print(df_list_1)
df_count = []
print(len(df_list_1))
while True:
    if len(df_list_1) == 0:
        break
    temp_list = []
    for _ in range(0, 4):
        temp_list.append(df_list_1[0])
        df_list_1.pop(0)
        if len(df_list_1) == 0:
            break
    df_count.append(temp_list)



df_count = pd.DataFrame(df_count)

print(df_count)

#f.write("Daily_report_%s \n"%date_Ymd)f







#f.close()