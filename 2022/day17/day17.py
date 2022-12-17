from itertools import count

pieces = [
    "####",

    ".#.\n"
    "###\n"
    ".#.",

    "..#\n"
    "..#\n"
    "###",

    "#\n"
    "#\n"
    "#\n"
    "#",

    "##\n"
    "##"
]

for i in range(len(pieces)):
    m = []
    height = pieces[i].count("\n")

    for y,line in enumerate(pieces[i].split("\n")):
        for x,c in enumerate(line):
            if c == "#":
                m.append((x,height - y))

    pieces[i] = m

def load(filename):
    global inst
    
    with open("input.txt") as f:
        m = {"<": -1, ">": 1}
        inst = [m[c] for c in f.readline().strip()]


def debug(field):
    maxy = field_height(field)

    def d(s):
        print(s, end='')
        
    for y in range(maxy, -2, -1):
        for x in range(-1,8):
            if x == -1 or x == 7:
                d("|")
            elif y == -1:
                d("-")
            elif (x,y) in field:
                d("#")
            else:
                d(" ")
        print()

    print()

def outside(p):
    return (   any(x >= 7 for x,_ in p)
            or any(x  < 0 for x,_ in p)
            or any(y  < 0 for _,y in p))

def collide(p, field):
    return any(c in field for c in p)

def field_height(field):
    return -1 if len(field) == 0 else max(y for _,y in field)

def drop(piece, field, ii):
    p = [(x + 2, y + field_height(field) + 4) for x,y in piece]

    while True:
        dx = inst[ii]
        ii = (ii + 1) % len(inst)

        p2 = [(x+dx,y) for x,y in p]

        if not outside(p2) and not collide(p2, field):
            p = p2


        p2 = [(x,y-1) for x,y in p]

        if outside(p2) or collide(p2, field):
            return ii, field | frozenset(p)

        p = p2

def mold(field):
    maxy = field_height(field)

    x,y = 0,maxy+1
    fill = [(x,y)]
    flood = set((x,y))
    bottom = y
        
    while len(fill) > 0:
        fx,fy = fill.pop()
        flood.add((fx,fy))
        bottom = min(bottom, fy)
        
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            x,y = fx+dx,fy+dy

            if y < 0: continue
            if y > maxy+1: continue
            if x < 0: continue
            if x >= 7: continue

            p = x,y
            
            if p in field: continue
            if p in flood: continue

            fill.append(p)

    molded = []
    
    for x in range(0,8):
        for y in range(0, maxy+1):
            if y >= bottom and (x,y) in field or (x,y) not in flood:
                molded.append((x,y - bottom))

    return frozenset(molded), bottom

memo = {}
def drop2(rnd, maxrnd, ii, field):
    pi = rnd % len(pieces)

    opi = pi
    oii = ii
    ofield = field
    skips = 0
    bottom = 0

    while (pi, ii, field) in memo:
        #print(skips, pi,ii,len(field))
        dr,ii2,field2,nb = memo[(pi, ii, field)]

        if rnd + skips + dr >= maxrnd:
            break
        
        ii = ii2
        field = field2
        bottom += nb
        skips += dr

        pi = (pi + dr) % len(pieces)


    if skips > 0:
        memo[(opi, oii, ofield)] = (skips,ii,field,bottom)
        return rnd+skips,ii,field,bottom
              
    ii,nf = drop(pieces[opi], ofield, oii)
    mf,nb = mold(nf)

    memo[(opi,oii,ofield)] = (1,ii,mf,nb)
    
    return rnd+1, ii, mf, nb

def run(ii, rounds):
    rnd = 0
    ii = 0
    bottom = 0
    
    field = frozenset()

    while rnd < rounds:
        rnd,ii,field,nb = drop2(rnd, min(rounds, rnd+100000000), ii, field)
        print(rnd, rnd/rounds)
        bottom += nb
        #print(bottom)
        #debug(field)

    return bottom + field_height(field) + 1


load("input.txt")
f1 = run(0, 1000000000000)

print(f1)
# print(part1("test.txt", 5))
# print("--------------")

