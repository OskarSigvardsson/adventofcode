from collections import defaultdict
from itertools import combinations

grid = [line.strip() for line in open("../inputs/day08-real.txt")]

w = len(grid[0])
h = len(grid)

def inside(p):
    return 0 <= p.real < w and 0 <= p.imag < h

antennae = defaultdict(list)

for y,line in enumerate(grid):
    for x,c in enumerate(line):
        if c != ".": antennae[c].append(x + y*1j)

p1set = set()

for ps in antennae.values():
    for p1,p2 in combinations(ps, 2):
        np1 = p2 + (p2 - p1)
        np2 = p1 + (p1 - p2)

        if inside(np1): p1set.add(np1)
        if inside(np2): p1set.add(np2)

print(f"Part 1: {len(p1set)}")

p2set = set()

for ps in antennae.values():
    for p1,p2 in combinations(ps, 2):
        d = p2 - p1

        np = p1
        while inside(np):
            p2set.add(np)
            np += d

        np = p1
        while inside(np):
            p2set.add(np)
            np -= d

print(f"Part 2: {len(p2set)}")