import json

merge_list = {"빅":{"데이터" : "빅데이터",
                    "세일":"빅세일"},
               "조세": {"전문가":"조세전문가"},
               "빅데이터" : {"클라우드":"빅데이터클라우드"}
               }

change_list = {"나ㄷ오":"나오다"}

delete_list = ["http", "하", "이", "는", "고", "어", "아", "에", "게", "도", "은", "음", "면", "나", "있", "았", "안", "거", "?", "거", "는데", "ㄴ", "ㄹ", "ㅁ", "을", "올", "다"]


#with open("NLP_upgrade_js_delete.json", "w", encoding='UTF-8') as json_file:
    #json.dump(delete_list, json_file, indent=2, ensure_ascii=False)


with open("NLP/NLP_upgrade_js_delete.json", "r", encoding="UTF-8") as json_file:
    list_data = json.load(json_file)
list_data.append("test")
with open("NLP/NLP_upgrade_js_delete.json", "w", encoding="UTF-8") as json_file:
    json.dump(list_data, json_file, ensure_ascii=False)


"""
with open("NLP/NLP_upgrade_js_change_typo.json", "r", encoding="UTF-8") as json_file:
    json_data = json.load(json_file)
    print(json_data)

change_before = "상냥하"
change_after = "상냥하다"
row = {change_before:change_after}
json_data.update(row)
with open("NLP/NLP_upgrade_js_change_typo.json", "w", encoding="UTF-8") as json_file:
    json.dump(json_data, json_file, ensure_ascii=False)
print(json_data)


with open("NLP/NLP_upgrade_js_merge.json", "r", encoding='UTF-8') as json_file:
    json_data = json.load(json_file)
    #json_data = dict(json_data)

print(json_data)
update_1 = {"라aa": {"파엘": "라파엘"}}
json_data.update(update_1)
print(json_data)
with open("NLP/NLP_upgrade_js_merge.json", "w", encoding='UTF-8') as json_file:
    update_1 = {"라": {"파엘": "라파엘"}}
    json_data.update(update_1)
    print(json_data)

    json.dump(json_data, json_file, ensure_ascii=False)
"""

#print(json_data)