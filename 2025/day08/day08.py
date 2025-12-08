from itertools import combinations

class Set:
	parent: "Set" = None
	size: int = 0
	
	def __init__(self):
		self.parent = self
		self.size = 1
	
	def find(self) -> "Set":
		root = self
		
		while root != root.parent:
			root = root.parent
			
		s = self
		# path compression
		while s != root:
			ns = s.parent
			s.parent = root
			s = ns

		return root
	
def union(s1: Set, s2: Set):
	r1 = s1.find()
	r2 = s2.find()
	
	if r1 == r2: return

	if r1.size < r2.size:
		r1,r2 = r2,r1
		
	r2.parent = r1
	r1.size += r2.size

def dist(p1,p2) -> int:
	x1,y1,z1 = p1
	x2,y2,z2 = p2
	
	return (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2

verts = [tuple(int(n) for n in line.split(",")) for line in open("../inputs/day08-real.txt")]

edges = list(combinations(range(len(verts)), 2))
edges.sort(key=lambda a: dist(verts[a[0]], verts[a[1]]))

def part1(edgecount): 
	sets = [Set() for i in range(len(verts))]

	for i,j in edges[:edgecount]:
		union(sets[i], sets[j])
	
	sets.sort(key = lambda s: -s.size)

	s1 = sets[0].size
	s2 = sets[1].size
	s3 = sets[2].size

	return s1 * s2 * s3
	
def part2():
	sets = [Set() for i in range(len(verts))]

	for i,j in edges:
		union(sets[i], sets[j])
		
		if sets[0].find().size == len(verts):
			return verts[i][0] * verts[j][0]

print(part1(1000))
print(part2())