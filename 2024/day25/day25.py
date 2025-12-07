from itertools import batched, product

lines = [line.strip() for line in open("../inputs/day25-real.txt")]
chunks = [batch[:-1] for batch in batched(lines, 8)]

locks = [chunk for chunk in chunks if all(c == "#" for c in chunk[0])]
keys = [chunk for chunk in chunks if all(c == "#" for c in chunk[-1])]

p1 = 0
for lock,key in product(locks,keys):
	lc = [len([c for c in r if c == "#"]) for r in zip(*lock)]
	kc = [len([c for c in r if c == "#"]) for r in zip(*key)]
	
	# print(lc)
	# print("\n".join(lock))
	# print("-----------------")
	# print(kc)
	# print("\n".join(key))
	if all(l1+l2 <= 8 for l1,l2 in zip(lc,kc)):
		#print("fits")
		p1 += 1
	#print("=================")
		
print(p1)