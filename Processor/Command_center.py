import multiprocessing
import time
from Alpha.Public import Site_info

if __name__ == '__main__':
    module_dict = Site_info.Info
    module_list_original = list(module_dict.keys())
    module_list = list(module_dict.keys())
    core_num = 4

    s0 = 0
    while True:
        start_module = time.time()
        end = time.time()
        timer_dict = {}

        for k1 in range(0, len(module_list_original)):
            timer_dict[module_list_original[k1]] = end - module_dict[module_list_original[k1]]["start_time"]

        print("timer : ", timer_dict)

        print("module_list_before :", module_list)
        s2 = 0
        while s2 <= 10:
            for k3 in range(0, core_num):
                for k4 in range(0, len(module_list_original)):
                    if (module_list[k3] == module_list_original[k4]) and (
                            1 < timer_dict[module_list_original[k4]] < module_dict[module_list_original[k4]][
                        "c_time"]) and (s0 == 1):
                        temp = module_list[k3]
                        del module_list[k3]
                        module_list.append(temp)

            breaker = []
            for k10 in range(0, core_num):
                breaker.append(False)
            breaker_True = True
            for k8 in range(0, core_num):
                for k5 in range(0, len(module_list_original)):
                    if module_list[k8] == module_list_original[k5] and (
                            timer_dict[module_list_original[k5]] > module_dict[module_list_original[k5]]["c_time"]):
                        breaker[k8] = True
            for k9 in range(0, core_num):
                breaker_True = breaker_True and breaker[k9]
            if breaker_True == True:
                break

            s2 += 1
        # 제대로 작동함.

        print("list_after : ", module_list)

        proc_0 = multiprocessing.Process(target=module_dict[module_list[0]]["function"])
        proc_1 = multiprocessing.Process(target=module_dict[module_list[1]]["function"])
        proc_2 = multiprocessing.Process(target=module_dict[module_list[2]]["function"])
        proc_3 = multiprocessing.Process(target=module_dict[module_list[3]]["function"])
        proc_0.start()
        proc_1.start()
        proc_2.start()
        proc_3.start()
        proc_0.join()
        proc_1.join()
        proc_2.join()
        proc_3.join()

        for k6 in range(0, core_num):
            for k7 in range(0, len(module_list_original)):
                if module_list[k6] == module_list_original[k7] and s0 == 1:
                    module_dict[module_list_original[k7]]["start_time"] = time.time()
        # 제대로 작동함

        if s0 == 0 and module_list[0] == "Cosmonaut_dmitory":
            s0 = 1
        #제대로 작동함, 계속 바꿔줘야함.

        for _ in range(0, core_num):
            temp = module_list[0]
            del module_list[0]
            module_list.append(temp)







