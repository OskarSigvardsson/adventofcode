
input = [int(n) for n in open("../inputs/day11-real.txt").readline().split(' ')]

def split(stone):
	s = str(stone)
	l = len(s)
	if l % 2 == 0:
		return int(s[:l//2]),int(s[l//2:])
	return None

# i don't there are decorators for memoization, but i'm OLD SCHOOL
memo = {}

def stones(stone, gen):
	global memo
	if gen == 0: return 1

	if (stone,gen) in memo: return memo[(stone,gen)]
	
	res = 0
	if stone == 0: 
		res = stones(1, gen-1)
	elif sp := split(stone):
		res = stones(sp[0], gen-1) + stones(sp[1], gen-1)
	else:
		res = stones(stone * 2024, gen-1)

	memo[(stone,gen)] = res
	return res

p1 = sum(stones(stone, 25) for stone in input)
p2 = sum(stones(stone, 75) for stone in input)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")