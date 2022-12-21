import z3
import re

s = z3.Solver()

ops = {
    "=": lambda x,y: x==y,
    "+": lambda x,y: x+y,
    "-": lambda x,y: x-y,
    "*": lambda x,y: x*y,
    "/": lambda x,y: x/y,
}

monkeys = {}

with open("input.txt") as f:
    for line in f:
        if m := re.match(R"(.*): (.*) (.) (.*)", line):
            monkeys[m.group(1)] = list(m.groups()[1:])
        elif m := re.match(R"(.*): (\d+)", line):
            monkeys[m.group(1)] = int(m.group(2))
            
vrs = { var: z3.Int(var) for var in monkeys.keys() }
del monkeys["humn"]

for var,val in monkeys.items():
    if isinstance(val, int):
        s.add(vrs[var] == val)
    elif var != "root":
        v1,op,v2 = val
        s.add(vrs[var] == ops[op](vrs[v1], vrs[v2]))

v1,_,v2 = monkeys["root"]
s.add(vrs[v1] == vrs[v2])

sat = s.check()
model = s.model()

print(model[vrs["humn"]])
