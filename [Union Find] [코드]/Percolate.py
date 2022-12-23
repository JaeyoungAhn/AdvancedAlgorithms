import math
import random
import statistics

def run(n):  # NxN개만큼 t회의 시뮬레이션 반복

    '''
    Weighted Quick Union
    '''
    def root(i):
        while i != ids[i]:
            i = ids[i]
        return i

    def connected(p, q):
        return root(p) == root(q)

    def union(p, adj):
        if size[p] == 0 or size[adj] == 0: return
        id = root(p)
        id2 = root(adj)
        if id == id2: return
        '''
        If the size of the tree is the same,
        basically which component gonna be the parent
        won't matter at all
        '''
        if size[id] <= size[id2]:
            ids[id] = id2
            size[id2] += size[id]
        else:
            ids[id2] = id
            size[id] += size[id2]
    ''' 
    Weighted Quick Union Ends
    '''

    def union_drive(p): # 상하좌우에 열 수 있는지 체크
        direction = []
        if p-n >= 0:
            direction.append(p-n)
        if (p+1 < n*n) and ((p+1) % n != 0): # % has higher priority than +
            direction.append(p+1)
        if (p-1 >= 0 ) and ((p-1) % n != n-1):
            direction.append(p-1)
        if p+n < n*n:
            direction.append(p+n)
        for adj in direction:
            union(p, adj)


    ids = [0 for i in range((n * n) + 2)]
    size = [0 for i in range((n * n) + 2)]
    shuffle = [0 for i in range((n * n))]
    percolate = 0
    count = 0

    for i in range(n * n):
        ids[i] = i
        shuffle[i] = i

    ids[n*n]=n*n
    ids[n*n+1]=n*n+1
    size[n*n]=n+1 # first row + parent itself
    size[n*n+1]=n+1 # last row + parent itself

    '''
    first row 와 last row들은 이미 parent와 연결되어있고 first row간
    union을 진행하면 root가 같으므로 return이 될 것이다.
    하지만 open이 된 상태는 아니었으므로, 열린 개수 count에는 지장이 없다.
    '''

    for i in range(n): # 가상의 TOP과 BOTTOM과 연결
        ids[i] = n*n
        ids[n * n - n + i] = n*n+1

    random.shuffle(shuffle)

    while percolate == 0:
        size[shuffle[count]] += 1
        opened = shuffle[count]
        union_drive(opened)
        count += 1 # 몇개를 열었는가

        connect = connected((n * n), (n * n) + 1)

        if connect :
            percolate = 1

    return count / (n * n)






def simulate(n, t):
    means = []
    for i in range(t):
        means.append(run(n))

    mean = statistics.mean(means)
    print("mean                    = %.10f" % mean)
    stdev = statistics.stdev(means)
    print("stdev                   = %.10f" % stdev)
    print("95%% confidence interval = [%.10f, %.10f] " % (mean - 1.96 * stdev / math.sqrt(t), mean + 1.96 * stdev / math.sqrt(t)) )
    return mean, stdev


''' 
Unit Test
'''

'''
simulate(200,100)는 각각 n과 t이다.
즉 N x N과 시뮬레이션 반복 횟수 t를 이야기 한다.
Unit Test
'''
if __name__ == "__main__":
    print(simulate(200, 100))
    # simulate(200,100)
    # simulate(2,10000)
    # simulate(2,100000)
