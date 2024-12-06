from itertools import product 

grid = [list(line.strip()) for line in open("../inputs/day06-real.txt")]

w = len(grid[0])
h = len(grid)

def start():
	for y,line in enumerate(grid):
		for x,c in enumerate(line):
			if c == "^": return x,y
		
	return None

def add(p,d):
	return (p[0] + d[0], p[1] + d[1])

def inside(p):
	x,y = p
	return 0 <= x < w and 0 <= y < h

sx,sy = start()

turn = {
	( 0,-1): ( 1, 0),
	( 1, 0): ( 0, 1),
	( 0, 1): (-1, 0),
	(-1, 0): ( 0,-1),
}

def part1():
	p = sx,sy
	d = 0,-1

	visited = set()

	while inside(p):
		visited.add(p)
		nx,ny = add(p, d)
		
		if inside((nx,ny)) and grid[ny][nx] == "#":
			d = turn[d]
		else:
			p = nx,ny
		
	p1 = len(visited)
	print(f"Part 1: {p1}")

def part2():
	global grid
	def loops():
		p = sx,sy
		d = 0,-1
		visited = set()

		while inside(p):
			if (p,d) in visited:
				return True

			visited.add((p,d))

			nx,ny = add(p, d)
			
			if inside((nx,ny)) and grid[ny][nx] == "#":
				d = turn[d]
			else:
				p = nx,ny
		
		return False
	
	p2 = 0

	for x,y in product(range(w), range(h)):
		if grid[y][x] != ".": continue

		grid[y][x] = "#"
		p2 += 1 if loops() else 0
		grid[y][x] = "."
		
	print(f"Part 2: {p2}")

part1()
part2()