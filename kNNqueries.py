#Vasilhs  Gewrgoulas
#AM 2954

import ast
import math
import sys
import heapq

Rtree = ''
queries = ''
out = ''
tree = []
q = (0, 0)
line = 0
k_closest = 10

def dist(w):
    dx = max([w[0] - q[0], 0, q[0] - w[1]])
    dy = max([w[2] - q[1], 0, q[1] - w[3]])
    return math.sqrt(dx * dx + dy * dy)

def kNN(root):

    k = 1
    ids = []
    queue = []
    for el in tree[root][2]: #dist from mbr,  entry id, node         leaf?
        heapq.heappush(queue, (dist(el[1]), el[0], tree[root][1], tree[root][0]))

    while queue and k <= k_closest:   
        el = heapq.heappop(queue)     #whenever we pop a leaf then we have our next min
        if el[3]:
            for item in tree[el[1]][2]:
                d = dist(item[1])
                heapq.heappush(queue, (d, item[0], tree[el[1]][1], tree[el[1]][0]))
        else:
            ids.append(str(el[1]))
            k += 1                            
    return ids

try:
    Rtree = open('file.txt', 'r')
    queries = open('NNqueries.txt', 'r')
except:
    exit(1)

node = Rtree.readline().rstrip("\n")
while node:
    tree.append(ast.literal_eval(node))
    node = Rtree.readline().rstrip("\n")

query = queries.readline().rstrip("\n").split(' ')
while query[0]:
    q = (float(query[0]), float(query[1]))
    ids = kNN(tree[-1][1])
    print('%s: %s' % (line , ', '.join(ids)))
    line += 1
    query = queries.readline().rstrip("\n").split(' ')

Rtree.close()
queries.close()




