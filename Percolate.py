import math
import random
import statistics

def run(n):  # n x n개만큼 t회의 시뮬레이션 반복

    ids = [0 for i in range((n * n) + 2)]
    size = [0 for i in range((n * n) + 2)]
    shuffle = [0 for i in range((n * n))]
    percolate = 0
    count = 0

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
        if size[id] <= size[id2]:
            ids[id] = id2
            size[id2] += size[id]
        else:
            ids[id2] = id
            size[id] += size[id2]

    def union_drive(p): # 상하좌우에 열 수 있는지 체크
        direction = []
        if p-n >= 0:
            direction.append(p-n)
        if (p+1 < n*n) and (p+1 % n != 0):
            direction.append(p+1)
        if (p-1 >= 0 ) and (p-1 % n != n-1):
            direction.append(p-1)
        if p+n < n*n:
            direction.append(p+n)
        for adj in direction:
            union(p, adj)

    for i in range(n * n):
        ids[i] = i
        shuffle[i] = i

    ids[n*n]=n*n
    ids[n*n+1]=n*n+1
    size[n*n]=n+1
    size[n*n+1]=n+1

    for i in range(n): # 가상의 TOP과 BOTTOM과 연결
        ids[i] = n*n
        ids[n * n - n + i] = n*n+1

    random.shuffle(shuffle)

    while percolate == 0:
        size[shuffle[count]] += 1
        opened = shuffle[count]
        union_drive(opened)
        count += 1

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
if __name__ == "__main__":
    print(simulate(200, 100))
    # simulate(200,100)
    # simulate(2,10000)
    # simulate(2,100000)