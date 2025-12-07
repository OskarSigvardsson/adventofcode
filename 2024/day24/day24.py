import re

vars = set()
initial = {}
rules = {}

ops = {
	"AND": lambda x,y: x & y,
	"OR":  lambda x,y: x | y,
	"XOR": lambda x,y: x ^ y,
}

for line in open("../inputs/day24-real.txt"):
	if m := re.match(r"(.*): (.*)", line):
		var,val = m.group(1),int(m.group(2))
		initial[var] = val
		vars.add(var)

	if m := re.match(r"(.*) (AND|OR|XOR) (.*) -> (.*)", line):
		v1,op,v2,v3 = m.groups()
		rules[v3] = (v1,op,v2)
		vars.update([v1,v2,v3])

def value(var):
	if var in initial:
		return 1
	
	v1,op,v2 = rules[var]
	return ops[op](value(v1),value(v2))
	
for var in sorted(vars):
	if not var.startswith("z"): continue
	print(f"{var}: {value(var)}")
	