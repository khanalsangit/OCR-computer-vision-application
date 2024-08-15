from multiprocessing import Process


def fun(name):
    print(f'hello {name}')

def main1():
    procs = []
    proc = Process(target=fun)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    proc = Process(target=fun, args=('Peter',))
    procs.append(proc)
    
    proc.start()

    for proc in procs:
        proc.join()


if __name__ == '__main__':
    main1()


##procs = []
##        proc = Process(target = recog1)
##        procs.append(proc)
##        proc.start()
##        for list_crop in img_crop_list:
##            proc = Process(target = recog1, args=(list_crop,))
##            procs.append(proc)
##            proc.start()
