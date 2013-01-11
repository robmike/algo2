import numpy as np

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

def floydwarsh(infile='g1.txt'):
    edges = {}
    with open(infile, 'r') as f:
        nvert, nedges = [int(x) for x in f.readline().split()]
        for line in f:
            u, v, cost = [int(x) for x in line.split()]
            edges[(u, v)] = cost

    # initialize initial path costs to infinity except for paths from
    # node to itself
    bestval = np.inf*np.ones((nvert, nvert, nvert), dtype='int32')
    for i in xrange(nvert):
        bestval[i, i, 0] = 0
    for (u,v), cost in edges.iteritems():
        bestval[u, v, 0] = cost

    for i in xrange(nvert):
        for j in xrange(nvert):
            for k in xrange(nvert):
                bestval[i,j,k] = min(bestval[i,j,k-1],
                                     bestval[i,k,k-1] + bestval[k,j,k-1] + edges[(i,j)])

    # Check for negative cycle
    for i in xrange(nvert):
        if bestval[i,i,nvert-1] < 0:
            return False
    
    shortest = float('inf')
    for i in xrange(nvert):
        for j in xrange(nvert):
            shortest = min(bestval[i, j, nvert-1], shortest)
    return shortest

floydwarsh()
