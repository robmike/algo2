import numpy as np
import scipy

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

def distance(pos1, pos2):
    return np.sqrt(np.sum(np.square(pos1 - pos2)))

# Calculate pairwise distances via outer-product np
# broadcasting trick
def pairwisedist(locations):
    c = np.transpose(locations[:, :, np.newaxis], (2,1,0))
    c = locations[:, :, np.newaxis] - c
    c = np.add.reduce(np.square(c), 1)
    return np.sqrt(c)

def bin(s):
   return str(s) if s<=1 else bin(s>>1) + str(s&1)


def subsettable(setsize, subsetsize):
   n = setsize
   d = subsetsize
   if(d == 1):
      return [(1 << i) for i in xrange(n)]
   out = []
   for i in xrange(0, n - d + 1):
      out.extend([(x << (i+1)) ^ (1 << i) for x in subsettable(n-i-1, d-1)])
   return out

def tsp(infile='tsp.txt'):
    with open(infile, 'r') as f:
      nvert = [int(x) for x in f.readline().split()]
      locations = np.zeros((nvert, 2), dtype='float32')
      
      for i, line in enumerate(f):
         locations[i,] = [float(x) for x in line.split()]

    dist = pairwisedist(locations)
    
    for m in xrange(2,m):
       # Rows: m-elements sets containing zeroth vertex described using binary encoding
       # Columns: Last vertex in tour
       nsets = scipy.misc.comb(nvert, m-1, exact=1)
       bestval = np.zeros((2**nsets, m), dtype='float32')

       # Base case: Last vertex in tour is vertex 0. 0 if set
       # consists only of first vertex. Infinity otherwise (Can't
       # have starting vertex as last vertex in tour unless it is the only
       # vertex in the tour).
       bestval[1:,0] = np.finfo(np.float32).max
       bestval[0,0] = 1.0
       
       # Create lookup table to convert between set index and binary
       # encoded representation as a subset of all elements
       

        