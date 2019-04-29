"""CS415 Project 4 - Created By Colin Dutra and Jeff Olson Spring 2019"""

import time
import heapq
DEVELOPMENT_MODE = True
w = [0]
v = [0]
F = [0]

def traditional(v, w, capacity):
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


def greedy(v,w,capacity):
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

def main():
    cap = "p00_c.txt"
    wt = "p00_w.txt"
    val = "p00_v.txt"

    if DEVELOPMENT_MODE == False:
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
    generateGlobalArray(len(v) + 1, cap + 1)
    out = hashsack(1,cap-1)
    print(out)
    for elem in F:
        print(elem)



    name = "Greedy Approach"

    start = time.perf_counter_ns()
    value,subset = greedy(v, w, cap)
    runtime = time.perf_counter_ns() - start
    readout(name, value, subset, runtime)

    name = "Heap-based Greedy Approach"
    start = time.perf_counter_ns()
    value, subset = greedheap(v, w, cap)
    runtime = time.perf_counter_ns() - start
    readout(name, value, subset, runtime)





main()