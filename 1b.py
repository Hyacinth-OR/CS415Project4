import sys
import time
import heapq
import math



def hash_helper(i,j):
    n = len(v)
    W = len(w)
    bn = math.ceil(math.log(n+1, 2))
    bw = math.ceil(math.log(W+1, 2))
    #print("bnstr: ", bn)

    #takes 0b of front of bin()
    bn_str = bin(i)[2:]
    bw_str = bin(j)[2:]

    bn_str1 = str(bn_str.zfill(bn))
    bw_str1 = str(bw_str.zfill(bw))

    
    r = "0b1" + bn_str1 + bw_str1
    
    return int(r, 2)


# data is value of F(i,j)
class LLNode:
	def __init__(self, i, j, val):
		self.i = i
		self.j = j
		self.val = val	
		self.next = None


class LinkedList:
	def __init__(self)
		self.head = None
		self.cur  = None
		self.size = 0

	def add_node(self, i, j, val):
		self.size+=1
		new_node = Node()
		new_node.i = i
		new_node.j = j
		new_node.val = val
		if self.size == 1:
			self.head = new_node
			new_node.next = None
		else:
			new_node.next = self.cur
			self.cur = new_node


	def get_node(self, i, j):
		found = False
		node = self.cur
		while (!found):
			if (i == node.i && j == node.j):
				found = True
				return node
			else
				node = node.next
		return None


class HashEntry:
	def __init__(self, i, j, key, val):
		self.ll = LinkedList()
		ll.add_node(i,j)
		self.key = key
		

	def getKey():
		return self.key

	def Handle_Collision(i,j):
		link = self.ll
		link.add_node(i,j,val)

	def getNode(i,j):
		link = self.ll
		ret_node = link.get_node(i,j)
		return ret_node


class HashTable:

	def __init__(self, k):
		self.size = k;
		self.table = [None] * self.size



	def HashFunc(i, j):
		return hash_helper(i,j) % self.size

	def Insert(i, j, key):
		key = HashFunc(i,j)
		entry = HashEntry(i,j, key)
		
		if (self.table[key] == None):
			self.table[key] = entry
		else:
			temp = self.table[key]
			temp.Handle_Collision(i,j)

	def Search(i, j):
		#found = False
		key = HashFunc(i,j)
		cur = self.table[key]
		if (cur.getNode(i,j) != None):
			return cur
		else
			return None









		