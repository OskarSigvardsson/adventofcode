from functools import cache
from itertools import product

inputs = [line.strip() for line in open("../inputs/day21-test.txt")]

keypads = [
	[ "789",
	  "456",
	  "123",
	  ".0A", ],

	[ ".^A",
	  "<v>" ] 
]

coords = [{},{}]

for i in range(2):
	for x,y in product(range(len(keypads[i][0])),range(len(keypads[i]))):
		coords[i][keypads[i][y][x]] = (x,y)

def dist(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return abs(x2 - x1) + abs(y2 - y1)

@cache
def paths(kpi,k1,k2):
	p1 = coords[kpi][k1]
	p2 = coords[kpi][k2]

	ret = []

	if p1 == p2: 
		return [""]

	x1,y1 = p1
	ds = [(">",1,0),("^",0,-1),("<",-1,0),("v",0,1)]
	d1 = dist(p1,p2)

	for c,dx,dy in ds:
		pmx = x1+dx
		pmy = y1+dy
		pm = pmx,pmy

		if dist(pm,p2) >= d1: continue
		km = keypads[kpi][pmy][pmx]
		if km == ".": continue

		for path in paths(kpi,km,k2):
			ret.append(c + path)
		
	return ret
	

def move(kpi,dest,state):
	if len(state) == 0:
		return [dest], ""

	for path in paths(kpi,state[0],dest):
		inputs = []
		substate = state[1:]
		for c in path:
			keys, substate = move(1,c,substate)
			inputs.extend(keys)

		keys, substate = move(1, "A", substate)
		inputs.extend(keys)
		return inputs, dest + substate

def move2(kpi,dest,state):
	if len(state) == 0:
		return 1, ""

	best = float('inf')

	for path in paths(kpi,state[0],dest):
		presses = 0
		substate = state[1:]
		for c in path:
			subpresses, substate = move(1,c,substate)
			presses += subpresses

		subpresses, substate = move(1, "A", substate)
		presses += subpresses
		best = min(best, presses)
	
	return best

presses = 0
inputs,state = move(0,"0","AA")

print("".join(inputs))
print(state)

