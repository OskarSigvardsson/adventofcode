from functools import reduce

input = list(open("../inputs/day06-real.txt"))

# part 1
lines = [
	[s.strip() for s in line.split(" ") if s != ""] for line in input
]

ops = { '+': lambda a,b:a+b, '*': lambda a,b:a*b }
part1 = 0
for col in zip(*lines):
	part1 += reduce(ops[col[-1]], [int(s) for s in col[:-1]])
	

# part 2
# just compute the transpose of the entire file, basically
opline = [s.strip() for s in input[-1].strip().split(" ") if s != ""]
nlines = [line for line in input[:-1]] 
ns = [[]]

for t in zip(*[line[:-1] for line in nlines]):
	s = "".join(t).strip()
	if s == "":
		ns.append([])
	else:
		ns[-1].append(int(s))

part2 = sum(reduce(ops[op], n) for (op,n) in zip(opline, ns))

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")