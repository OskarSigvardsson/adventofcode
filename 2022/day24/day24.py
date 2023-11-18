from collections import defaultdict, deque

start = []

blizz = []
maps = []

w = 0
h = 0

dirs = {
    ">": (1,0),
    "^": (0,-1),
    "<": (-1,0),
    "v": (0,1),
}

idirs = {v:k for k,v in dirs.items()}


def load(filename):
    global blizz, w, h
    start = []

    with open(filename) as f:
        for y,line in ((i,line.strip()) for i,line in enumerate(f)):
            if y == 0:
                continue
            if line[1] == "#":
                h = y + 1
                continue
            
            w = len(line)
            
            for x,c in enumerate(line):
                if c in ">^<v":
                    start.append((x,y,c))

    start.sort()
    blizz.append(start)
    maps.append(set((x,y) for x,y,_ in start))

    # nb = step(start)

    # while nb != blizz[0]:
    #     blizz.append(nb)
    #     maps.append(set((x,y) for x,y,_ in nb))
    #     nb = step(nb)

    #     if len(blizz) > 50:
    #         break

def get_map(i):
    while i >= len(blizz):
        blizz.append(step(blizz[-1]))

    while i >= len(maps):
        maps.append(set((x,y) for x,y,_ in blizz[len(maps)]))

    return maps[i]


def debug(blizz, px=-1, py=-1):
    m = defaultdict(list)

    for (x,y,c) in blizz:
        m[(x,y)].append(c)

    for y in range(0, h):
        for x in range(0, w):
            c = "!"
            
            if x == px and y == py:
                c = "E"
            elif y == 0 and x != 1:
                c = "#"
            elif y == h-1 and x != w-2:
                c = "#"
            elif x == 0 or x == w-1:
                c = "#"
            elif len(m[(x,y)]) == 0:
                c = '.'
            elif len(m[(x,y)]) == 1:
                c = m[(x,y)][0]
            elif len(m[(x,y)]) > 1:
                c = len(m[(x,y)])

            print(c, end='')
        print()
    print()
    
def step(blizz):
    newblizz = []

    for x,y,c in blizz:
        dx,dy = dirs[c]
        nx,ny = x+dx,y+dy

        if ny == 0:
            ny = h-2
        elif ny == h-1:
            ny = 1
        elif nx == 0:
            nx = w-2
        elif nx == w-1:
            nx = 1

        newblizz.append((nx,ny,c))

    newblizz.sort()
    return newblizz

def inside(x,y):
    if (x,y) == (1,0):
        return True
    if (x,y) == (w-2,h-1):
        return True

    return x in range(1,w-1) and y in range(1,h-1)

def search(rnd, start, dest):
    queue = deque([(rnd,start,None)])
    
    visited = set()
    prev = {}
    
    final = None
    
    while len(queue) > 0:
        rnd,(x,y),p = queue.popleft()

        if (rnd,(x,y)) in visited:
            continue

        visited.add((rnd,(x,y)))

        prev[(rnd,(x,y))] = p
        
        if (x,y) == dest:
            print("hit!", rnd)
            final = rnd,(x,y)
            break

        nrnd = rnd+1
        #m = maps[nrnd % len(maps)]
        m = get_map(nrnd)
        
        for dx,dy in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
            nx,ny = x+dx,y+dy

            if inside(nx,ny) and (nx,ny) not in m:
                queue.append((nrnd,(nx,ny),(rnd,(x,y))))

    # states = []
    # curr = final

    # while curr is not None:
    #     states.append(curr)
    #     curr = prev[curr]

    # states.reverse()

    # px,py = 0,0

    # for rnd,(x,y) in states:
    #     print(rnd,(px,py),(x,y))
    #     debug(blizz[rnd % len(blizz)], x, y)
    #     assert(abs(x-px) + abs(y-py) <= 1)
    #     assert((x,y) not in maps[rnd % len(maps)])
    #     px,py = x,y
        
    return final[0]

load("input.txt")
rnd = search(0, (1,0), (w-2,h-1))
rnd = search(rnd, (w-2,h-1), (1,0))
rnd = search(rnd, (1,0), (w-2,h-1))
