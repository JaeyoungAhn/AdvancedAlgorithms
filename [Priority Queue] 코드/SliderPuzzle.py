import copy
import queue
import random
from queue import PriorityQueue

class Board:
    def __init__(self, tiles):
        self.n = len(tiles)
        self.tiles = copy.deepcopy(tiles)
        self.twinBoard = None
        
        # Compute Hamming distance
        self.hammingDistance = 0
        goal = 0
        for rowId, row in enumerate(tiles):
            for colId, t in enumerate(row):
                goal += 1
                if t == 0: continue
                if t != goal: self.hammingDistance += 1

        # Compute Manhattan distance
        self.manhattanDistance = 0
        for rowId, row in enumerate(tiles):
            for colId, t in enumerate(row):
                if t == 0: continue
                goalRow, goalCol = (t-1) // self.n, (t-1) % self.n
                self.manhattanDistance += abs(rowId - goalRow) + abs(colId - goalCol)
                # 3 2 1
                # 4 5 6
                # 7 8 0

    # Create a human-readable string representation
    def __str__(self):
        strList = []
        for rowId, row in enumerate(self.tiles):
            for colId, t in enumerate(row):
                strList.append(f'{t:6d}')
            strList.append('\n')
        return ''.join(strList)

    def __repr__(self):
        return self.__str__()

    # Defines behavior for the equality operator, ==
    def __eq__(self, other):
        if other == None: return False
        if not isinstance(other, Board): return False
        
        if self.n != other.n: return False
        for rowId, row in enumerate(self.tiles):
            for colId, t in enumerate(row):
                if t != other.tiles[rowId][colId]: return False
        return True

    # Defines behavior for the less-than operator, <
    # This function is required to compare two Boards in a PriorityQueue
    def __lt__(self, other):
        if self.n < other.n: return True
        else:
            for rowId, row in enumerate(self.tiles):
                for colId, t in enumerate(row):
                    if t < other.tiles[rowId][colId]: return True
            return False

    def hamming(self):
        return self.hammingDistance
    
    def manhattan(self):
        return self.manhattanDistance

    def dimension(self):
        return len(self.tiles)

    def isGoal(self):
        return self.hammingDistance == 0
    
    def neighbors(self):
        # Create a neighbor board by switching (row,col) with (rowZero,colZero),
        #   where (rowZero,colZero) is the location of the empty tile
        def createNeighbor(tiles, row, col, rowZero, colZero):
            assert(tiles[rowZero][colZero] == 0)
            tiles[rowZero][colZero], tiles[row][col] = tiles[row][col], 0  # Switch two tiles
            neighbor = Board(self.tiles) # Create a neighbor with the switched tiles
            tiles[rowZero][colZero], tiles[row][col] = 0, tiles[rowZero][colZero] # Switch the tiles back to their original positions
            return neighbor

        # Find the empty tile and store its location in (rowZero, colZero)
        # rowZero, colZero = None, None
        for rowId, row in enumerate(self.tiles):
            for colId, t in enumerate(row):
                if t==0: rowZero, colZero = rowId, colId        

        neighborList = []
        if rowZero>0: neighborList.append(createNeighbor(self.tiles, rowZero-1, colZero, rowZero, colZero)) # Push down the empty tile
        if rowZero<self.dimension()-1: neighborList.append(createNeighbor(self.tiles, rowZero+1, colZero, rowZero, colZero)) # Push up the empty tile
        if colZero>0: neighborList.append(createNeighbor(self.tiles, rowZero, colZero-1, rowZero, colZero)) # Push right to the empty tile
        if colZero<self.dimension()-1: neighborList.append(createNeighbor(self.tiles, rowZero, colZero+1, rowZero, colZero)) # Push left to the empty tile

        return neighborList

    def twin(self):
        if self.twinBoard == None:
            # Randomly select two tile numbers to swap
            numbers4Twin = list(range(1,self.dimension()*self.dimension()))
            random.shuffle(numbers4Twin)

            # Identify (row, col) of the two tiles
            for rowId, row in enumerate(self.tiles):
                for colId, t in enumerate(row):
                    if t==numbers4Twin[0]: row1, col1 = rowId, colId
                    elif t==numbers4Twin[1]: row2, col2 = rowId, colId
            
            # Swap the two tiles to create a twin board
            self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1]
            self.twinBoard = Board(self.tiles)
            self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1] # Swap the two tiles back to their original positions

        return self.twinBoard


def solveNprint(initialBoard): #결과 출력에 사용
        solution = solveManhattan(initialBoard)
        if solution != None:
            print(f"Solvable in {len(solution)-1} moves")
            for board in solution:
                print(board)
        else: print("Unsolvable")


def solveManhattan(initialBoard): # 구현해야하는 함수이다. initialBoard는 보드 객체
    assert(isinstance(initialBoard, Board))

    # Priority Queue
    minPQ = queue.PriorityQueue()

    # 하나의 초기 상태를 나타내며 Board 객체에 추가 정보를 담은 아래와 같은 4-tuple이다.
    #(현재까지 이동횟수+Manhattan 거리, Board 객체, 현재까지 이동 횟수, 직전 상태를 나타내는, 4-tuple)
    minPQ.put((0+initialBoard.manhattan(), initialBoard, 0, None))

    while True:
        get_node = minPQ.get()

        # minNode가 목표 상태와 같다면?
        if Board.isGoal(get_node[1]):
            ans = []
            ans.append(get_node[1])
            while(get_node[3] != None):
                get_node = get_node[3]
                ans.append(get_node[1])
            ans.reverse()
            return ans
        else:
            #minNode의 각 neighbor를 아래와 같이 minPQ에 추가한다. 직전 neighbor는 제외
            for node in Board.neighbors(get_node[1]):
                temp_node = get_node[3]
                if (temp_node is not None) and (node == temp_node[1]):
                    continue
                minPQ.put((get_node[2]+1+Board.manhattan(node), node, get_node[2]+1, get_node))


if __name__ == "__main__":    
    
    # Solvable in 0 move (already solved)
    # b10 = Board([[1,2,3],[4,5,6],[7,8,0]])
    # solveNprint(b10)
    
    # Solvable in 4 moves
    # b11 = Board([[0,1,3],[4,2,5],[7,8,6]])
    # solveNprint(b11)


    # Solvable in 14 moves
    # b12 = Board([[8,1,3],[4,0,2],[7,6,5]])
    # solveNprint(b12)
    
    # Solvable in 24 moves
    b14 = Board([[3,2,1],[6,5,4],[0,7,8]])
    solveNprint(b14)
    # print(b14.hamming())
    # print(b14.manhattan())
    
    # Solvable in 4 moves
    # b15 = Board([[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20],[21,22,23,24,25,26,27,28,29,30],\
    #     [31,32,33,34,35,36,37,38,39,40],[41,42,43,44,45,46,47,48,49,50],[51,52,53,54,55,56,57,58,59,60],\
    #     [61,62,63,64,65,66,67,68,69,70],[71,72,73,74,75,76,77,78,79,80],[81,82,83,84,85,86,0,87,89,90],\
    #     [91,92,93,94,95,96,97,88,98,99]])
    # solveNprint(b15)
    # print(b15.hamming())
    # print(b15.manhattan())


    '''
    #
    # Unit Test for Board
    #
    b1 = Board([[1,2,3],[4,5,6],[7,8,0]])
    b2 = Board([[1,2,3],[4,5,6],[7,8,0]])
    b3 = Board([[1,2,3],[4,5,6],[8,7,0]])    
    print(b1)
    print(b1 == b2)
    print(b1 == b3)

    for b in b1.neighbors():
        print(b)
    b4 = Board([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])    
    for b in b4.neighbors():
        print(b)
    b5 = Board([[8,1,3],[4,0,2],[7,6,5]])
    for b in b5.neighbors():
        print(b)

    print(b1.hamming())    
    print(b3.hamming())
    print(b4.hamming())
    print(b5.hamming())

    print(b1.manhattan())
    print(b3.manhattan())
    print(b4.manhattan())
    print(b5.manhattan())

    print(b1.isGoal())
    print(b3.isGoal())
    print(b4.isGoal())
    print(b5.isGoal())

    print(b1.twin())
    print(b3.twin())
    print(b4.twin())
    print(b5.twin())
    '''

    