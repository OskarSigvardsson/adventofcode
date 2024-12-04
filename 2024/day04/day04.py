from itertools import product

grid = [line.strip() for line in open("../inputs/day04-real.txt")]
w = len(grid[0])
h = len(grid)

def sample(x,y):
    if 0 <= x < w and 0 <= y < h: return grid[y][x]
    return " ";

def word(p, d):
    x,y = p
    dx,dy = d
    return "".join(sample(x+dx*i, y+dy*i) for i in range(4))

ds = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

p1 = 0
for p in product(range(w), range(h)):
    for d in ds:
        p1 += 1 if word(p,d) == "XMAS" else 0


print(f"Part 1: {p1}")

p2 = 0

for (x,y) in product(range(w), range(h)):
    if sample(x,y) != "A": continue
    w1 = "".join(sorted([sample(x-1,y-1), sample(x+1,y+1)]))
    w2 = "".join(sorted([sample(x-1,y+1), sample(x+1,y-1)]))

    p2 += 1 if w1 == "MS" and w2 == "MS" else 0

print(f"Part 2: {p2}")
