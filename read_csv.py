import time
import csv
from memory_profiler import profile
import pandas as pd


def proc():
    start_time = time.time()
    d = []
    count = 0
    with open('./csv_file/test/annotations-human.csv') as f:
        read = csv.reader(f)

        for r in read:
            d.append(r)
            count += 1

    end_time = time.time()

    elapsed_time = end_time - start_time



    return elapsed_time, count, len(d)

# @profile
def proc2():
    start_time = time.time()
    d = []
    count = 0

    read = pd.read_csv('./csv_file/test/annotations-human.csv')
    for r in read:
        d.append(r)
        count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(type(read))
    # print(read.shape)

    return elapsed_time, count, len(d)

@profile
def proc3():
    start_time = time.time()
    d = []
    count = 0

    read = pd.read_csv('./csv_file/test/annotations-human.csv', chunksize=10000)

    for rr in read:
        # print rr.shape
        for r in range(rr.shape[0]):
            d.append(r)
            count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time, count, len(d)

if __name__ == '__main__':

    elapsed_time, count, l = proc2()

    print "time: %f" % elapsed_time
    print "count: %d" % count
    print "length: %d" % l


