from itertools import product
from collections import defaultdict

m = None
w,h = None, None

with open("../inputs/day14-real.txt", "r") as f:
    m = [list(line.strip()) for line in f]

    w,h = len(m[0]),len(m)

    c = tuple((x,y) for (y,x) in product(range(h), range(w)) if m[y][x] == "O")
    m = [[s if s != "O" else "." for s in row] for row in m]

def load(c):
    return sum(h-y for x,y in c)

def step_one(c, ds = [(0,-1),(-1,0),(0,1),(1,0)]):
    c2 = list(c)

    for d in ds:
        dx,dy = d
        while True:
            moved = False

            for i,p in enumerate(c2):
                x,y = p
                x2,y2 = x,y

                while True:
                    x2 += dx
                    y2 += dy

                    if x2 not in range(w) or y2 not in range(h):
                        break

                    if m[y2][x2] == "#" or (x2,y2) in c2:
                        break

                x2 -= dx
                y2 -= dy

                if (x,y) != (x2,y2):
                    c2[i] = (x2,y2)
                    moved = True

            if not moved:
                break

    return tuple(sorted(c2))
    
cache = defaultdict(dict)

def step(c, steps, depth = 0):
    if steps == 0:
        return c

    if steps in cache[c]:
        return cache[c][steps]

    if steps == 1:
        c2 = step_one(c)
        cache[c][1] = c2
        return c2
    
    hop1 = steps//2
    hop2 = steps - hop1

    c2 = step(c, hop1, depth+1)
    c3 = step(c2, hop2, depth+1)

    cache[c][steps] = c3
    return c3

        
part1 = load(step_one(c, ds = [(0,-1)]))
print("Part 1: {}".format(part1))

part2 = load(step(c, 1000000000))
print("Part 2: {}".format(part2))
