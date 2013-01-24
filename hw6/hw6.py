import numpy as np
import progressbar as pb
from collections import OrderedDict

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

class Node(object):
    def __init__(self, nodeid, index=-1, lowlink=-1, successors=None):
        self.nodeid = nodeid
        self.index = index
        self.lowlink = lowlink
        self.successors = []
        if successors:
            self.successors = successors

index = 0

def is2satisfiable(infile):
    with open(infile, 'r') as f:
        # Number of vertices is always equal to number of clauses
        n = int(f.readline())
        nodehash = {}
        for i, line in enumerate(f):
            nodeid1, nodeid2 = [int(x) for x in line.split()]
            try:
                nodehash[-nodeid1]
            except KeyError:
                nodehash[-nodeid1] = {}
            nodehash[-nodeid1][nodeid2] = True
            try:                # Some variables or their negation may not have any edges
                nodehash[nodeid2]
            except KeyError:
                nodehash[nodeid2] = {}
            try:
                nodehash[-nodeid2]
            except KeyError:
                nodehash[-nodeid2] = {}
            nodehash[-nodeid2][nodeid1] = True
            try:                # Some variables or their negation may not have any edges
                nodehash[nodeid1]
            except KeyError:
                nodehash[nodeid1] = {}
        
        # Problem is not satistfiable if there is a chain (a) ->
        # (b) -> ... -> not(a) -> ... -> (a) or, in other words, a
        # variable and its negation occur in the same connected
        # component
        nodeindex = {}
        nodelink = {}
        seen = OrderedDict()

        # Strongly connected components algorithm on implication graph
        def strongconnect(node):
            global index
            nodeindex[node] = index
            nodelink[node] = index
            index +=1
            seen[node] = True

            for w in nodehash[node]:
                try:
                    windex = nodeindex[w]
                    if w in seen:
                        nodelink[node] = min(windex, nodelink[node])
                except KeyError:
                    result = strongconnect(w)
                    if result == False:
                       return False
                    nodelink[node] = min(nodelink[w], nodelink[node])

            if(nodelink[node] == nodeindex[node]): # starting node for this component
               component = {}
               v = None
               while seen and v != node: # Create connected component
                  v,unused = seen.popitem()
                  try:
                     # If -v already in connected component
                     component[-v]
                     return False
                  except KeyError:
                     component[v] = True


        for v in nodehash.keys():
            try:
                # Skip already processed nodes
                nodeindex[v]
            except KeyError:
                result = strongconnect(v)
                if result == False:
                   return False

    return True

# parallel python hw6.py -- 2sat*.txt | sort
if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
      f = sys.argv[1]
      result = is2satisfiable(f)
      print("%s: %s" % (f, result))
      with open('output-%s.txt' % f, 'w') as outf:
          outf.write(str(result))
   else:
       infiles = ['2sat%i.txt' % i for i in range(1,7)]
       bincode = 0
       for i, f in enumerate(infiles):
           result = is2satisfiable(f)
           bincode = bincode << 1
           if result:
               bincode += 1
       print(repr(bin(bincode)))