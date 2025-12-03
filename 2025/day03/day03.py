lines = [line.strip() for line in open("../inputs/day03-real.txt")]

length = len(lines[0])
memo = {}

def maxpower(line, col, digits):
	if digits == 0:
		return 0

	if col >= length:
		return -999999999999999999999
	
	if (line, col, digits) in memo:
		return memo[(line, col, digits)]
	
	# select this battery
	p1 = maxpower(line, col+1, digits-1) + 10**(digits-1) * int(lines[line][col])
	
	# skip this battery
	p2 = maxpower(line, col+1, digits)
	
	power = max(p1, p2)
	
	memo[(line, col, digits)] = power
	return power

part1 = sum(maxpower(line, 0,  2) for line in range(len(lines)))
part2 = sum(maxpower(line, 0, 12) for line in range(len(lines)))

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")