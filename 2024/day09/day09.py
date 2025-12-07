from dataclasses import dataclass
from itertools import cycle

line = "".join(line.strip() for line in open("../inputs/day09-test.txt"))
diskmap = [int(n) for n in line]

disk = []

fileId = 0
for size,isFile in zip(diskmap, cycle([True, False])):
	disk.extend([fileId if isFile else '.'] * size)

	if isFile: fileId += 1 
	
p1 = 0
p2 = len(disk) - 1

while p2 > p1:
	if disk[p1] != '.': 
		p1 += 1
		continue

	if disk[p2] == '.': 
		p2 -= 1
		continue
	
	disk[p1],disk[p2] = disk[p2],disk[p1]

p1 = sum(int(c)*i for i,c in enumerate(disk) if c != '.')
print(f"Part 1: {p1}")


def fun(v):
	match v:
		case (x,y): print("it's a position, and it's x value is", x)
		case [x,y,z]: print("it's a list with three things in it", x, y, z)