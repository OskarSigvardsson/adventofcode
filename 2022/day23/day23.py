from collections import defaultdict
from itertools import product, count

def load(filename):
    with open(filename) as f:
        elves = set()
        
        for y,line in enumerate(f):
            for x,c in enumerate(line):
                if c == "#":
                    elves.add((x,y))

        return elves
    
def debug(elves):
    minx = min(x for x,_ in elves) - 1
    maxx = max(x for x,_ in elves) + 1
    miny = min(y for _,y in elves) - 1
    maxy = max(y for _,y in elves) + 1

    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            print("#" if (x,y) in elves else ".", end='')
        print()
    print()

dirs = [
    ((0,-1),(-1,-1),(1,-1)),
    ((0,1),(-1,1),(1,1)),
    ((-1,0),(-1,-1),(-1,1)),
    ((1,0),(1,-1),(1,1))
]

def step(elves, rnd):
    dests = defaultdict(list)
    props = {}
    
    stay = set()
    
    for x,y in elves:

        alone = not any((x+dx,y+dy) in elves
                    for dx,dy in
                    product(range(-1,2),range(-1,2))
                    if (dx,dy) != (0,0))

        if alone:
            # print(f"elf {(x,y)} is alone")
            stay.add((x,y))
            continue

        for i in range(4):
            d1,d2,d3 = dirs[(rnd + i) % 4]

            good = not any((x+dx,y+dy) in elves for (dx,dy) in [d1,d2,d3])

            if good:
                dx,dy = d1
                dests[(x+dx,y+dy)].append((x,y))
                props[(x,y)] = (x+dx,y+dy)
                # print(f"elf {(x,y)} proposes {props[(x,y)]}")
                break
        else:
            stay.add((x,y))
            # print(f"elf {(x,y)} is stuck")

    newelves = set()
    
    for x,y in elves:
        if (x,y) in stay: 
            # print(f"elf {(x,y)} stays")
            newelves.add((x,y))
        elif len(dests[props[(x,y)]]) == 1:
            # print(f"elf {(x,y)} goes to {props[(x,y)]}")
            newelves.add(props[(x,y)])
        else:
            # print(f"elf {(x,y)} clashes, stays put")
            newelves.add((x,y))
    
    return newelves

def score(elves):
    minx = min(x for x,_ in elves)
    maxx = max(x for x,_ in elves)
    miny = min(y for _,y in elves)
    maxy = max(y for _,y in elves)

    return (maxx-minx+1) * (maxy-miny+1) - len(elves)
    
elves = load("input.txt")

for i in range(10):
    elves = step(elves, i)

print(score(elves))

elves = load("input.txt")
for i in count(0):
    newelves = step(elves, i)
    if elves == newelves:
        print(i + 1)
        break
    elves = newelves
