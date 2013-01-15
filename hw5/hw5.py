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

def distance(pos1, pos2):
    return np.sqrt(np.sum(np.square(pos1 - pos2)))

# Calculate pairwise distances via outer-product np
# broadcasting trick
def pairwisedist(locations):
    c = np.transpose(locations[:, :, np.newaxis], (2,1,0))
    c = locations[:, :, np.newaxis] - c
    c = np.add.reduce(np.square(c), 1)
    return np.sqrt(c)    

def tsp(infile='tsp.txt'):
    with open(infile, 'r') as f:
        nvert = [int(x) for x in f.readline().split()]
        locations = np.zeros((nvert, 2), dtype='float32')

        # Rows: set membership (non-empty) described using binary encoding
        # Columns: Last vertex in tour
        bestval = np.zeros((2**nvert, nvert), dtype='float32')

        # Base case: Last vertex in tour is vertex 0. 0 if set
        # consists only of first vertex. Infinity otherwise (Can't
        # have starting vertex as last vertex in tour unless it is the only
        # vertex in the tour).
        bestval[1:,0] = np.finfo(np.float32).max
        bestval[0,0] = 1.0
        for i, line in enumerate(f):
            locations[i,] = [float(x) for x in line.split()]

    dist = pairwisedist(locations)


        