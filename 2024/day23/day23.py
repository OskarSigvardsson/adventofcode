from itertools import combinations

es = set()
vs = []

for line in open("../inputs/day23-real.txt"):
	a,b = line.strip().split("-")
	es.add((a,b))
	es.add((b,a))
	vs.extend([a,b])

vs = sorted(set(vs))
vc = len(vs)

p1 = 0
for t in combinations(vs,3):
	if any(x.startswith("t") for x in t) and all((x,y) in es for x,y in combinations(t,2)):
		p1+=1
		
def bk(r,p,x, indent = 0):
	print(" " * indent + f"bk({sorted(r)},{sorted(p)},{sorted(x)}", end = '')
	if len(p) == 0 and len(x) == 0:
		print(r)
	else:
		print()
		
	for v in p:
		


print(f"Part 1: {p1}")