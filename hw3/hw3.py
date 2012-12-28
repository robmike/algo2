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

def knapsack(infile='knapsack1.txt'):
    with open(infile, 'r') as f:
        size, nitems = [int(x) for x in f.readline().split()]
        items = []
        bestval = np.zeros((nitems, size+1), dtype='int32')
        for line in f:
            value, weight = [int(x) for x in line.split()]
            items.append((value, weight))
        for i,(value,weight) in enumerate(items):
            for w in xrange(0,size + 1): # weight so-far
                lastidx = max(i-1, 0)    # handle i == 0
                if w < weight:
                    bestval[i][w] = bestval[lastidx][w]
                else:
                    bestval[i][w] = max(bestval[lastidx][w], 
                                        bestval[lastidx][w - weight] + value)
    return bestval[nitems-1][size]

#q1
print knapsack()