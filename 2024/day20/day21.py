import heapq
from itertools import product
from collections import defaultdict

grid = [list(line.strip()) for line in open("../inputs/day20-test.txt")]

w,h = len(grid[0]),len(grid)
sx,sy = None,None
ex,ey = None,None

for x,y in product(range(w), range(h)):
	if grid[y][x] == "S":
		sx,sy = x,y
	if grid[y][x] == "E":
		ex,ey = x,y

def path(grid):
	for line in grid:
		print("".join(line))
	print("-"*w)
	frontier = [(0,(sx,sy))]
	visited = set()
	
	while len(frontier) > 0:
		s,p = heapq.heappop(frontier)
		x,y = p
		
		if grid[y][x] == "#": continue
		if p == (ex,ey): return s
		if p in visited: continue

		visited.add(p)

		heapq.heappush(frontier, (s+1,(x+1,y  )))
		heapq.heappush(frontier, (s+1,(x-1,y  )))
		heapq.heappush(frontier, (s+1,(x  ,y+1)))
		heapq.heappush(frontier, (s+1,(x  ,y-1)))

def part1():
	ref = path(grid)
	saved = defaultdict(set)

	for x1,y2 in product(range(1,w-2),range(1,h-2)):
		if grid[y][x] != ".": continue

		for dx,dy in [(1,0),(0,-1),(-1,0),(0,1)]:
			x2,y2 = x1+dx,y2+dy
			if 
		
	for k,v in sorted(saved.items()):
		print(k,len(v))

	print(saved[64])
part1()