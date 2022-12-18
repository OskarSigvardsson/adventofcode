import re

def parse(filename):
    sensors = []

    with open(filename) as f:
        for line in f:
            sensors.append(tuple(int(s) for s in re.findall(R"(-?\d+)", line)))

    return sensors

def line_events(y, sensors):
    line = []

    for (sx,sy,bx,by) in sensors:
        d = abs(sx-bx) + abs(sy-by)
        dy = abs(sy-y)

        if dy <= d:
            sx1 = sx - (d-dy)
            sx2 = sx + (d-dy)

            line.append((sx1, -1))
            line.append((sx2, 1))

    return sorted(line)

def part1(y, filename):
    line = line_events(y, parse(filename))
    s = 0
    d = 0
    px = line[0][0]

    for (x,t) in sorted(line):
        if d < 0 and px < x:
            s += x - px
            px = x

        d += t 

    return s

def part2(y1, y2, filename):
    sensors = parse(filename)

    for y in range(y1,y2+1):
        line = line_events(y, sensors)

        px = line[0][0]
        d = 0
        
        for (x,t) in sorted(line):
            if d == 0 and px + 1 < x:
                return (px + 1) * 4000000 + y

            px = x
            d += t


print(part1(10, "test.txt"))
print(part1(2000000, "input.txt"))
print(part2(0,20,"test.txt"))
print(part2(0,4000000,"input.txt"))
