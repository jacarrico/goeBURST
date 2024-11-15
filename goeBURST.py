#!/usr/bin/env python
import os
import sys

#Class UF from 	https://www.ics.uci.edu/~eppstein/PADS/UnionFind.py
class UF:
	"""An implementation of union find data structure.
	It uses weighted quick union by rank with path compression.
	"""

	def __init__(self, N):
		"""Initialize an empty union find object with N items.
		Args:
			N: Number of items in the union find object.
		"""

		self._id = list(range(N))
		self._count = N
		self._rank = [0] * N

	def find(self, p):
		"""Find the set identifier for the item p."""

		id = self._id
		while p != id[p]:
			id[p] = id[id[p]]   # Path compression using halving.
			p = id[p]
		return p

	def count(self):
		"""Return the number of items."""

		return self._count

	def connected(self, p, q):
		"""Check if the items p and q are on the same set or not."""

		return self.find(p) == self.find(q)

	def union(self, p, q):
		"""Combine sets containing p and q into a single set."""

		id = self._id
		rank = self._rank

		i = self.find(p)
		j = self.find(q)
		if i == j:
			return

		self._count -= 1
		if rank[i] < rank[j]:
			id[i] = j
		elif rank[i] > rank[j]:
			id[j] = i
		else:
			id[j] = i
			rank[i] += 1

	def __str__(self):
		"""String representation of the union find object."""
		return " ".join([str(x) for x in self._id])

	def __repr__(self):
		"""Representation of the union find object."""
		return "UF(" + str(self) + ")"


def LoadProfiles(profiles_in):
	global profiles
	profiles=[]
	#TODO change dict to list
	ct=0
	fp = open(profiles_in,'r')
	for line in fp:
		ct+=1
		profiles.append(line.rstrip().split('\t'))
	fp.close()
	#TODO Return Unique profiles only 
	return profiles

def HammVect(v1,v2):
	ndif=sum(1 for i, j in zip(v1, v2) if i != j)
	return ndif

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
def EdgeComp(e1,e2):
	u,v=e1
	x,y=e2
	leveluv = HammVect(profiles[u],profiles[v])  
	levelxy = HammVect(profiles[x],profiles[y])

	if leveluv != levelxy:
		return leveluv - levelxy

	for k in range (maxlen):				
		maxuv = max(lvs[u][k], lvs[v][k])	
		maxxy = max(lvs[x][k], lvs[y][k])

		if maxuv != maxxy:
			return maxxy - maxuv

		minuv = min(lvs[u][k], lvs[v][k])
		minxy = min(lvs[x][k], lvs[y][k])

		if minuv != minxy:
			return minxy - minuv 

		maxuv = max(u,v) 
		maxxy = max(x,y)

	if maxuv != maxxy:
		return maxxy - maxuv

	minuv = min(u,v)
	minxy = min(x,y)

	if minuv != minxy:
		return minxy - minuv

def Kruskal():

	global edges
	edges=[] 
	nprof=len(profiles)
	for i in range(nprof):
		for j in range(i +1, nprof):
			edges.append([i,j])
	#edges.sort(cmp=EdgeComp)
	edges=sorted(edges, key=cmp_to_key(EdgeComp))

	# var uf = new UnionFind(n)
	uf = UF(nprof)

	tree = []
	i=0
	while i<len(edges) and len(tree)<nprof-1:
	 	
		if uf.find(edges[i][0]) != uf.find(edges[i][1]): 
			tree.append(edges[i])		
			uf.union(edges[i][0], edges[i][1])
		
		i+=1
	
	return tree

def CalcLVs():
	global maxlen
	global lvs
	maxlen= len(profiles[1])
	nprof=len(profiles)

	lvs=[ [0]*maxlen for i in range(nprof)]

	for i in range(nprof):
		for j in range(i+1,nprof):
			diff=HammVect(profiles[i],profiles[j])
			lvs[i][diff-1]+=1
			lvs[j][diff-1]+=1

	return lvs,maxlen


def main():
	try:
		profiles_in = sys.argv[1]
	except IndexError:
		print("blablabla")

	profiles = LoadProfiles(profiles_in)
	#print profiles
	lvs,maxlen=CalcLVs()
	tree=Kruskal()
	print(tree)

if __name__ == "__main__":
	main()
