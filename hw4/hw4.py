from collections import defaultdict
import progressbar as pb
from math import isinf

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

# Computes floyd-warshall all-pairs and then returns shortest
def floydwarsh(infile='g1.txt'):
    bestval = defaultdict(lambda: None)
    with open(infile, 'r') as f:
        nvert, nedges = [int(x) for x in f.readline().split()]
        for i in xrange(nvert):
            bestval[(i, i)] = 0
        for line in f:
            u, v, cost = [int(x) for x in line.split()]
            u, v = u - 1, v - 1 # Convert 1-indexed to 0-indexed
            bestval[(u, v)] = cost

    
    widgets = [pb.Percentage(), ' ', pb.Bar(), ' ', pb.ETA()]
    pbar = pb.ProgressBar(widgets=widgets, maxval=nvert**2).start()
    import pdb
    for k in xrange(nvert):
       for i in xrange(nvert):
          for j in xrange(nvert):
               # print i,j,k
               # print "bestval[(i,k)]: " + repr(bestval[(i,k)])
               # print "bestval[(k,j)]: " + repr(bestval[(k,j)])
               if None not in [bestval[(i,k)], bestval[(k,j)]]:
                  candidate = bestval[(i,k)] + bestval[(k,j)]
                  if bestval[(i,j)] == None:
                     bestval[(i,j)] = candidate
                  else:
                     bestval[(i,j)] = min(bestval[(i,j)], candidate)
          pbar.update(k*nvert + i)

    pbar.finish()
    # Check for negative cycle
    for i in xrange(nvert):
        if bestval[(i,i)] < 0:
            return False
    
    shortest = min([cost for (u,v), cost in bestval.iteritems() if cost != None and u != v])
    return shortest

if __name__ == '__main__':
   fname = sys.argv[1]
   result = floydwarsh(fname)
   print fname + ': ' + repr(result)

