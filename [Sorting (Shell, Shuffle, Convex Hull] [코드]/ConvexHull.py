import math

def degreeScan(init_point, arys):
    new_arys = []
    for ary in arys:
        degree = math.atan2(ary[1] - init_point[1],ary[0] - init_point[0])
        new_list = list(ary)
        new_list.append(degree)
        new_arys.append(new_list)
    return new_arys

# Determine if the line i->j->k is a counter-clockwise turn
# Each of i, j, and k is a 3-tuple (x coordinate, y coordinate, degree)
def ccw(i, j, k):
    area = (j[0] - i[0]) * (k[1] - i[1]) - (j[1] - i[1]) * (k[0] - i[0])
    if area > 0: return True
    else: return False

def grahamScan(arys):
    # finding starting point with smallest y and biggest x
    init_point = arys[0]
    for ary in arys[1:]:
        if ary[1] < init_point[1]:
            init_point = ary
        elif ary[1] == init_point[1]:
            if ary[0] > init_point[0]:
                init_point = ary

    # sorting in a way that smaller degree, smaller y and smaller x comes last.
    arys.sort(key=lambda p: (-p[1],-p[0]))
    new_arys = degreeScan(init_point, arys)
    new_arys.sort(key=lambda p:-p[2])

    stack = []
    while len(new_arys) > 0: # repeat til none is left in the array
        stack.append(new_arys.pop())
        if len(stack) <= 2: continue
        cc = ccw(stack[-3], stack[-2], stack[-1])
        if not cc:
            new_arys.append(stack.pop())
            stack.pop()

    # final check whether last 2 items and starting point make a straight line
    cc = ccw(stack[-2], stack[-1], stack[0])
    if not cc:
        stack.pop()

    # convert list into tuple
    result = []
    for ary in stack:
        tup = tuple(ary[:2])
        result.append(tup)
    return result

'''
Unit Test
'''
if __name__ == "__main__":
    #print(grahamScan([(0,0),(-2,-1),(-1,1),(1,-1),(3,-1),(-3,-1)]))
    print(grahamScan([(4,2),(3,-1),(2,-2),(1,0),(0,2),(0,-2),(-1,1),(-2,-1),(-2,-3),(-3,3),(-4,0),(-4,-2),(-4,-4)]))
