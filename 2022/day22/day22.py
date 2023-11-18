import re

width = 0
height = 0
m = []
rules = []

def load(filename):
    global width, height, m, rules
    with open(filename) as f:
        lines = [l.rstrip() for l in f.readlines()]
        si = lines.index("")
        maplines = lines[:si]
        ruleline = lines[si+1]

        height = len(maplines)
        width = max(len(line) for line in maplines)

        m = [l + " " * max(0, width - len(l)) for l in maplines]

        def tryint(s):
            try:
                return int(s)
            except:
                return s

        rules = [tryint(s) for s in re.findall(R"\d+|[RL]", ruleline)]
        

dirs = {
    "R": 0+1j,
    "L": 0-1j,
}

arrows = {
    ( 1, 0): ">",
    ( 0,-1): "^",
    (-1, 0): "<",
    ( 0, 1): "v"
}

score = {
    1+0j: 0,
    0+1j: 1,
    -1+0j: 2,
    0-1j: 3,
    
}

def debug(p = (1000,1000), walked = {}):
    for y in range(height):
        for x in range(width):
            if (x,y) == p:
                print("x", end='')
            elif (x,y) in walked:
                print(walked[(x,y)], end='')
            else:
                print(m[y][x], end='')

        print()
    
def part1():
    x,y = m[0].index("."),0
    d = 1+0j
    walked = {}

    for rule in rules:
        #print(x,y,rule)
        if isinstance(rule, int):
            for _ in range(rule):
                dx,dy = int(d.real),int(d.imag)
                x2,y2 = (x+dx) % width, (y+dy) % height

                while m[y2][x2] == " ":
                    x2,y2 = (x2+dx) % width, (y2+dy) % height

                if m[y2][x2] == "#":
                    break

                walked[(x,y)] = arrows[(dx,dy)]
                x,y = x2,y2

                # debug((x,y),walked)
                # print()
        else:
            d *= dirs[rule]

    print(1000*(y+1) + 4*(x+1) + score[d])


load("input.txt")
part1()

