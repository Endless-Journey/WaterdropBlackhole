import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout, QTextBrowser, QLineEdit, QSizePolicy, QTextEdit
from Info import Secure_core
import pymysql
import json
import re
from PyKomoran import *
from NLP_upgrade import NLP_class


### NLP_upgrade_gui
### PyKomoran의 성능을 "업그레이드"하기 위해 제작되어짐
### 업그레이드를 보조하기 위한 GUI


class MyApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        login_info = Secure_core.Info_db
        self.NLP = NLP_class()
        self.db = pymysql.connect(host=login_info["host"],
                             port=login_info["port"],
                             user=login_info["user"],
                             passwd=login_info["passwd"],
                             charset=login_info["charset"],
                             db='nlp_program')




    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.line_edit_1_1 = QLineEdit(self)
        grid.addWidget(self.line_edit_1_1, 1, 0)

        self.line_edit_1_2 = QLineEdit(self)
        grid.addWidget(self.line_edit_1_2, 2, 0)
        self.line_edit_1_2.returnPressed.connect(self.save_to_js_change_V)
        #엔터키를 눌렀을 때 실행

        self.line_edit_2_1 = QLineEdit(self)
        grid.addWidget(self.line_edit_2_1, 1, 1)

        self.line_edit_2_2 = QLineEdit(self)
        grid.addWidget(self.line_edit_2_2, 2, 1)
        self.line_edit_2_2.returnPressed.connect(self.save_to_js_change)

        self.line_edit_3_1 = QLineEdit(self)
        grid.addWidget(self.line_edit_3_1, 1, 2)
        self.line_edit_3_1.returnPressed.connect(self.save_to_js_delete)

        self.line_edit_4_1 = QLineEdit(self)
        grid.addWidget(self.line_edit_4_1, 1, 3)
        self.line_edit_4_1.returnPressed.connect(self.add_dict_user)

        self.line_edit_4_3 = QTextEdit(self)
        grid.addWidget(self.line_edit_4_3, 5, 4)
        self.line_edit_4_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.line_edit_5_1 = QLineEdit(self)
        grid.addWidget(self.line_edit_5_1, 1, 4)

        self.line_edit_5_2 = QLineEdit(self)
        grid.addWidget(self.line_edit_5_2, 2, 4)

        self.line_edit_5_3 = QLineEdit(self)
        grid.addWidget(self.line_edit_5_3, 3, 4)
        self.line_edit_5_3.returnPressed.connect(self.add_fwd_user)



        self.label_1 = QLabel("change_list_V", self)
        grid.addWidget(self.label_1, 0, 0)

        self.label_2 = QLabel("change_list_typo", self)
        grid.addWidget(self.label_2, 0, 1)

        self.label_3 = QLabel("delete_list", self)
        grid.addWidget(self.label_3, 0, 2)

        self.label_4 = QLabel("add_dict_user", self)
        grid.addWidget(self.label_4, 0, 3)

        self.label_5 = QLabel("add_fwd_user", self)
        grid.addWidget(self.label_5, 0, 4)

        self.label_5 = QLabel("output", self)
        grid.addWidget(self.label_5, 4, 0)

        self.label_6 = QLabel("add_list_to_dict.user", self)
        grid.addWidget(self.label_6, 4, 4)

        self.text_1 = QTextBrowser(self)
        grid.addWidget(self.text_1, 5, 0, 1, 4)
        #(row, column, rowspan, columnspan)
        self.text_1.resize(1200, 300)

        self.btn_1 = QPushButton("load new date", self)
        grid.addWidget(self.btn_1, 6, 0)
        self.btn_1.resize(1200, 50)
        self.btn_1.clicked.connect(self.load_data)

        self.btn_2 = QPushButton("add_list_to_dict.user", self)
        grid.addWidget(self.btn_2, 6, 4)
        self.btn_2.clicked.connect(self.add_dict_user_list)

        self.btn_3 = QPushButton("refresh NLP", self)
        grid.addWidget(self.btn_3, 6, 1)
        self.btn_3.clicked.connect(self.refresh_NLP)

        self.setWindowTitle('NLP_Upgrade_Gui')
        self.move(300, 300)
        self.resize(1600, 500)
        self.show()
        self.a = 0

    def refresh_NLP(self):
        self.NLP = NLP_class()

    def save_to_js_change(self):
        change_before = self.line_edit_2_1.text()
        change_after = self.line_edit_2_2.text()
        row = {change_before: change_after}

        with open("NLP_upgrade_js_change_typo.json", "r", encoding="UTF-8") as json_file:
            json_data = json.load(json_file)

        json_data.update(row)
        with open("NLP_upgrade_js_change_typo.json", "w", encoding="UTF-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False)

        self.line_edit_2_1.clear()
        self.line_edit_2_2.clear()

    def save_to_js_change_V(self):
        change_before = self.line_edit_1_1.text()
        change_after = self.line_edit_1_2.text()
        row = {change_before: change_after}

        with open("NLP_upgrade_js_change_V.json", "r", encoding="UTF-8") as json_file:
            json_data = json.load(json_file)

        json_data.update(row)
        with open("NLP_upgrade_js_change_V.json", "w", encoding="UTF-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False)

        self.line_edit_1_1.clear()
        self.line_edit_1_2.clear()

    def save_to_js_delete(self):
        delete_word = self.line_edit_3_1.text()
        with open("NLP_upgrade_js_delete.json", "r", encoding="UTF-8") as json_file:
            list_data = json.load(json_file)
        list_data.append(delete_word)
        with open("NLP_upgrade_js_delete.json", "w", encoding="UTF-8") as json_file:
            json.dump(list_data, json_file, ensure_ascii=False)
        self.line_edit_3_1.clear()

    # 명사를 추가한다
    def add_dict_user(self):
        with open('dict.user.txt', 'a', encoding='UTF-8') as f:
            word = self.line_edit_4_1.text()
            pos = "NNP"

            #'w' 로 열면 내용이 모두 사라진다 주의
            data = word + "\t" + pos + "\n"
            f.write(data)
            self.line_edit_4_1.clear()

    def add_fwd_user(self):
        with open('fwd.user.txt', 'a', encoding='UTF-8') as f:
            word_origin = self.line_edit_5_1.text()
            word_v_1 = self.line_edit_5_2.text()
            word_v_2 = self.line_edit_5_3.text()

            data = word_origin + "\t" + word_v_1 + "/VV" + " " + word_v_2 + "/EC" + "\n"
            f.write(data)

            self.line_edit_5_1.clear()
            self.line_edit_5_2.clear()
            self.line_edit_5_3.clear()

    def add_dict_user_list(self):
        text = self.line_edit_4_3.toPlainText()

        rmve_1 = "\(.*\)|\s-\s.*"
        rmve_2 = "\[.*\]|\s-\s.*"
        del_list = ["ⓚ", "ⓛ", "ⓑ"]


        split_list_1 = text.split("\n")
        split_list_2 = []

        for part in split_list_1:
            if len(part.strip()) == 0:
                continue
            part = re.sub(rmve_1, "", part)
            part = re.sub(rmve_2, "", part)
            find_semi = part.find(":")
            find_dash = part.find("-")

            if find_semi >= 0:
                part = part[0:find_semi]
            if find_dash >= 0:
                part = part[0:find_dash]

            for del_element in del_list:
                part = re.sub(del_element, "", part)
            split_list_2.append(part.strip())

        with open('dict.user.txt', 'a', encoding="utf-8") as f:
            for part in split_list_2:
                data = part + "\t" + "NNP" + "\n"
                f.write(data)

        self.line_edit_4_3.clear()


    def load_data(self):
        curs = self.db.cursor()
        sql = """
        SELECT article_text FROM text_for_nlp LIMIT 1;"""
        curs.execute(sql)
        result = curs.fetchall()
        result = result[0][0]
        result = result.replace("\t", "").replace("\n", "")
        result = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", result)
        for part in re.split('\.', result):
            str_part_result = ""
            if len(part) == 0:
                continue
            self.text_1.append(part)

            part_result = self.NLP.NLP_upgrade_module_ALL(part)
            str_part_result = ",".join(part_result)
            self.text_1.append(str_part_result)
            self.text_1.append("---------------------------------------")


        self.text_1.append("**************************************************************")
        self.text_1.append("--------------------------------------------------------------")
        sql_delete = """DELETE FROM text_for_nlp WHERE (id<= (SELECT MIN(id) FROM (SELECT id FROM text_for_nlp order by id ASC LIMIT 1) AS min_id));
        """
        curs.execute(sql_delete)
        self.db.commit()
        #self.text_1.repaint()
        self.a += 1



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   ex.show()
   sys.exit(app.exec_())