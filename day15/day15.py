import math
from heapq import heappush, heappop

def path(d, dest):
    closed = {}
    frontier = [(0, (0,0))]

    while dest not in closed:
        dist, (x,y) = heappop(frontier)

        if (x,y) in closed:
            continue
        
        closed[(x,y)] = dist

        heappush(frontier, (dist + d(x-1, y), (x-1, y)))
        heappush(frontier, (dist + d(x, y-1), (x, y-1)))
        heappush(frontier, (dist + d(x+1, y), (x+1, y)))
        heappush(frontier, (dist + d(x, y+1), (x, y+1)))
        
    return closed[dest]


with open("input.txt", "r") as f:
    m = [[int(c) for c in line.strip()] for line in f]

    w,h = len(m[0]), len(m)
    
    def d1(x,y):
        if x < 0 or y < 0 or x >= w or y >= h:
            return math.inf
        
        return m[y][x]

    def d2(x,y):
        if x < 0 or y < 0 or x >= 5*w or y >= 5*h:
            return math.inf

        dx,dy = x//w, y//h
        mx,my = x%w, y%h

        return (m[my][mx] + dx + dy - 1) % 9 + 1

    print(f"Part 1: { path(d1, (w-1,h-1)) }")
    print(f"Part 2: { path(d2, (5*w-1,5*h-1)) }")
