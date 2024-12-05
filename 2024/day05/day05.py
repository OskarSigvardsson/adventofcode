from collections import defaultdict

m = defaultdict(set)
us = []

for line in open("../inputs/day05-real.txt"):
	if line.count("|") > 0:
		n1,n2 = [int(n) for n in line.split("|")]
		m[n1].add(n2)
	
	if line.count(",") > 0:
		us.append([int(n) for n in line.split(",")])

def ordered(l):
	for i in range(1, len(l)):
		for j in range(0, i):
			if l[j] in m[l[i]]: return False

	return True

p1 = sum(u[len(u)//2] for u in us if ordered(u))
print(f"Part 1: {p1}")

def correct(l1):
	l2 = l1[:]
	for i in range(1, len(l2)):
		for j in range(0, i):
			# swap the incorrect ones
			if l2[j] in m[l2[i]]:
				l2[i],l2[j] = l2[j],l2[i]

	return l2
	
corrected = [correct(u) for u in (u for u in us if not ordered(u))]
p2 = sum(u[len(u)//2] for u in corrected)

print(f"Part 2: {p2}")