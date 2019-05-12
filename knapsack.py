"""CS415 Project 4 - Created By Colin Dutra and Jeff Olson Spring 2019"""
"""
#M[i][j] = M[i - 1][j]
#H.Insert(i-1,j,v[i])
#M[i][j] = max(M[i - 1][j], v[i] + M[i - 1][j - w[i]])
"""

#!/usr/bin/env python3

import sys
import time as t
import heapq
import math
#import matplotlib.pyplot as plt;
DEVELOPMENT_MODE = True
GRAPH_MODE = False
w = [0]
v = [0]
F = [0]
M = [0]



def hash_helper(i,j):
    n = len(v)
    W = len(w)
    bn = math.ceil(math.log(n+1, 2))
    bw = math.ceil(math.log(W+1, 2))
    

    #takes 0b of front of bin()
    bn_str = bin(i)[2:]
    bw_str = bin(j)[2:]
    

    bn_str1 = str(bn_str.zfill(bn))
    bw_str1 = str(bw_str.zfill(bw))
    
    
    r = "0b1" + bn_str1 + bw_str1
    
    #print("r: ", r)
    return int(r, 2)


# data is value of F(i,j)
# data is value of F(i,j)
class LLNode:
    def __init__(self):
        self.i = None
        self.j = None
        self.val = None  
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.cur  = None
        self.size = 0

    def add_node(self, i, j, val):
        self.size+=1
        new_node = LLNode()
        new_node.i = i
        new_node.j = j
        new_node.val = val
        if self.size == 1:
            self.head = new_node
            self.cur = new_node
            new_node.next = None
        else:
            new_node.next = self.cur
            self.cur = new_node


    def get_node(self, i, j):        
        node = self.cur
        while (node != None):
            if (i == node.i and j == node.j):                
                return node
            else:
                node = node.next
        return None

    def printList(self):
        node = self.head
        while(node != None):
            print("i: ", node.i, "j: ", node.j, "val: ", node.val)
            node = node.next


class HashEntry:
    def __init__(self, i, j, val, key):
        self.ll = LinkedList()
        self.ll.add_node(i,j,val)
        self.key = key
        self.val = val
        

    def getKey():
        return self.key

    def Handle_Collision(self,i,j,val):
        link = self.ll
        #link.printList()
        link.add_node(i,j,val)

    def getNode(self,i,j):
        link = self.ll
        ret_node = link.get_node(i,j)
        return ret_node

    def printEntry(self):
        print()
        print("--- ENTRY ---")
        print("key: ", self.key)
        print("val: ", self.val)
        self.ll.printList()
        print()


class HashTable:

    def __init__(self, k):
        self.size = k;
        self.table = []
        for i in range(k):
            self.table.append(None)



    def HashFunc(self, i, j):
        return hash_helper(i,j) % self.size

    def Insert(self, i, j, val):
        key = self.HashFunc(i,j)
        entry = HashEntry(i,j,val,key)
        #entry.printEntry()
        
        if (self.table[key] == None):
            self.table[key] = entry
        else:
            temp = self.table[key]
            temp.Handle_Collision(i,j,val)

    def Search(self, i, j):
        #found = False
        key = self.HashFunc(i,j)
        #print("search key", key)
        cur = self.table[key]
        if (cur != None):
            return cur.getNode(i,j)
        else:
            return None

    def Update(self, i,j, val):
        key = self.HashFunc(i,j)
        CurEntry = self.table[key]
        if CurEntry != None:
            node = CurEntry.getNode(i,j)
            #node.val = val
        else:
            self.Insert(i,j,val)

    def DumpTable(self):
        for i in range(self.size):
            temp = self.table[i]
            temp.printEntry()


def traditional(v, w, capacity, mode = 0):
    rows = len(v)
    cols = capacity

    v = [0] + v[:]
    w = [0] + w[:]

    d = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(1, rows):
        for j in range(1, cols):
            if j - w[i] < 0:
                d[i][j] = d[i - 1][j]

            else:
                d[i][j] = max(d[i - 1][j], v[i] + d[i - 1][j - w[i]])

    subset = []
    i = rows - 1
    j = cols - 1
    '''
    for i in range(1, rows):
        line = "[ "
        for j in range(1,cols):
            line += str(d[i][j]) + " "
        line += " ]"
        print(line)
    '''

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


def space_efficient(v,w,capacity):
    global M
    
    rows = len(v)
    cols = capacity


    # adding dummy values as later on we consider these values as indexed from 1 for convinence
    v = [0] + v[:]
    w = [0] + w[:]

    M = [[0 for i in range(cols)] for j in range(rows)]

    # row : values , #col : weights
    # what Ian and thought was a solid size for k also could be a 1/4 of capacity
    #sizek = math.ceil(math.sqrt((len(v)*len(w))/2))
    sizek = math.ceil((len(v)*len(w))/2)
    H = HashTable(int(sizek))
    #print("size: ", sizek)


        
    for i in range(1, rows):
        # weights
        for j in range(1, cols):
            #d[i][j] = hashsack(i,j,v[i], H)
            if j - w[i] < 0:
                M[i][j] = hashsack(i-1, j, H)
                #print("val: ", d[i][j] )
                
            else:
                M[i][j] = max(hashsack(i-1,j, H), v[i]+hashsack(i-1, j - w[i], H))
                #print("val: ", d[i][j] )
            

                

                
    subset = []
    i = rows - 1
    j = cols - 1

    #H.DumpTable()
    '''
    for i in range(1, rows):
        line = "[ "
        for j in range(1,cols):
            line += str(M[i][j]) + " "
        line += " ]"
        print(line)
        '''
    #get subset
    while i > 0 and j > 0:
        if M[i][j] != M[i - 1][j]:
            subset.append(i)

            j = j - w[i]
            i = i - 1

        else:
            i = i - 1
    

    max_val = 0
    for i in M[rows - 1]:
        if i == None:
            i = 0
        if i > max_val:
            max_val = i

    return max_val, sorted(subset)



def hashsack(i,j, HTable): # i = number if items, j = capacity
    global M
    if i == 0 or j == 0:
        return 0
    
    if M[i][j] == 0: # if it doesnt exist in the table      
        if j < w[i]:
            temp = HTable.Search(i-1,j)
            if temp != None:
                value = temp.val
            else:
                value = hashsack(i-1,j,HTable)
        else:
            temp1 = HTable.Search(i-1,j)
            temp2 = HTable.Search(i-1,j - w[i])
            if (temp1 != None and temp2 != None):
                value = max(temp1.val, temp2.val)
            elif(temp1 == None or temp2 == None):
                value = max(hashsack(i-1,j,HTable), v[i] + hashsack(i-1,j-w[i],HTable))

        
        HTable.Insert(i,j,value)
    return M[i][j]
    
    




def getsize(array):
    size = 0
    for elem in array:
        size+= len(elem)

    return size

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
    #g = sorted(g)
    #g.reverse()
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



def readout(name,value,subset,rtime):
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
    print(name,"Time Taken:",str(rtime / (10**5)) + "ms")

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
        start = t.perf_counter()
        b1value, b1subset = greedy(v, w, cap)
        b1runtime = t.perf_counter() - start
        b1runtimes.append(b1runtime)



        #task 2b
        start = t.perf_counter()
        b2value, b2subset = greedheap(v, w, cap)
        b2runtime = t.perf_counter() - start
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
        start = t.perf_counter()

        d = traditional(v, w, cap, 1)
        mem = getsize(d)
        runtime = t.perf_counter() - start
        a1runtimes.append(runtime/100000)
        a1mems.append(mem)
        ###############
        # for task 1b #
        ###############
        # start = t.perf_counter_ns()
        # value, subset = hashsack(v, w, cap)
        # runtime = t.perf_counter_ns() - start
        # a2runtimes.append(runtime)



    a1runtimes,a1mems = sorted(a1runtimes), sorted(a1mems)
    print(a1runtimes,a1mems)
    plt.plot(a1mems, a1runtimes, 'r-', label=a1name)
    #plt.plot(a2mems, a2runtimes, 'g-', label=a2name)

    plt.legend()
    plt.show()



def main():
    cap = "p01_c.txt"
    wt = "p01_w.txt"
    val = "p01_v.txt"
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

        start = t.perf_counter()
        value,subset = traditional(v,w,cap)
        runtime = t.perf_counter() - start
        readout(name,value,subset,runtime)


        name2 = "Space-efficient Dynamic Programming"
        start = t.perf_counter()
        value,subset = space_efficient(v,w,cap)
        runtime = t.perf_counter() - start
        readout(name2, value, subset, runtime)


        b1name = "Greedy Approach"

        start = t.perf_counter()
        b1value,b1subset = greedy(v, w, cap)
        b1runtime = t.perf_counter() - start
        readout(b1name, b1value, b1subset, b1runtime)




        b2name = "Heap-based Greedy Approach"
        start = t.perf_counter()
        b2value, b2subset = greedheap(v, w, cap)
        b2runtime = t.perf_counter() - start
        readout(b2name, b2value, b2subset, b2runtime)







main()