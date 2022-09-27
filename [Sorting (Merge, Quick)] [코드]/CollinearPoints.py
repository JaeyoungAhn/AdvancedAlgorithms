def gradient(start_point, compare_point):
    if compare_point == start_point:
        return float('-inf')
    elif compare_point[1] - start_point[1] == 0:
        return 0
    elif start_point[0] - compare_point[0] == 0:
        return float('inf')
    else:
        return (compare_point[1] - start_point[1]) / (compare_point[0] - start_point[0])  # returns slope


def compare_coordinate(start, leftmost, rightmost, maximal_tuple):
    # This is to find out two endpoints in a straight line.
    # Starting point with -inf gradient, leftmost and rightmost points in the streak are the candidates.
    three_list = [start, leftmost, rightmost]
    three_list.sort(key=lambda x: (x[0], x[1]))

    # adding two endpoints in a tuple
    temp_list = []
    temp_list.extend(three_list[0][0:2])
    temp_list.extend(three_list[2][0:2])
    temp_tuple = tuple(temp_list)

    if temp_tuple not in maximal_tuple:
        maximal_tuple.append(temp_tuple)

def collinearPoints(points):
    points.sort(key=lambda x: (x[0], x[1]))  # smaller x with smaller y comes first
    maximal_tuple = []  # final tuple to be returned
    for start_point in points:
        deep_points = points[:]  # deep-copying the points
        for idx, point in enumerate(deep_points):
            temp_list = list(point)
            temp_list.append(gradient(start_point, point))
            deep_points[idx] = temp_list

        deep_points.sort(key=lambda x: x[2])  # sorting according to the gradient

        # To find out a straight line with more than 4 points
        streak = 1
        last_point = deep_points[0]
        for idx, point in enumerate(deep_points[1:], 1):
            if last_point[2] == point[2]:
                streak += 1
                if idx == len(deep_points)-1:  # streak broken as it reached last index
                    if streak >= 3:
                        leftmost = deep_points[idx + 1 - streak]
                        rightmost = point
                        compare_coordinate(start_point, leftmost, rightmost, maximal_tuple)
            else:  # streak broken as new point's gradient is different from last point
                if streak >= 3:
                    leftmost = deep_points[idx-streak]
                    rightmost = last_point
                    compare_coordinate(start_point, leftmost, rightmost, maximal_tuple)

                streak = 1
            last_point = point

    return maximal_tuple


if __name__ == "__main__":
    print(collinearPoints([(19000, 10000), (18000, 10000), (32000, 10000), (21000, 10000), (1234, 5678), (14000, 10000)]))
    print(collinearPoints([(10000,0),(0,10000),(3000,7000),(7000,3000),(20000,21000),(3000,4000),(14000,15000),(6000,7000)]))
    print(collinearPoints([(0,0),(1,1),(3,3),(4,4),(6,6),(7,7),(9,9)]))
    print(collinearPoints([(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(8,0)]))
    print(collinearPoints([(7,0),(14,0),(22,0),(27,0),(31,0),(42,0)]))
    print(collinearPoints([(12446,18993),(12798,19345),(12834,19381),(12870,19417),(12906,19453),(12942,19489)]))
    print(collinearPoints([(1,1),(2,2),(3,3),(4,4),(2,0),(3,-1),(4,-2),(0,1),(-1,1),(-2,1),(-3,1),(2,1),(3,1),(4,1),(5,1)]))
