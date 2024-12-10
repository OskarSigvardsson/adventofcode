from itertools import product

grid = [line.strip() for line in open("../inputs/day10-real.txt")]

w = len(grid[0])
h = len(grid)
dirs =[(1,0),(0,1),(-1,0),(0,-1)] 

def sample(x,y):
    if 0 <= x < w and 0 <= y < h: 
        return int(grid[y][x])
    return -1

def union(iter):
    return set().union(*iter)

def trail_ends(x,y, depth = 0):
    s = sample(x,y)
    if s == 9: return set([(x,y)])

    return union(trail_ends(x+dx,y+dy) for dx,dy in dirs if sample(x+dx,y+dy) == s+1)

# could memoize this to make it faster, but why bother
def trail_paths(x,y):
    s = sample(x,y)
    if s == 9: return 1

    return sum(trail_paths(x+dx,y+dy) for dx,dy in dirs if sample(x+dx,y+dy) == s+1)


p1 = sum(len(trail_ends(x,y)) for x,y in product(range(w), range(h)) if sample(x,y) == 0)
p2 = sum(trail_paths(x,y) for x,y in product(range(w), range(h)) if sample(x,y) == 0)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")