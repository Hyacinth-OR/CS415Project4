"""CS415 Project 4 - Created By Colin Dutra and Jeff Olson Spring 2019"""
import sys
import time
import heapq
import matplotlib.pyplot as plt
DEVELOPMENT_MODE = True
GRAPH_MODE = True
w = [0]
v = [0]
F = [0]


def traditional(v, w, capacity, mode = 0):
    rows = len(v) + 1
    cols = capacity + 1

    # adding dummy values as later on we consider these values as indexed from 1 for convinence
    v = [0] + v[:]
    w = [0] + w[:]

    # row : values , #col : weights
    d = [[0 for i in range(cols)] for j in range(rows)]

    # 0th row and 0th column have value 0

    # values
    for i in range(1, rows):
        # weights
        for j in range(1, cols):
            # if this weight exceeds max_weight at that point
            if j - w[i] < 0:
                d[i][j] = d[i - 1][j]

            # max of -> last ele taken | this ele taken + max of previous values possible
            else:
                d[i][j] = max(d[i - 1][j], v[i] + d[i - 1][j - w[i]])

    subset = []
    i = rows - 1
    j = cols - 1

    # Get the items to be picked
    while i > 0 and j > 0:
        if d[i][j] != d[i - 1][j]:
            subset.append(i)

            j = j - w[i]
            i = i - 1

        else:
            i = i - 1
    if mode == 1:
        return d
    else:
        return d[rows - 1][cols - 1], sorted(subset)


def hashsack(i,j): # i = number if items, j = capacity
    global F
    if F[i][j] < 0:
        if j < w[i]:
            value = hashsack(i-1,j)
        else:
            value = max(hashsack(i-1,j), v[i] + hashsack(i-1, j - w[i]))
        F[i][j] = value
    return F[i][j]


def filerr():
    print("##############################################")
    print("## File not found! Running for p01 fileset! ##")
    print("##############################################")
    print()


def greedy(v, w, capacity):
    g = []
    for i in range(len(v)):
        g.append([v[i]/w[i],v[i],w[i],i])
    g = sorted(g)
    g.reverse()
    burden = 0
    subset = []
    value = 0
    for i in range(len(g)):
        if (burden + g[i][2]) > capacity:
            break
        else:
            burden += g[i][2]
            value += g[i][1]
            subset.append(g[i][3] + 1)

    return value,sorted(subset)

def greedheap(v,w,capacity):
    g = []
    for i in range(len(v)):
        g.append([v[i] / w[i], v[i], w[i], i])
    g = sorted(g)
    g.reverse()
    heapq._heapify_max(g)

    burden = 0
    subset = []
    value = 0
    for i in range(len(g)):
        curr = heapq._heappop_max(g)
        if (burden + curr[2]) > capacity:
            break
        else:
            burden += curr[2]
            value += curr[1]
            subset.append(curr[3] + 1)

    return value, sorted(subset)


def processFiles(capacity,weights,values):
    w =[]
    v = []

    with open(capacity) as c:
        line = c.readline()
        line = line.strip()
        cap = int(line)
    with open(weights) as wt:
        for line in wt:
            line = line.strip()
            w.append(int(line))
    with open(values) as vals:
        for line in vals:
            line = line.strip()
            v.append(int(line))

    info = []
    for i in range(len(w)):
        pack = [w[i],v[i]]
        info.append(pack)




    return cap,v,w

def generateGlobalArray(cols,rows):
    global F
    F = [[-1 for i in range(cols)] for j in range(rows)]

    for i in range(cols):
        F[0][i] = 0
    for i in range(rows):
        F[i][0] = 0



def readout(name,value,subset,time):
    stringset = "{"
    for elem in str(subset):
        if elem == "[" or elem == "]":
            continue

        else:
            stringset += str(elem)
    stringset += "}"
    print()
    print(name,"Optimal value:",value)
    print(name,"Optimal subset:",stringset)
    print(name,"Time Taken:",str(time / (10**5)) + "ms")

def GRAPHTASK2(files):
    b1name = "Greedy Approach"
    b2name = "Heap-based Greedy Approach"
    plt.xlabel('# of items')
    plt.ylabel('time(ns)')
    plt.title('Greedy Approaches')
    b1runtimes = []
    b2runtimes = []
    lens = []
    file = -1
    for elem in files: # Have to get all the points from the files.
        file+=1
        cap = elem[0]
        wt = elem[1]
        val = elem[2]



        cap, v, w = processFiles(cap, wt, val)
        lens.append(len(v))


        #task 2a
        start = time.perf_counter_ns()
        b1value, b1subset = greedy(v, w, cap)
        b1runtime = time.perf_counter_ns() - start
        b1runtimes.append(b1runtime)



        #task 2b
        start = time.perf_counter_ns()
        b2value, b2subset = greedheap(v, w, cap)
        b2runtime = time.perf_counter_ns() - start
        b2runtimes.append(b2runtime)


    lens = sorted(lens)
    b1runtimes,b2runtimes = sorted(b1runtimes),sorted(b2runtimes)
    plt.plot(lens, b1runtimes, 'r-', label=b1name)
    plt.plot(lens, b2runtimes, 'g-', label=b2name)
    plt.legend()
    plt.show()

def GRAPHTASK1(files):

    a1name = "Traditional Approach"
    a2name = "Memory Efficient Approach"
    plt.xlabel('space')
    plt.ylabel('time(ns)')
    plt.title('Dynamic Approaches')
    a1runtimes = []
    a2runtimes = []
    file = -1
    a1mems = []
    a2mems = []

    for elem in files[:-1]: # We are plotting two lines for each file.
        file+=1
        cap = elem[0]
        wt = elem[1]
        val = elem[2]

        cap, v, w = processFiles(cap, wt, val)

        # for task 1a
        start = time.perf_counter_ns()

        d = traditional(v, w, cap, 1)
        mem = sys.getsizeof(d)
        runtime = time.perf_counter_ns() - start
        a1runtimes.append(runtime)
        a1mems.append(mem)
        ###############
        # for task 1b #
        ###############
        # start = time.perf_counter_ns()
        # value, subset = hashsack(v, w, cap)
        # runtime = time.perf_counter_ns() - start
        # a2runtimes.append(runtime)



    a1runtimes,a1mems = sorted(a1runtimes), sorted(a1mems)
    print(a1runtimes,a1mems)
    plt.plot(a1mems, a1runtimes, 'r-', label=a1name)
    #plt.plot(a2mems, a2runtimes, 'g-', label=a2name)

    plt.legend()
    plt.show()



def main():
    cap = "p00_c.txt"
    wt = "p00_w.txt"
    val = "p00_v.txt"
    files =\
    [["p00_c.txt","p00_w.txt","p00_v.txt"], ["p01_c.txt","p01_w.txt","p01_v.txt"],
     ["p02_c.txt", "p02_w.txt", "p02_v.txt"], ["p03_c.txt","p03_w.txt","p03_v.txt"],
     ["p04_c.txt", "p04_w.txt", "p04_v.txt"],["p05_c.txt","p05_w.txt","p05_v.txt"],
     ["p06_c.txt", "p06_w.txt", "p06_v.txt"], ["p07_c.txt","p07_w.txt","p07_v.txt"],
     ["p08_c.txt", "p08_w.txt", "p08_v.txt"]]

    if GRAPH_MODE:
        GRAPHTASK1(files)
        GRAPHTASK2(files)

    else:

        if not DEVELOPMENT_MODE:
            cap = input("Enter file containing the capacity: ")
            wt = input("Enter file containing the weights: ")
            val = input("Enter file containing the values: ")

        try:
            global v, w
            cap, v, w = processFiles(cap, wt, val)

        except FileNotFoundError:
            filerr()
            cap, wt, val = "p01_c.txt", "p01_w.txt", "p01_v.txt"
            cap, v, w = processFiles(cap, wt, val)


        print("Knapsack Capacity =", str(cap) + '.',"Total number of items =",len(w))

        name = "Traditional Dynamic Programming"

        start = time.perf_counter_ns()
        value,subset = traditional(v,w,cap)
        runtime = time.perf_counter_ns() - start
        readout(name,value,subset,runtime)


        name = "Space-efficient Dynamic Programming"


        b1name = "Greedy Approach"

        start = time.perf_counter_ns()
        b1value,b1subset = greedy(v, w, cap)
        b1runtime = time.perf_counter_ns() - start
        readout(b1name, b1value, b1subset, b1runtime)




        b2name = "Heap-based Greedy Approach"
        start = time.perf_counter_ns()
        b2value, b2subset = greedheap(v, w, cap)
        b2runtime = time.perf_counter_ns() - start
        readout(b2name, b2value, b2subset, b2runtime)







main()