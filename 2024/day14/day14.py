import re

from functools import reduce

robots = []
for line in open("../inputs/day14-real.txt"):
    px,py,vx,vy = [int(n) for n in re.match(r"p=(.*),(.*) v=(.*),(.*)", line).groups()]
    robots.append(((px,py),(vx,vy)))

w = 101
h = 103

def move(p,v):
    px,py = p
    vx,vy = v

    npx = (px + vx) % w
    npy = (py + vy) % h

    return (npx,npy),(vx,vy)

def quadrant(p):
    px,py = p
    if px < w//2 and py < h//2: return 1
    if px > w//2 and py < h//2: return 2
    if px < w//2 and py > h//2: return 3
    if px > w//2 and py > h//2: return 4
    return 0

def display(robots):
    ps = set(p for p,_ in robots)

    for y in range(h):
        for x in range(w):
            print('#' if (x,y) in ps else '.', end='')
        print()

def part1(robots):
    for step in range(100):
        for i in range(len(robots)):
            robots[i] = move(*robots[i])

    quadrants = [0,0,0,0,0]

    for p,_ in robots:
        quadrants[quadrant(p)] += 1

    print("Part 1:", reduce(lambda x,y:x*y, quadrants[1:]))

def part2(robots):
    gen = 0
    while True:
        # MAGIC NUMBERS!
        candidate = (gen - 14) % 101 == 0
        if candidate:
            print(gen)
            print("-"*100)
            display(robots)
            print("-"*100)

        for i in range(len(robots)):
            robots[i] = move(*robots[i])

        gen += 1
        if candidate:
            input("")

part1(robots[:])
part2(robots[:])