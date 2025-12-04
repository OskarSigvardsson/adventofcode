
lines = [line.strip() for line in open('../inputs/day04-real.txt')]

w = len(lines[0])
h = len(lines)

orig = {(x,y): lines[y][x] for x in range(w) for y in range(h)}

def roll(m, x, y):
	if x not in range(w): return 0
	if y not in range(h): return 0
	
	return 1 if m[(x,y)] == '@' else 0

def accessible(m, x, y):
	if roll(m,x,y) == 0: return 0

	s =  sum(roll(m, x+dx,y+dy) for dx in [-1,0,1] for dy in [-1,0,1] if not (dx == 0 and dy == 0))
	
	return 1 if s < 4 else 0

def prune(m):
	nm = {}
	removed = 0

	for (x,y) in ((x,y) for x in range(w) for y in range(h)):
		if m[(x,y)] == '.':
			nm[(x,y)] = '.'
		elif accessible(m,x,y): 
			nm[(x,y)] = '.'
			removed += 1
		else:
			nm[(x,y)] = '@'
			
	return removed, nm
	
part1 = sum(accessible(orig, x,y) for x in range(w) for y in range(h))

m = orig
part2 = 0

while True:
	removed,nm = prune(m)
	m = nm
	part2 += removed

	if removed == 0:
		break
	
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")