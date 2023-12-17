from heapq import heappush,heappop

m = []

with open("../inputs/day17-real.txt", "r") as f:
    m = [[int(c) for c in line.strip()] for line in f]

w = len(m[0])
h = len(m)

left = 0+1j
right = 0-1j

goal = (w-1) + (h-1)*1j

def cost(p):
    return m[int(p.imag)][int(p.real)]

def from_tuple(p):
    return p[0]+p[1]*1j

def to_tuple(p):
    return (p.real,p.imag)

def bounds_check(p):
    return p.real in range(w) and p.imag in range(h)

def part1():
    pq = []
    visited = {}
    heappush(pq, (0, (0,0), (1,0), 1))
    heappush(pq, (0, (0,0), (0,1), 1))
    while len(pq) > 0:
        s,p,d,r = heappop(pq)

        p = from_tuple(p)
        d = from_tuple(d)

        if r > 3:
            continue
        if (p,d,r) in visited:
            continue

        visited[(p,d,r)] = s

        if p == goal:
            return s

        d2 = d * left
        p2 = p + d2
        if bounds_check(p2):
            heappush(pq, (s + cost(p2),to_tuple(p2),to_tuple(d2),1))

        d3 = d * right
        p3 = p + d3
        if bounds_check(p3):
            heappush(pq, (s + cost(p3),to_tuple(p3),to_tuple(d3),1))

        p4 = p + d
        if bounds_check(p4):
            heappush(pq, (s + cost(p4),to_tuple(p4),to_tuple(d),r + 1))


def part2():
    pq = []
    visited = {}
    prev = {}

    heappush(pq, (0, (0,0), (1,0), 1))
    heappush(pq, (0, (0,0), (0,1), 1))

    while len(pq) > 0:
        s,p,d,r = heappop(pq)

        p = from_tuple(p)
        d = from_tuple(d)

        if (p,d,r) in visited:
            continue

        visited[(p,d,r)] = s

        if p == goal and r > 3:
            return s

        d2 = d * left
        p2 = p + d2
        if r > 3 and bounds_check(p2):
            heappush(pq, (s + cost(p2),to_tuple(p2),to_tuple(d2),1))

        d3 = d * right
        p3 = p + d3
        if r > 3 and bounds_check(p3):
            heappush(pq, (s + cost(p3),to_tuple(p3),to_tuple(d3),1))

        p4 = p + d
        if r < 10 and bounds_check(p4):
            heappush(pq, (s + cost(p4),to_tuple(p4),to_tuple(d),r + 1))


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")


