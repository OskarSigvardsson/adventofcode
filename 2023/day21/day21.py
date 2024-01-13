m = []

with open("../inputs/day21-real.txt", "r") as f:
    m = [list(line.strip()) for line in f]

w,h = len(m[0]),len(m)

sx,sy = None, None

for y,row in enumerate(m):
    for x,c in enumerate(row):
        if c == "S":
            sx,sy = x,y
            m[y][x] = "."
            break

assert(sx)
assert(sy)
assert(w == h)

def part1(steps):
    ps1 = set([(sx,sy)])
    ps2 = set()

    for _ in range(steps):
        for x,y in ps1:
            for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                x2,y2 = x+dx,y+dy

                if x2 not in range(w) or y2 not in range(h):
                    continue

                if m[y2][x2] == "#":
                    continue

                ps2.add((x2,y2))


        # swap here is a bit overkill, you could just create new ones every iteration
        ps1,ps2 = ps2,ps1
        ps2.clear()

    return len(ps1)

print(f"Part 1: {part1(64)}")

def seed_values():
    ps1 = set([(sx,sy)])
    ps2 = set()
    l1 = [1]
    l2 = [0]
    l3 = [0]

    i = 0
    while True:
        for x,y in ps1:
            for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                x2,y2 = x+dx,y+dy

                xi,yi = x2%w,y2%h

                if m[xi][yi] == "#":
                    continue

                ps2.add((x2,y2))

        ps1,ps2 = ps2,ps1
        ps2.clear()

        i += 1

        l1.append(len(ps1))

        if len(l1) > w:
            l2.append(l1[-1] - l1[-w - 1])
        else:
            l2.append(0)

        l3.append(l2[-1] - l2[-2])
                  
        if len(l3) > w and l3[-w:] == l3[-2*w:-w]:
            break
            
    return l1,l2,l3

def part2(steps):
    l1,l2,l3 = seed_values()

    for i in range(len(l1), steps+1):
        l3.append(l3[-w])
        l2.append(l2[-1] + l3[-1])
        l1.append(l1[-w] + l2[-1])

        # if i in [6,10,50,100,500,1000,5000,steps]:
        #     print(i,l1[-1])

    return l1[-1]

print(f"Part 2: {part2(26501365)}")
