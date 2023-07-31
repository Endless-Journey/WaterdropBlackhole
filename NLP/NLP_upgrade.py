from PyKomoran import *
import json
import time
import re

class NLP_class:
    def __init__(self):
        self.komoran = Komoran("EXP")
        self.komoran.set_user_dic('C:/Users/euler/Desktop/Dev/Project_helloworld/Alpha/Public/dict.user.txt')
        self.komoran.set_fw_dic('C:/Users/euler/Desktop/Dev/Project_helloworld/Alpha/Public/fwd.user.txt')
        self.tag_list_1 = ["NNP", "NNG", 'SL']
        self.tag_list_2 = ["VV", "XR", "VA"]
        #self.tag_list_2 = []

    def NLP_upgrade_module_NOUNS(self, text_input):
        text_input = text_input.replace("\t", "").replace("\n", "")
        text_input = re.sub("[ㄱ-ㅎ]+", "", text_input)
        text_input = re.sub("[ㅏ-ㅣ]+", "", text_input)
        text_input = re.sub("\s+", " ", text_input)
        text_input = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", text_input)
        text_input = text_input.strip()
        #print(self.komoran.get_plain_text(text_input))

        with open("NLP_upgrade_js_change_typo.json", "r", encoding='UTF-8') as json_file:
            change_list_typo = json.load(json_file)
        with open("NLP_upgrade_js_delete.json", "r", encoding='UTF-8') as json_file:
            delete_list = json.load(json_file)

        for k1 in list(change_list_typo):
            text_input = text_input.replace(k1, change_list_typo[k1])

        pos_result = self.komoran.get_morphes_by_tags(text_input, tag_list=self.tag_list_1)

        for k2 in pos_result:
            if k2 in delete_list:
                pos_result.remove(k2)

        return pos_result

    def NLP_upgrade_module_ALL(self, text_input):
        text_input = text_input.replace("\t", "").replace("\n", "")
        text_input = re.sub("[ㄱ-ㅎ]+", "", text_input)
        text_input = re.sub("[ㅏ-ㅣ]+", "", text_input)
        text_input = re.sub("\s+", " ", text_input)
        text_input = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", text_input)
        text_input = text_input.strip()
        #print(self.komoran.get_plain_text(text_input))

        with open("NLP_upgrade_js_change_typo.json", "r", encoding='UTF-8') as json_file:
            change_list_typo = json.load(json_file)
        with open("NLP_upgrade_js_change_V.json", "r", encoding='UTF-8') as json_file:
            change_list_V = json.load(json_file)
        with open("NLP_upgrade_js_delete.json", "r", encoding='UTF-8') as json_file:
            delete_list = json.load(json_file)

        for k1 in list(change_list_typo):
            text_input = text_input.replace(k1, change_list_typo[k1])

        pos_result_1 = self.komoran.get_morphes_by_tags(text_input, tag_list=self.tag_list_1)
        pos_result_2 = self.komoran.get_morphes_by_tags(text_input, tag_list=self.tag_list_2)

        for k3 in range(0, len(pos_result_2)):
            for k3_1 in list(change_list_V):
                if pos_result_2[k3] == k3_1:
                    pos_result_2.pop(k3)
                    pos_result_2.insert(k3, change_list_V[k3_1])

        pos_result = pos_result_1 + pos_result_2

        for k2 in pos_result:
            if k2 in delete_list:
                pos_result.remove(k2)

        return pos_result




if __name__ == '__main__':
    text = """
    4차 산업혁명으로 표현되는 인공지능(AI), 로봇공학, 빅데이터, 클라우드 등과 같은 기술이 세무대리계에 엄청난 파장을 몰고 올 태세다.

    장기적으로 AI가 세무사를 대신할 것이라는 '어두운 미래'를 걱정하는 목소리부터, 4차 산업혁명 기술에 올라탄 세무사들은 새로운 날개를 달 수 있을 것이라는 '부푼 희망'도 있다.

    엄청난 변화의 예고 속에서도 세무대리계는 아직까지 잠잠한 분위기다. '4차 산업혁명 시대'라는 거창한 문구는 여기저기서 나돌고 있지만 어떻게 대응해야 하고 무엇을 준비해야 할지 등에 대해서는 구체적인 진전이 별로 없다.

    세금에 관한한 세무사라는 조세전문가의 역할이 앞으로도 계속 필요할 수밖에 없을 것이고, 기장-조정-신고와 같은 전통적인 업무와 조사대행, 조세불복과 같은 업무프로세스에 큰 변화가 있겠느냐는 낙관론이 아직까지는 많다.

    주목할 만한 점은 4차 산업혁명이 세무사의 '업무영역'에 어떤 영향을 미칠 것인지에 대해서는 민감하게 반응하고 있다. AI가 결국 '세무사 패싱'을 낳을 것이라는 우려가 이면에 깔려 있다. 한국세무사회도 세무사들의 이같은 우려의 목소리를 받아들여 지난해 4차 산업혁명에 따른 AI 세무서비스 시장 전망과 관련한 연구용역을 냈다.

    이에 발맞춰 최근 세무대리계에는 실시간 데이터 처리, 신속한 회계분석 처리가 가능한 여러 세무회계프로그램이 출현하고 있다. 이들 프로그램의 공통점은 '자동회계처리', 즉 세무사사무소 기장업무의 자동화를 전제로 하고 있다.

    세무사계에는 '자동 회계처리' 프로그램에 대해 우려와 기대의 목소리가 상존한다.

    결국 자동 회계처리 프로그램이 세무사를 대신하게 될 것이라는 걱정과, 자동기장을 발판으로 좀더 생산적인 업무개발에 나설 수 있다는 기대가 나오고 있다. 특히 세무법인과 청년 개업세무사를 중심으로 '자동기장'에 대한 관심이 뜨겁다.


    [출처] 한국세정신문 (http://www.taxtimes.co.kr)
    
    반기를 들다
    
    젊은 대통령
    
    제주도 몇박으로 가셔도 10만원은 드릴텐데 사정상 한달이나 해외가시면 좀 더 드릴 것 같아요
    시모 여행갈 때 입 씻으면 우린 물건 날라와요
    아 물론 오시기 전 집 청소며 반찬 식사준비는 당연하고
    """
    NLP = NLP_class()
    result = NLP.NLP_upgrade_module_NOUNS(text)
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