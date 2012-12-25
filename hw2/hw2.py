import heapq
import numpy as np
from numpy import ndfromtxt, recfromtxt

import pdb, sys
# debug shit (from stackexchange)
def info(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # we are in interactive mode or we don't have a tty-like
      # device, so we call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # we are NOT in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

sys.excepthook = info

class DisjointSet(object):
    def __init__(self):
        self.partitions = {}
    def count(self):
        return len(self.partitions.keys())
    def makeset(self, x):
        self.partitions[x] = [x]
    def find(self, x):
        for rep, elems in self.partitions.iteritems():
            if x in elems:
                return rep
        return None
    def sameset(self, x, y):
        return self.find(x) == self.find(y)
    def merge(self, p, q):
        p = self.find(p)
        q = self.find(q)
        rep = p
        if len(self.partitions[p]) < len(self.partitions[q]):
            rep = q
        a, b = self.partitions[p], self.partitions[q]
        del(self.partitions[p])
        del(self.partitions[q])
        self.partitions[rep] = a + b

def cluster(nclusters = 4):
    h = []
    partitions = DisjointSet()
    with open('clustering1.txt', 'r') as f:
        nvert = int(f.readline())
        # edges = recfromtxt(f, dtype=int, usemask=False)
        for line in f:
            u, v, ecost = [int(x) for x in line.split()]
            heapq.heappush(h, (ecost, u, v))
            partitions.makeset(u)
            partitions.makeset(v)

        while(h and partitions.count() > nclusters):
            elem = heapq.heappop(h)
            ecost, u, v = elem
            # print elem
            if not partitions.sameset(u,v):
                partitions.merge(u,v)
                #print "different sets, merging"
        # FIXME: Handle 1 cluster
        # FIXME: Can h ever be empty for more than 1 cluster?
        if h:
           while(h):
              separation, u, v = heapq.heappop(h)
              if not partitions.sameset(u,v):
                 print separation, u, v
                 break
        else:
            separation = ecost
            print "error"
        return partitions, separation


# q2
def bin(s):
   return str(s) if s<=1 else bin(s>>1) + str(s&1)

class Counter(object):
   def __init__(self, d, nbits):
      self.d = d
      self.nbits = nbits

def nextPairWithDist(nodes, d, nbits):
   # next pair with distance d
   if(len(nodes) == 1):
      raise(StopIteration)
   for n in nodes:
      for i in xrange(0, nbits - d + 1):
         # solution only handles d = 2
         # can handle arbitrary d with
         # base-nbits d digit adder
         if d == 2:
            for j in xrange(i+1, nbits):
               candidate = n ^ (1 << i) ^ (1 << j)
               # print i,j, bin(candidate)
               if candidate in nodes and candidate > n:
                  yield d, n, candidate
         else:
            candidate = n ^ (1 << i)
            # print bin(candidate)
            if candidate in nodes and candidate > n:
               yield d, n, candidate
   raise(StopIteration)

   

def hammingcluster():
    h = []
    partitions = DisjointSet()
    maxdistance = 2
    nodes = set([])
    with open('clustering2.txt', 'r') as f:
        nvert_donotuse, nbits = [int(x) for x in f.readline().split()]
        # edges = recfromtxt(f, dtype=int, usemask=False)
        for line in f:
            nodeint = int(''.join([str(x) for x in line.split()]), 2)
            nodes.add(nodeint)
            partitions.makeset(nodeint)

        nvert = len(nodes)

        for d in xrange(1,maxdistance+1):
           for nextpair in nextPairWithDist(nodes, d, nbits):
              ecost, u, v = nextpair
              if not partitions.sameset(u,v):
                 partitions.merge(u,v)

        return partitions.count() #, partitions.partitions

# unused function
def binsearchmincluster():
   l, r = 0, 20000
   i  = r
   while(l < r):
      print i, l, r
      i = (l + r)/2
      success = hammingcluster(i)
      if not success:
         r = i
      else:
         l = i + 1
   return i - 1     # Returns largest cluster size that meets criteria


# print "q1"
# p = cluster(4)
# # print p[0].partitions
# print p[1]

print "q2"
# p = hammingcluster(2)