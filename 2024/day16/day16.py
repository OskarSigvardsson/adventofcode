import heapq

from itertools import product

grid = [line.strip() for line in open("../inputs/day16-real.txt")]

w = len(grid[0])
h = len(grid)

sx,sy = None, None
ex,ey = None, None

for (x,y) in product(range(w), range(h)):
	if grid[y][x] == "S":
		sx,sy = x,y
	if grid[y][x] == "E":
		ex,ey = x,y

states = [((sx,sy),(1,0),None)]
		
def rotate(c,state):
	p,d,path = states[state]
	dx,dy = d
	d = (dx+dy*1j)*c
	d = (int(d.real),int(d.imag))
	ns = len(states)
	states.append((p,d,state))
	return ns

def advance(state):
	p,d,path = states[state]
	dx,dy = d
	x,y = p
	p = x+dx,y+dy
	ns = len(states)
	states.append((p,d,state))
	return ns


def path():
	frontier = [(0,0)]
	visited = {}
	prev = {}
	tiles = set()
	best = float('inf')
	curr = 0

	while len(frontier) > 0:
		score,state = heapq.heappop(frontier)
		p,d,prev = states[state]
		x,y = p

		if score > best: break
		if grid[y][x] == "#": continue
		if (p,d) in visited and visited[(p,d)] < score: continue
		
		if x == ex and y == ey: 
			best = min(best, score)
			it = state
			while it:
				tiles.add(states[it][0])
				it = states[it][2]
			continue
			
		visited[(p,d)] = score

		heapq.heappush(frontier, (score+1,   advance(state)))
		heapq.heappush(frontier, (score+1000,rotate(1j,state)))
		heapq.heappush(frontier, (score+1000,rotate(-1j,state)))
		
	return best,len(tiles)

p1,p2 = path()

print(f"Part 1: {p1}")
print(f"Part 1: {p2}")
