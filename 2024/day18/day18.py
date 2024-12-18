import heapq

coords = []

for line in open("../inputs/day18-real.txt"):
    x,y = [int(n) for n in line.strip().split(",")]
    coords.append((x,y))

w = 71
h = 71

def part1(coords):
    frontier = [(0,(0,0),None)]
    visited = set()
    ex,ey = w-1,h-1
    prevMap = {}

    while len(frontier) > 0:
        s,p,prev = heapq.heappop(frontier)
        x,y = p

        if x not in range(w) or y not in range(h):
            continue

        c = "#" if p in coords else "."

        if c == "#": continue
        if p in visited: continue

        if p == (ex,ey): 
            path = [(ex,ey)]

            while prev is not None:
                path.append(prev)
                prev = prevMap[prev]

            return set(path)

        visited.add(p)
        prevMap[p] = prev

        heapq.heappush(frontier, (s+1,(x+1,y  ), p))
        heapq.heappush(frontier, (s+1,(x-1,y  ), p))
        heapq.heappush(frontier, (s+1,(x  ,y+1), p))
        heapq.heappush(frontier, (s+1,(x  ,y-1), p))

    return None

def part2(coords):
    coordSet = set()
    p1 = part1(coordSet)
    i = 0

    while p1 is not None:
        while coords[i] not in p1:
            coordSet.add(coords[i])
            i += 1

        coordSet.add(coords[i])
        i += 1

        p1 = part1(coordSet)

        if p1 is None: return coords[i-1]

p1 = len(part1(set(coords[:1024]))) - 1
p2 = part2(coords) 

print(f"Part 1: {p1}")
print(f"Part 2: {p2[0]},{p2[1]}")