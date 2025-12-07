import re

from math import floor,ceil

a,b,c = None,None,None
program = None

for line in open("../inputs/day17-real.txt"):
	if m := re.match(r"Register A: (\d+)",line): a = int(m.groups()[0])
	if m := re.match(r"Register B: (\d+)",line): b = int(m.groups()[0])
	if m := re.match(r"Register C: (\d+)",line): c = int(m.groups()[0])

	if m := re.match(r"Program: (.*)",line): 
		program = [int(n) for n in m.groups()[0].split(",")]
	
def trunc(x):
	if x < 0: return int(ceil(x))
	return int(floor(x))

def dis(prog):
	pc = 0
	while pc < len(prog):
		print(f"{pc:<2}: ", end='')
		op = prog[pc]
		lit = prog[pc+1]
		pc += 2

		match lit:
			case x if 0 <= x <= 3: 
				com = x

			case 4: com = "a"
			case 5: com = "b"
			case 6: com = "c"

			case 7: com = None

		match op:
			case 0: print(f"a <- a >> {com}")
			case 1: print(f"b <- b ^ {lit}")
			case 2: print(f"b <- {com} & 7")
			case 3: print(f"jnz {lit}")
			case 4: print(f"b <- b ^ c")
			case 5: print(f"out <- {com} & 7")
			case 6: print(f"b <- a >> {com}")
			case 7: print(f"c <- a >> {com}")
		


def run(a,b,c,prog):
	pc = 0
	out = []
	print(pc,":",a,b,c,out)
	while pc < len(prog):
		op = prog[pc]
		lit = prog[pc+1]
		com = None
		pc += 2

		match lit:
			case x if 0 <= x <= 3: 
				com = x

			case 4: com = a
			case 5: com = b
			case 6: com = c

			case 7: com = None

		match op:
			case 0: a = trunc(a / 2**com)
			case 1: b = b ^ lit
			case 2: b = com & 7
			case 3: pc = pc if a == 0 else lit
			case 4: b = b ^ c
			case 5: out.append(com & 7)
			case 6: b = trunc(a / 2**com)
			case 7: c = trunc(a / 2**com)
		
		print(pc,":",a,b,c,out)

	return out

dis(program)
#print(",".join(str(n) for n in run(a,b,c,program)))