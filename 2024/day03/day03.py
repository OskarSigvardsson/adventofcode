import re
input = "".join(line for line in open("../inputs/day03-real.txt"))

#part 1
mul = re.compile(r"mul\((\d+),(\d+)\)", flags=re.MULTILINE)
p1 = sum(int(a)*int(b) for a,b in mul.findall(input))
print(f"Part 1: {p1}")

#part 2
insts = re.compile(r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))", flags=re.MULTILINE)
p2 = 0
enabled = True

for inst in insts.finditer(input):
	match inst.groups():
		case [mul, a, b] if mul.startswith("mul"):
			p2 += int(a)*int(b) if enabled else 0
		case ["do()", _, _]:
			enabled = True
		case ["don't()", _, _]:
			enabled = False

print(f"Part 2: {p2}")