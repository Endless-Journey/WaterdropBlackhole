import multiprocessing

from Cosmonaut import Cosmonaut_ruliweb

if __name__ == '__main__':
    proc_0 = multiprocessing.Process(target=Cosmonaut_ruliweb.infinite_loop())

    proc_0.start()
    proc_0.join()