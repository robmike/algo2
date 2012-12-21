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
    with open('clustering_small.txt', 'r') as f:
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
            if not partitions.sameset(u,v):
                partitions.merge(u,v)
        if h:
            separation, u, v = heapq.heappop(h)
        else:
            separation = ecost
        return partitions, separation

print "foo"
p = cluster(2)
print p[1]