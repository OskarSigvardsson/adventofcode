import sys

from itertools import count
from collections import defaultdict

EMPTY = "."
WALL = "#"
SAND = "o"

m = defaultdict(lambda: EMPTY)
xmin, xmax = sys.maxsize, -sys.maxsize
ymin, ymax = sys.maxsize, -sys.maxsize
floor = 0

def sgn(n):
    if n == 0:
        return 0
    elif n > 0:
        return 1
    return -1

def segment(sx,sy,dx,dy):
    if sx == dx and sy == dy:
        yield (sx,sy)
    elif sx == dx:
        for y in range(sy, dy, sgn(dy - sy)):
            yield (sx,y)
        yield (sx, dy)
    elif sy == dy:
        for x in range(sx, dx, sgn(dx - sx)):
            yield (x,sy)
        yield (dx, sy)
    else:
        assert(false)
        
def debug():
    for y in range(ymin, max(ymax+1, floor+1)):
        for x in range(xmin, xmax+1):
            print(get(x,y), end='')
        print()

with open("input.txt") as f:
    for line in f:
        coords = [[int(n) for n in s.strip().split(",")] for s in line.split("->")]
        for s,d in zip(coords, coords[1:]):
            for x,y in segment(*s, *d):
                m[(x,y)] = WALL
                xmin,ymin = min(xmin, x), min(ymin, y)
                xmax,ymax = max(xmax, x), max(ymax, y)
                floor = max(floor, ymax + 2)


def get(x,y):
    if y == floor:
        return WALL
    return m[(x,y)]

def drop_sand():
    global xmin,ymin,xmax,ymax

    x,y = 500,0

    while True:
        if y > ymax + 2:
            return x,y
        elif get(x,y+1) == EMPTY:
            x,y = x,y+1
        elif get(x-1,y+1) == EMPTY:
            x,y = x-1,y+1
        elif get(x+1,y+1) == EMPTY:
            x,y = x+1,y+1
        else:
            xmin,ymin = min(xmin, x), min(ymin, y)
            xmax,ymax = max(xmax, x), max(ymax, y)
           
            m[(x,y)] = SAND
            return x,y
            
for i in count(1):
    x,y = drop_sand()
    if (x,y) == (500,0):
        print(i)
        break

debug()
