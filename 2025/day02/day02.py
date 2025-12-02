ranges = []

for r in open("../inputs/day02-real.txt").read().split(","):
	a,b = r.split("-")
	ranges.append((int(a), int(b)))
	
def valid1(id):
	s = str(id)
	l = len(s) // 2

	return s[:l] != s[l:]

def valid2(id):
	s = str(id)
	l = len(s)
	for i in range(1, l//2 + 1):
		if s == s[:i] * (l//i):
			return False
	
	return True

part1 = sum(sum(id for id in range(a,b+1) if not valid1(id)) for (a,b) in ranges)
part2 = sum(sum(id for id in range(a,b+1) if not valid2(id)) for (a,b) in ranges)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")