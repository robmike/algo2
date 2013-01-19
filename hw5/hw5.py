import numpy as np
import scipy
import scipy.misc
import progressbar as pb

BIGFLOAT32 = np.finfo(np.float32).max

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

# def elements(n):
#    return [0] + elements_sub(n)

def elements(n):
   t = []
   if n == 0:
      return []
   elif n&1:
      t = [1]
   return t + [x+1 for x in elements(n>>1)]

def subsetlist(setsize, subsetsize):
   n = setsize
   d = subsetsize
   if n < d:
      return []
   if n == d:
      return [2**n-1]
   if(d == 1):
      return [(1 << i) for i in xrange(n)]
   out = []
   for i in xrange(0, n - d + 1):
      out.extend([(x << (i+1)) ^ (1 << i) for x in subsetlist(n-i-1, d-1)])
   return out

# Create lookup table to convert between set index and binary
# encoded representation as a subset of all elements
def subsettable(setsize, subsetsize):
   n = setsize
   d = subsetsize
   out = {}
   for i,v in enumerate(subsetlist(setsize, subsetsize)):
      out[v] = i
   return out

def tsp(infile='tsp.txt'):
    with open(infile, 'r') as f:
      nvert = int(f.readline())
      locations = np.zeros((nvert, 2), dtype='float32')
      
      for i, line in enumerate(f):
         locations[i,] = [float(x) for x in line.split()]

    dist = pairwisedist(locations)

    # Subsets always include vertex 0
    maxsubset = scipy.misc.comb(nvert-1, (nvert-1)/2, exact=1)
    # Rows: m-elements sets containing zeroth vertex described using binary encoding
    # Columns: Last vertex in tour
    bestval = np.zeros((maxsubset+1, nvert), dtype='float32')

    # Base case: Last vertex in tour is vertex 0. Cost = 0 if set
    # consists only of first vertex. Infinity otherwise (Can't have
    # starting vertex as last vertex in tour unless it is the only
    # vertex in the tour).
    bestval[0,0] = 0.0
    bestval[1:,0] = BIGFLOAT32
    prev_bestval = bestval.copy()
    m_subsettable = {0 : 0}       # Set containing only 0th element has index 0

    widgets = [pb.Percentage(), ' ', pb.Bar(), ' ', pb.ETA()]
    pbar = pb.ProgressBar(widgets=widgets, maxval=2**nvert-1).start()
    progress_count = 0
    import pdb
    #pdb.set_trace()
    for m in xrange(2,nvert+1):
       # print "m=%i" % m
       prev_subsettable = m_subsettable
       m_subsettable = subsettable(nvert-1, m-1)
       #print("Considering subsets of size %i" % m)
       for subset, sidx in sorted(m_subsettable.iteritems()):
          subset_elems = elements(subset)
          # print("Considering tours within the set")
          # print([0] + subset_elems)
          for j in subset_elems:
             # if m == 3 and j==3:
             #    pdb.set_trace()
             prev_binencoding = subset^(1<<(j-1))
             # print("Looking at previous tours that passed through")
             # print([0] + elements(prev_binencoding))
             colidx = [0] + [x for x in subset_elems if x != j]
             rowidx = prev_subsettable[prev_binencoding] # index into m-1 element table for subset excluding j
             # minimize along exit points in set
             bv = np.min(prev_bestval[rowidx, colidx] + dist[j, colidx])
             bestval[sidx, j] = bv
             # print("Shortest tour that ends at %i and passes through" % j)
             # print([0] + elements(prev_binencoding))
             # print("Has value %.2f" % bv)
             # print(subset_elems)

          progress_count += 1
          pbar.update(progress_count)

       # when m > 2, row 0 no longer corresponds to the set consisting
       # only of the zero vertex. In all those cases we are not
       # allowed to have the 0 vertex as the "last" vertex.
       bestval[0,0] = BIGFLOAT32 

       # Swap arrays so that we can reuse memory without reallocating
       temp = prev_bestval
       prev_bestval = bestval
       bestval = temp
       # print prev_bestval
    pbar.finish()
    return np.min(prev_bestval[0, 1:] + dist[1,1:]) # exclude starting vertex

if __name__ == '__main__':
   import sys
   f = 'small.txt'
   if len(sys.argv) > 1:
      f = sys.argv[1]
   print tsp(f)
