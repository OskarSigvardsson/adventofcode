from itertools import combinations

reports = [[int(n) for n in line.split(' ')] for line in open("../inputs/day02-real.txt")]

def sign(n):
	if n < 0: return -1
	if n > 0: return 1
	return 0
	
def is_safe(r):
	ds = [a - b for a,b in zip(r, r[1:])]

	pos = all(sign(d) == 1 for d in ds)
	neg = all(sign(d) == -1 for d in ds)
	siz = all(1 <= abs(d) <= 3 for d in ds)

	return siz and (pos or neg)

def is_dampened_safe(r):
	return any(is_safe(c) for c in combinations(r, len(r) - 1))

p1 = sum(1 for r in reports if is_safe(r))
p2 = sum(1 for r in reports if is_dampened_safe(r))

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")


