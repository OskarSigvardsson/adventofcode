import re
from collections import defaultdict
from itertools import product

with open("../inputs/day03-real.txt") as f:
    grid = [list(f) for f in f]

    # Part 1
    w,h = len(grid[0]), len(grid)
    s = 0
    sx = None
    x,y = 0,0
    n = 0

    def check_boundary(y, minx, maxx):
        for y in range(max(0, y-1), min(h-1, y+2)):
            for x in range(max(0, minx-1), min(w-1, maxx+2)):
                c = grid[y][x]

                if c not in ".0123456789\n":
                    return True

        return False
    
    for y,x in product(range(h), range(w)):
        c = grid[y][x]

        if c in "0123456789":
            if n == 0:
                sx = x
                
            n = 10*n + int(c)
            continue
        else:
            if n != 0 and check_boundary(y, sx, x - 1):
                s += n

            n = 0

    print("Part 1: {}".format(s))


    # Part 2
    s = 0
    for y,x in product(range(h), range(w)):
        c = grid[y][x]
        if c == "*":
            y2,x2 = y-1,x-1
            ns = []
            
            while True:
                if y2 >= h or y2 > y + 1:
                    break
                    
                elif y2 < 0 or x2 >= w or x2 > x + 1:
                    y2 += 1
                    x2 = x - 1

                elif x2 < 0:
                    x2 += 1

                elif grid[y2][x2] in "0123456789":
                    nbeg,nend = x2,x2

                    while nend < w and grid[y2][nend] in "0123456789":
                        nend += 1

                    while nbeg > 0 and grid[y2][nbeg-1] in "0123456789":
                        nbeg -= 1

                    ns.append(int("".join(grid[y2][nbeg:nend])))

                    x2 = nend

                else:
                    x2 += 1

            if len(ns) == 2:
                s += ns[0]*ns[1]

    print("Part 2: {}".format(s))
