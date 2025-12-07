
lines = [line.strip() for line in open("../inputs/day07-real.txt")]
w = len(lines[0])
h = len(lines)

def part1():
	rays = { lines[0].find("S") }
	splits = 0

	for line in lines:
		newrays = set()

		for ray in rays:
			if line[ray] == "^":
				splits += 1
				newrays |= { ray - 1, ray + 1 }
			else:
				newrays |= { ray }
				
		rays = newrays
				
	return splits

def sample(x,y):
	if x not in range(w): return "."
	if y not in range(h): return "."
	return lines[y][x]

def timelines(x, y, memo = {}):
	if y == 0:
		return int(sample(x,y) == "S")

	if sample(x,y) == "^":
		return 0
	
	if (x,y) in memo:
		return memo[(x,y)]

	s = timelines(x,y-1)
	
	if sample(x-1,y) == "^": s += timelines(x-1,y-1)
	if sample(x+1,y) == "^": s += timelines(x+1,y-1)
	
	memo[(x,y)] = s
	return s

def part2():
	return sum(timelines(x,h-1) for x in range(w))

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
