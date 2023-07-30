from Cosmonaut import Cosmonaut_ruliweb
from Alpha.Cosmonaut_site import Cosmonaut_dogdrip
from Alpha.Cosmonaut_site import Cosmonaut_instiz
from Alpha.Cosmonaut_site import Cosmonaut_inven
from Alpha.Cosmonaut_site import Cosmonaut_theqoo
from Alpha.Cosmonaut_site import Cosmonaut_ppomppu
from Alpha.Cosmonaut_site import Cosmonaut_ruliweb
from Alpha.Cosmonaut_site import Cosmonaut_todayhumor
from Alpha.Cosmonaut_site import Cosmonaut_ygosu
from Alpha.Cosmonaut_site import Cosmonaut_82cook
from Alpha.Cosmonaut_site import Cosmonaut_bobaedream
from Alpha.Cosmonaut_site import Cosmonaut_etoland
from Alpha.Cosmonaut_site import Cosmonaut_gasengi
from Alpha.Cosmonaut_site import Cosmonaut_hygall
from Alpha.Cosmonaut_site import Cosmonaut_mania
from Alpha.Cosmonaut_site import Cosmonaut_humoruniv
from Alpha.Cosmonaut_site import Cosmonaut_quasarzone
from Alpha.Cosmonaut_site import Cosmonaut_dmitory
from Alpha.Cosmonaut_site import Cosmonaut_tgd
from Alpha.Cosmonaut_site import Cosmonaut_cboard
from Alpha.Cosmonaut_site import Cosmonaut_theyouthdream
from Alpha.Cosmonaut_site import Cosmonaut_orbi
from Alpha.Cosmonaut_site import Cosmonaut_arcalive
from Alpha.Cosmonaut_site import Cosmonaut_blind
from Alpha.Cosmonaut_site import Cosmonaut_gigglehd
from Alpha.Cosmonaut_site import Cosmonaut_wetrend
from Alpha.Cosmonaut_site import Cosmonaut_OKKY

import time
#5m : 300, 10m : 600, 30m : 1800, 1h : 3600,  2h : 7200, 3h : 10800, 6h : 21600
Info = {
        "Cosmonaut_dogdrip" : {"name" : "dogdrip",
                               "function" : Cosmonaut_dogdrip.method_dogdrip,
                               "c_time" : 600,
                               "start_time" : time.time()},
        "Cosmonaut_instiz" :{"name" : "instiz",
                             "function" : Cosmonaut_instiz.method_instiz,
                             "c_time" : 300,
                             "start_time" : time.time()},
        "Cosmonaut_inven": {"name" : "inven",
                            "function": Cosmonaut_inven.method_inven,
                            "c_time": 300,
                            "start_time" : time.time()},
        "Cosmonaut_theqoo": {"name" : "theqoo",
                             "function": Cosmonaut_theqoo.method_theqoo,
                             "c_time": 300,
                             "start_time" : time.time()},
        "Cosmonaut_ppomppu": {"name" : "ppomppu",
                              "function": Cosmonaut_ppomppu.method_ppomppu,
                             "c_time": 2400,
                             "start_time": time.time()},
        "Cosmonaut_ruliweb": {"name" : "ruliweb",
                              "function": Cosmonaut_ruliweb.method_ruliweb,
                             "c_time": 300,
                             "start_time": time.time()},
        "Cosmonaut_todayhumor": {"name" : "todayhumor",
                                 "function": Cosmonaut_todayhumor.method_todayhumor,
                             "c_time": 8000,
                             "start_time": time.time()},
        "Cosmonaut_ygosu": {"name" : "ygosu",
                            "function": Cosmonaut_ygosu.method_ygosu,
                             "c_time": 1800,
                             "start_time": time.time()},
        "Cosmonaut_82cook": {"name" : "82cook",
                             "function": Cosmonaut_82cook.method_82cook,
                            "c_time": 7200,
                            "start_time": time.time()},
        "Cosmonaut_bobaedream": {"name" : "bobaedream",
                                 "function": Cosmonaut_bobaedream.method_bobaedream,
                                "c_time": 1200,
                                "start_time": time.time()},
        "Cosmonaut_etoland": {"name" : "etoland",
                              "function": Cosmonaut_etoland.method_etoland,
                            "c_time": 600,
                            "start_time": time.time()},
        "Cosmonaut_gasengi": {"name" : "gasengi",
                              "function": Cosmonaut_gasengi.method_gasengi,
                            "c_time": 3600,
                            "start_time": time.time()},
        "Cosmonaut_hygall": {"name" : "hygall",
                             "function": Cosmonaut_hygall.method_hygall,
                            "c_time": 1800,
                            "start_time": time.time()},
        "Cosmonaut_mania": {"name" : "mania",
                            "function": Cosmonaut_mania.method_mania,
                             "c_time": 3600,
                             "start_time": time.time()},
        "Cosmonaut_humoruniv": {"name" : "humoruniv",
                                "function": Cosmonaut_humoruniv.method_humoruniv,
                                "c_time": 300,
                                "start_time": time.time()},
        "Cosmonaut_quasarzone": {"name" : "quasarzone",
                                 "function": Cosmonaut_quasarzone.method_quasarzone,
                                 "c_time": 2400,
                                 "start_time": time.time()},
        "Cosmonaut_dmitory": {"name" : "dmitory",
                              "function": Cosmonaut_dmitory.method_dmitory,
                              "c_time": 3600,
                              "start_time": time.time()},
        "Cosmonaut_tgd": {"name" : "tgd",
                          "function": Cosmonaut_tgd.method_tgd,
                          "c_time": 1800,
                          "start_time": time.time()},
        "Cosmonaut_cboard": {"name": "cboard",
                          "function": Cosmonaut_cboard.method_cboard,
                          "c_time": 1800,
                          "start_time": time.time()},
        "Cosmonaut_theyouthdream": {"name": "theyouthdream",
                             "function": Cosmonaut_theyouthdream.method_theyouthdream,
                             "c_time": 1800,
                             "start_time": time.time()},
        "Cosmonaut_orbi": {"name": "orbi",
                            "function": Cosmonaut_orbi.method_orbi,
                            "c_time": 1800,
                            "start_time": time.time()},
        "Cosmonaut_arcalive": {"name": "arcalive",
                           "function": Cosmonaut_arcalive.method_arcalive,
                           "c_time": 300,
                           "start_time": time.time()},
        "Cosmonaut_blind": {"name": "blind",
                               "function": Cosmonaut_blind.method_blind,
                               "c_time": 1800,
                               "start_time": time.time()},
        "Cosmonaut_gigglehd": {"name": "gigglehd",
                            "function": Cosmonaut_gigglehd.method_gigglehd,
                            "c_time": 21600,
                            "start_time": time.time()},
        "Cosmonaut_wetrend": {"name": "wetrend",
                               "function": Cosmonaut_wetrend.method_wetrend,
                               "c_time": 3600,
                               "start_time": time.time()},
        "Cosmonaut_OKKY": {"name": "OKKY",
                              "function": Cosmonaut_OKKY.method_OKKY,
                              "c_time": 21600,
                              "start_time": time.time()},
    }