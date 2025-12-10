# /// script
# dependencies = [
#   "z3-solver",
# ]
# ///

import z3
import re
import heapq

lines = list(open("../inputs/day10-real.txt"))
machines = []


for line in lines:
	indicators,buttons,joltage = re.match(r"\[(.*)\] (.*) \{(.*)\}$", line).groups()
	
	indicators = tuple(c == "#" for c in indicators)
	buttons = [[int(n) for n in s[1:-1].split(",")] for s in list(re.findall(r"\([\d,]+\)", buttons))]
	joltage = tuple(int(n) for n in joltage.split(","))
	
	machines.append((indicators, buttons, joltage))
	

# bog standard breadth-first search. using heapq because I was expecting to
# implement A* in part 2, but sort-of pointless here
def part1(goal, buttons):
	visited = set()
	frontier = [(0,tuple(False for _ in range(len(goal))))]
	
	while len(frontier) > 0:
		score, ind = heapq.heappop(frontier)
		
		if ind in visited:
			continue

		if ind == goal:
			return score
		
		visited.add(ind)
		
		for button in buttons:
			nind = list(ind)

			for n in button:
				nind[n] = not nind[n]
				
			heapq.heappush(frontier, (score + 1, tuple(nind)))
			
# This is obviously an integer linear programming problem, but I didn't want to
# write a solver, so i tried a bunch of A* versions first, but they were
# unacceptably slow. at some point i just gave up and used z3
def part2(buttons, goal):
	vars = [z3.Int(f"b{i}") for i in range(len(buttons))]
	solver = z3.Optimize()

	for var in vars:
		solver.add(var >= 0)

	for i in range(len(goal)):
		s = 0;
		for j in range(len(buttons)):
			if i in buttons[j]:
				s += vars[j]
		solver.add(s == goal[i])
		
	solver.minimize(sum(vars))
	
	r = solver.check()
	assert r == z3.sat

	m = solver.model()
	return sum(m[v].as_long() for v in vars)

print("Part 1:", sum(part1(goal, buttons) for goal,buttons,_ in machines))
print("Part 2:", sum(part2(buttons, joltage) for _,buttons,joltage in machines))
