
import ast

Rtree = ''
queries = ''
out = ''
tree = []

def intersect(w, mbr):
    if(w[0] >= mbr[1] or w[1] <= mbr[0]):   #side by side
        return False
    if(w[2] >= mbr[3] or w[3] <= mbr[2]):   #one above the other
        return False
    return True
    
def evaluate(window):
    return search(window, tree[-1][1],[])   #from the root and downwards

def search(window, node, ids):
    if tree[node][0]:  #not a leaf
        for item in tree[node][2]:
            if intersect(window, item[1]):
                search(window , item[0] , ids)
    else:              #leaf
        for item in tree[node][2]:
            if intersect(window, item[1]):
                ids.append(str(item[0]))
    return ids
      
try:
    Rtree = open('file.txt', 'r')
    queries = open('Rqueries.txt', 'r')
    out = open('rout.txt' , 'w')
except:
    exit(1)

node = Rtree.readline().rstrip("\n")
while node:
    tree.append(ast.literal_eval(node))
    node = Rtree.readline().rstrip("\n")

query = queries.readline().rstrip("\n").split(' ')
line = 0
while query[0]:
    window = [float(query[0]), float(query[2]), float(query[1]), float(query[3])]
    ids = evaluate(window)
    print('%s (%s): %s ' % (line, len(ids), ', '.join(ids)))
    out.write('%s (%s): %s ' % (line, len(ids), ', '.join(ids)) + '\n')
    line += 1
    query = queries.readline().rstrip("\n").split(' ')

Rtree.close()
queries.close()




