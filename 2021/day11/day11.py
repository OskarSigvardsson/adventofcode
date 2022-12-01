from itertools import count


def step(m, w, h):
    flashes = 0
    # not sure if this stack business is needed...
    stack = []

    for x,y in ((x,y) for x in range(w) for y in range(h)):
        m[y][x] += 1

        if m[y][x] >= 10:
            stack.append((x,y))

    while len(stack) > 0:
        x,y = stack.pop()

        if x < 0 or y < 0 or x >= w or y >= h:
            continue

        if m[y][x] == 0:
            continue

        m[y][x] += 1

        if m[y][x] >= 10:
            m[y][x] = 0
            flashes += 1

            for dx,dy in ((dx,dy) for dx in range(-1,2) for dy in range(-1,2)):
                stack.append((x+dx, y+dy))

    return flashes


def part1(m, steps):
    w, h = len(m[0]), len(m)

    flashes = 0

    for s in range(steps):
        flashes += step(m, w, h)

    return flashes
    

def part2(m):
    w, h = len(m[0]), len(m)

    for s in count(1):
        flashes = step(m, w, h)
        
        if flashes == w*h:
            return s
    

with open("input.txt", "r") as f:
    m = [[int(c) for c in line.strip()] for line in f]

    # these are modified in place. so copy them. i guess you don't have to copy
    # one of them, but it's nicer this way :) 
    m1 = [line[:] for line in m]
    m2 = [line[:] for line in m]
    
    print(f"Part 1: { part1(m1, 100) }")
    print(f"Part 2: { part2(m2)      }")

