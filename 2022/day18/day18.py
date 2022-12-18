from itertools import product

def load(filename):
    global lines
    with open(filename) as f:
        lines = [tuple(int(c) for c in s.strip().split(",")) for s in f]


def surface():
    xs = set()
    ys = set()
    zs = set()

    def add(s,c):
        if c in s:
            s.remove(c)
        else:
            s.add(c)
            
    for (x,y,z) in lines:
        add(xs, (x,y,z))
        add(xs, (x+1,y,z))
        add(ys, (x,y,z))
        add(ys, (x,y+1,z))
        add(zs, (x,y,z))
        add(zs, (x,y,z+1))

    return xs,ys,zs

def limits():
    return (
        (min(x for x,_,_ in lines), max(x for x,_,_ in lines)),
        (min(y for _,y,_ in lines), max(y for _,y,_ in lines)),
        (min(z for _,_,z in lines), max(z for _,_,z in lines)))

def part2():
    volume = set(lines)
    xs,ys,zs = surface()

    xl,yl,zl = limits()

    xmin,xmax = xl
    ymin,ymax = yl
    zmin,zmax = zl

    flood = []
    fill = set()

    for y,z in product(range(ymin,ymax+1),range(zmin,zmax+1)):
        flood.append((xmin-1, y, z))
        flood.append((xmax+1, y, z))

    for x,z in product(range(xmin,xmax+1),range(zmin,zmax+1)):
        flood.append((x, ymin-1, z))
        flood.append((x, ymax+1, z))

    for x,y in product(range(xmin,xmax+1),range(ymin,ymax+1)):
        flood.append((x, y, zmin-1))
        flood.append((x, y, zmax+1))

    def inside(x,y,z):
        return (
            x in range(xmin,xmax+1) and
            y in range(ymin,ymax+1) and
            z in range(zmin,zmax+1)
        )

    origlen = len(xs) + len(ys) + len(zs)
    
    def remove(s, v):
        try:
            s.remove(v)
        except KeyError:
            pass
        
    while len(flood) > 0:
        p = flood.pop()
        x,y,z = p

        if p in fill or p in volume:
            continue

        fill.add((x,y,z))

        remove(xs, (x,y,z))
        remove(xs, (x+1,y,z))
        remove(ys, (x,y,z))
        remove(ys, (x,y+1,z))
        remove(zs, (x,y,z))
        remove(zs, (x,y,z+1))

        for (dx,dy,dz) in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            nx,ny,nz = x+dx,y+dy,z+dz

            if inside(nx,ny,nz):
                flood.append((nx,ny,nz))

    afterlen = len(xs) + len(ys) + len(zs)

    return origlen - afterlen

load("input.txt")
print(part2())
# print(sum(len(s) for s in surface()))
# print(limits())
