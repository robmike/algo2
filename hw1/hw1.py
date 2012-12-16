import heapq

def schedulejobs(metricfun):
    h = []
    with open("jobs.txt", 'r') as f:
        njobs = int(f.readline())
        for jobnum in xrange(0, njobs):
            w, l = [int(x) for x in f.readline().split()]
            # Use of negative will make this a max heap.  Note that in
            # python tuples are compared element by element
            heapq.heappush(h, (-metricfun(w,l), w, l))
    wsum = 0
    totaltime = 0
    while(h):
        metric, w, l = heapq.heappop(h)
        totaltime += l
        # print totaltime
        # print("%i, %i" % (w, totaltime))
        wsum += w*totaltime
    return wsum

def prim():
    edges = {}
    todoverts = set([])
    with open('edges.txt', 'r') as f:
        nvert, nedge = [int(x) for x in f.readline().split()]
        for i in xrange(0, nedge):
            v1, v2, edge_cost = [int(x) for x in f.readline().split()]
            if v1 == v2:
                continue
            if v1 > v2:
                v2, v1 = v1, v2
            if edges.has_key((v1,v2)):
                edge_cost = min(edges[(v1,v2)], edge_cost)
            edges[(v1, v2)] = edge_cost
            todoverts = todoverts | set((v1,v2))
    seenverts = set([todoverts.pop()])
    treecost = 0
    tree = {}
    while len(todoverts) > 0:
        minecost = float('inf')
        bestedge = None
        for (v1,v2), ecost in edges.iteritems():
            if (v1 in seenverts and v2 in todoverts) or (v2 in seenverts and v1 in todoverts):
                if ecost < minecost:
                    minecost = ecost
                    bestedge = (v1,v2)
        treecost += minecost
        if not bestedge:
            import pdb
            pdb.set_trace()
        tree[bestedge] = edges[bestedge]
        del edges[bestedge]
        v1, v2 = bestedge
        seenverts.add(v1)
        seenverts.add(v2)
        todoverts.discard(v1)
        todoverts.discard(v2)
    return tree, treecost


# q1
print "q1"
print schedulejobs(lambda w, l: w - l)

# q2
print "q2"
print schedulejobs(lambda w, l: w/l)

# q3
print "q3"
print prim()[1]
