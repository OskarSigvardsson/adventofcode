from itertools import product

grid = [line.strip() for line in open("../inputs/day12-real.txt")]

w = len(grid[0])
h = len(grid)

dirs = [(1,0),(0,-1),(-1,0),(0,1)]

corners = [
    [( 1, 0), ( 1,-1), ( 0,-1)],
    [( 0,-1), (-1,-1), (-1, 0)],
    [(-1, 0), (-1, 1), ( 0, 1)],
    [( 0, 1), ( 1, 1), ( 1, 0)],
]

def sample(x,y):
    if 0 <= x < w and 0 <= y < h: 
        return grid[y][x]
    return '.'

def corner_count(x,y,area):
    s1 = sum([False, False, False] == [(x+dx,y+dy) in area for dx,dy in corner] for corner in corners)
    s2 = sum([ True, False,  True] == [(x+dx,y+dy) in area for dx,dy in corner] for corner in corners)
    s3 = sum([False,  True, False] == [(x+dx,y+dy) in area for dx,dy in corner] for corner in corners)
    return s1 + s2 + s3

plots = set((x,y) for x,y in product(range(w), range(h)))
regions = {}

p1 = 0
p2 = 0

while len(plots) > 0:
    x,y = next(iter(plots))
    c = sample(x,y)

    frontier = [(x,y)]
    area = set()
    perimeter = 0

    while len(frontier) > 0:
        x,y = frontier.pop()

        if sample(x,y) != c: 
            perimeter += 1
            continue

        if (x,y) not in plots:
            continue

        plots.remove((x,y))

        area.add((x,y))

        for dx,dy in dirs:
            frontier.append((x+dx, y+dy))

    cornercount = sum(corner_count(px,py,area) for px,py in area)

    p1 += len(area) * perimeter
    p2 += len(area) * cornercount

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
