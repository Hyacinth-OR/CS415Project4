import sys
import time
import heapq
import math



def hash_helper(i,j):
    n = 5
    W = 5
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
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = val  
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.cur  = None
        self.size = 0

    def add_node(self, i, j, val):
        self.size+=1
        new_node = LLNode(i,j,val)
        #new_node.i = i
        #new_node.j = j
        #new_node.val = val
        if self.size == 1:
            self.head = new_node
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

def main():
	H = HashTable(13)
	for i in range(5):
		for j in range(5):
			H.Insert(i,j,i*j)
	
	H.Update(3,4,7)
	H.Update(2,2,2)
	H.Update(5,4,99)
	#H.DumpTable()
	temp = H.Search(4,3)
	print(temp.val)

	temp1 = H.Search(2,1)
	print(temp1.val)

	temp2 = H.Search(6,6)
	if temp2 == None:
		print("0")




main()





		