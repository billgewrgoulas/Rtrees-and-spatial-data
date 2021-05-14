#Vasileios Gewrgoulas
#AM 2954

import sys
import math

_DIVISORS = [180.0 / 2 ** n for n in range(32)]

def interleave_latlng(lat, lng):
    if not isinstance(lat, float) or not isinstance(lng, float):
        print('Usage: interleave_latlng(float, float)')
        raise ValueError("Supplied arguments must be of type float!")

    if (lng > 180):
        x = (lng % 180) + 180.0
    elif (lng < -180):
        x = (-((-lng) % 180)) + 180.0
    else:
        x = lng + 180.0
    if (lat > 90):
        y = (lat % 90) + 90.0
    elif (lat < -90):
        y = (-((-lat) % 90)) + 90.0
    else:
        y = lat + 90.0

    morton_code = ""
    for dx in _DIVISORS:
        digit = 0
        if (y >= dx):
            digit |= 2
            y -= dx
        if (x >= dx):
            digit |= 1
            x -= dx
        morton_code += str(digit)

    return morton_code

###############################split rects into chunks######################

rtree = ''
level = 0  # 0 will be the leaf level
node_id = 0

def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

offset = ''
coords = ''

################################calculate MBR################################
def get_mbr(points):

    xAxis = []
    yAxis = []
    for point in points:
        xAxis.extend([float(point[1][0]),float(point[1][1])])
        yAxis.extend([float(point[1][2]),float(point[1][3])])

    return [min(xAxis) , max(xAxis) , min(yAxis) , max(yAxis)]

def get_z(x1, x2, y1, y2):
    center = ((x1+x2)/2, (y1+y2)/2)
    return interleave_latlng(center[1], center[0])

###############################construct the tree###########################

def bulk_load(rect_mbrs):
    global level, tree, node_id, rtree
    
    nodes = int(math.floor(len(rect_mbrs) / 20))
    level_chunks = chunks(rect_mbrs, 20)

    non_leaf = 1
    if level == 0:
        non_leaf = 0

    if len(rect_mbrs) <= 1:
        print('cant construct Rtree of one or zero entry(ies): ')
        print(str(rect_mbrs))
        return

    #reached the root
    if nodes < 1:
        root = [non_leaf, node_id, level_chunks[0]]
        rtree.write(str(root) + '\n')
        print( '1 node at level: %s '  % (level))
        return

    upper = []
    all_nodes = []
    for i in range(0, nodes):
        chunk = level_chunks[i]
        all_nodes.append([non_leaf , node_id , chunk])
        upper.append([node_id, get_mbr(chunk)])
        node_id += 1

    extra = int(len(rect_mbrs) % 20)
    if extra >= 8:
        upper.append([node_id, get_mbr(level_chunks[nodes])])
        all_nodes.append([non_leaf, node_id, level_chunks[nodes]])
        node_id += 1
    elif extra > 0:
        ###adjust### 
        new_node = [non_leaf, node_id]
        items = []
        last = all_nodes.pop()
        id = upper.pop()[0]
        for i in range(0, 8 - extra):
            items.insert(0, last[-1].pop())
        items.extend(level_chunks[nodes])
        new_node.append(items)
        all_nodes.append(last)
        all_nodes.append(new_node)
        upper.append([id, get_mbr(last[-1])])
        upper.append([node_id, get_mbr(items)])
        node_id += 1
        
    for node in all_nodes:
        rtree.write(str(node) + '\n')
    print('%s nodes at level: %s ' % (len(all_nodes), level))
    level += 1

    bulk_load(upper)

    ##construct mbrs for the next layer

#############3#main#################3
try:
    offset = open('offsets.txt', 'r')
    coords = open('coords.txt', 'r')
    rtree = open('rtree.txt' , 'w')
except:
    exit(1)

######## retrieve polygons and convert em into mbrs  
pol = offset.readline().rstrip("\n").split(',')
rectangles = []

while pol[0]:
    
    item = []
    xAxis = []
    yAxis = []
    mbr = []

    item.append(int(pol[0]))  #get the id
    for i in range(int(pol[1]), int(pol[2]) + 1):
        point = coords.readline().rstrip("\n").split(',')
        xAxis.append(float(point[0]))
        yAxis.append(float(point[1]))    

    mbr.extend([min(xAxis), max(xAxis), min(yAxis), max(yAxis)])
    item.append(mbr)

    z = get_z(mbr[0], mbr[1], mbr[2], mbr[3])
    item.append(z)
    rectangles.append(item)
    pol = offset.readline().rstrip("\n").split(',')

##########################construct our sorted list of MBRS and ids###########
rectangles = sorted(rectangles, key=lambda x: x[2])

for r in rectangles:
    r.pop()

bulk_load(rectangles)

###################################################################################################

offset.close()
coords.close()
rtree.close()
