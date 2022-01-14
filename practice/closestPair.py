import math
import numpy as np
import copy

"""function to calculate distance between two points

args:
    a(tuple): tuple of size 2 in format, (x,y) representing a point
    b(tuple): tuple of size 2 in format, (x,y) representing a point
    
returns:
    float: distance between point a and point b"""


def distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


"""brute force function to calculate closest pair

args: 
    points(list): list of tuples of size 2 in format,(x,y)

returns: 
    float:distance between closest pair

"""


def bruteforceclosestpair(points):
    if len(points) <= 1:
        return 0
    d = float('inf')  # distance
    closest_pair = [points[0], points[1]]  # list to hold closest pair of points
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            if d > distance(points[i],
                            points[j]):  # if distance is greater than current calculated distance
                d = distance(points[i], points[j])  # update distance
                closest_pair[0] = points[i]
                closest_pair[1] = points[j]
    return d, closest_pair


"""function to find closest pair within delta of groups of points
args:
    x(list): list of points sorted by x coordinates
    y(list): list of points sorted by y coordinates
    delta(float): current shortest distance between pair of points
    curr_best(list): list of current closest pair

returns:
    curr_best[0]: point a
    curr_best[1]: point b
    best: distance between a and b
"""


def closest_split_pair(x, y, delta, curr_best):
    ln_x = len(x)
    mid_x = x[ln_x // 2][0]  # median in x-sorted array

    # array of points within delta on x-sorted array
    s = [x for x in y if abs(mid_x - delta) <= delta]
    best = delta  # assign best value to delta
    ln_y = len(s)
    for i in range(ln_y - 1):
        for j in range(i + 1, min(i + 7, ln_y)):
            a, b = s[i], s[j]
            dst = distance(a, b)
            if dst < best:
                curr_best = a, b
                best = dst
    return curr_best[0], curr_best[1], best


"""recursive divide and conquer function to calculate closest pair of points 
args:
    x(list): list of points sorted by x coordinates
    y(list): list of points sorted by y coordinates
    Pair(list): list to keep track of closest pair of points
    
returns:
    list: list of closest pair of points
"""


def closestpair(x, y, pair=[0, 0]):
    if len(x) <= 3:  # if len of given list is than 4, use brute force method
        return bruteforceclosestpair(x)

    mid = len(x) // 2  # ceiling midpoint
    pl = x[:mid]  # copy all points till midpoint (by x coordinate)
    pr = x[mid:]  # copy all points from midpoint (by x coordinate)

    ql = [point for point in y if point[0] <= x[mid][0]]  # copy same points till midpoint (by x coordinate)
    qr = [point for point in y if point[0] > x[mid][0]]  # copy same points from midpoint (by x coordinate) till end

    d1, pair1 = closestpair(pl, ql)  # recursively find closest pair distance on all points till midpoint (inclusive)
    d2, pair2 = closestpair(pr, qr)  # recursively find closest pair distance on all points from midpoint till end
    min_pair = []
    d = 0

    # take smallest distance of the two and copy the corresponding pair
    if d1 >= d2:
        d = d2
        min_pair = pair2
    else:
        d = d1
        min_pair = pair1

    (pair[0], pair[1], best_in_split) = closest_split_pair(x, y, d, min_pair)

    if d <= best_in_split:
        return d, min_pair

    return best_in_split, pair



"""Function to create a list of random integers

args:
    size(int): size of list to be created

returns: 
    list of random integers
"""


def ListGenerator(size):
    return np.random.randint(low=1, high=1001, size=size)  # Generate uniform random numbers
    # from 1 to 1000


"""Function to generate points

args:
    length(int, optional): number of points to create
    
returns:
    list of points

"""


def pointsGenerator(length=100):
    x = ListGenerator(length)
    y = ListGenerator(length)
    points = []
    for i in range(0, length):
        points.append((x[i], y[i]))
    return points


"""Function to test closestpair function

args:
    points(list): list of points

returns:
    shortest distance and respective pair of points

"""


def testCase(points):
    sortedX = sorted(points, key=lambda x: x[0])
    sortedY = sorted(points, key=lambda y: y[1])
    distance, closestPair = closestpair(sortedX, sortedY)
    print("By D&C\nDistance: "+ str(distance), ", Pair: " + str(closestPair))


points = [(-0.10, 5.58), (-0.67, 5.83), (-2.25, 4.85), (-0.32, 11.05), (-2.57, 7.48), (-1.25, 5.08), (-0.28, 6.05),
          (-1.47, 6.68), (-1.67, 6.28), (-0.52, 8.52), (-0.90, 9.63), (-1.75, 4.97), (-0.83, 9.37), (0.00, 5.68),
          (-3.00, 4.70), (-1.93, 10.93), (0.68, 5.77), (-3.33, 7.77)]
testCase(points)
testPoints = pointsGenerator(100)
testCase(testPoints)
best_dist, closest = bruteforceclosestpair(testPoints)
print("By Bruteforce\nDistance: " + str(distance(closest[0],closest[1])), ", Pair: " + str(closest))


