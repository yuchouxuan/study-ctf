import threading


class MT(threading.Thread):
    id = 0
    work = {}
    res = []

    def __init__(self, id, work={}, res=[]):
        threading.Thread.__init__(self)
        self.id = id
        self.work = work
        self.res = res

    def run(self):
        pass


class TPool:
    works = []
    resresults = []
    lt = []

    def __init__(self, mt, cont=8, works=[], results=[], ):

        self.results = results
        self.lt = []
        if works == []:
            self.works = [{} for i in range(cont)]
        else:
            self.works = works
        for i in range(cont):
            t = mt(i, self.works[i], self.results)
            self.lt.append(t)
        pass

    def start(self):
        for i in self.lt:
            if not i.is_alive():
                i.start()

    def join(self):
        for i in self.lt:
            i.join()

    def run(self):
        self.start()
        self.join()


import multiprocessing

def CreatePorcess(func=print, arg=[('hello',)]):
    # print('xxxxxxxxxxxxxxxxxxxxx')
    mgr = multiprocessing.Manager()
    l = mgr.list()
    PorPool=[]
    for i in arg:
        print(i)
        a = multiprocessing.Process(target=func,args=i )
        PorPool.append(a)
        a.start()
    for i in PorPool:
        try:
            i.join()
        except:
            pass




if __name__ == "__main__":
    pass
