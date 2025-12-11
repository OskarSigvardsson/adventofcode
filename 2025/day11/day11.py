from collections import defaultdict

verts = []
edges = {}

for line in [line.strip() for line in open("../inputs/day11-real.txt")]:
	a,bs = line.split(":")
	bs = bs.strip().split(" ")
	
	verts.append(a)
	edges[a] = bs

def count1(src, dst):
	if src == dst: return 1
	
	return sum(count1(v, dst) for v in edges[src])

def count2(src, dst, musts, memo = {}):
	if src == dst: 
		if musts == ():
			return 1
		return 0
	
	if (src, musts) in memo: return memo[(src, musts)]

	nmusts = tuple(m for m in musts if src != m)

	ret = sum(count2(v, dst, nmusts) for v in edges[src])
	
	memo[(src,musts)] = ret

	return ret

print("Part 1:", count1("you", "out"))
print("Part 2:", count2("svr", "out", ("dac", "fft")))