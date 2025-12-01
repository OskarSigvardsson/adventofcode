
lines = list(open("../inputs/day01-real.txt"))

signs = { "L": -1, "R": 1 }

dial = 50
part1 = 0

for line in lines:
	sign = signs[line[0]]
	turn = int(line[1:])
	
	dial = (dial + sign * turn) % 100
	if dial == 0: 
		part1 += 1
		
dial = 50
part2 = 0

for line in lines:
	sign = signs[line[0]]
	turn = int(line[1:])

	for _ in range(turn):
		dial = (dial + sign) % 100
		if dial == 0:
			part2 += 1

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")