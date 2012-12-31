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

    return bestval[nitems-1][size], opt_items

def knapsacklarge(infile='knapsack2.txt'):
    with open(infile, 'r') as f:
       size, nitems = [int(x) for x in f.readline().split()]
       items = []
       for line in f:
          value, weight = [int(x) for x in line.split()]
          items.append((value, weight))

       bestval = {}
       def bestval_recurse(idx, weight_left):
          if idx < 0:
             return 0
          value, weight = items[idx]
          with_item, without_item = 0, 0 # value with/without item
          try:
             without_item = bestval[(idx-1, weight_left)]
             raise(KeyError)
          except KeyError:
             without_item = bestval_recurse(idx-1, weight_left)
             bestval[(idx-1, weight_left)] = without_item
          if weight <= weight_left:
             try:
                with_item = bestval[(idx-1, weight_left - weight)]
                raise(KeyError)
             except KeyError:
                with_item = bestval_recurse(idx-1, weight_left - weight) + value
                bestval[(idx-1, weight_left)] = with_item
          # print idx, with_item, without_item, weight, value
          return max(with_item, without_item)

       return bestval_recurse(nitems-1, size) # [(nitems-1, size)]

def knapsackopt(infile='knapsack2.txt'):
    with open(infile, 'r') as f:
        size, nitems = [int(x) for x in f.readline().split()]
        items = []
        bestval = [0]*(size+1)
        for line in f:
            value, weight = [int(x) for x in line.split()]
            items.append((value, weight))
        for i,(value,weight) in enumerate(items):
            for w in xrange(size, -1, -1): # total weight so-far
                lastidx = max(i-1, 0)    # handle i == 0
                if w < weight:
                    bestval[w] = bestval[w] # nop, new value same as old
                else:
                   bestval[w] = max(bestval[w], bestval[w - weight] + value)
                # print i, w, value, weight, bestval[i][w]
    return bestval[size]


# f = 'knapsacksmall.txt'
# f = 'knapsack1.txt'
# print('q1')
# print knapsack(f)

print('q2')
print knapsackopt()