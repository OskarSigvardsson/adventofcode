import re

insts = []

with open("../inputs/day18-real.txt", "r") as f:
    for line in f:
        m = re.match(R"^(.) (\d+) ..(......)", line.strip())
        d,l,rgb = m.groups()

        insts.append((d, int(l), rgb))

dirs = {
    'U': ( 0,  1),
    'D': ( 0, -1),
    'L': (-1,  0),
    'R': ( 1,  0),
}

def part1_input(insts):
    return [(d,l) for d,l,_ in insts]

def part2_input(insts):
    c = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }
    
    return [(c[rgb[-1]], int(rgb[:-1], 16)) for _,_,rgb in insts]


def count(insts):
    x1,y1 = 0,0

    # sum of the magitude of the bivectors/cross products of all edges.
    s = 0

    # length of boundary
    t = 0

    for c,l in insts:
        dx,dy = dirs[c]
        x2,y2 = x1 + dx*l, y1 + dy*l
        t += l

        # bivector/determinant formula
        s += x1*y2 - x2*y1

        x1,y1 = x2,y2

    # s is twice the answer, so divide over two (it's also the wrong sign)
    # t is part of the boundary that wasn't counted
    # and a plus one to account for the corners
    return int(-s/2 + t/2 + 1)

print(count(part1_input(insts)))
print(count(part2_input(insts)))


# initial thing i used for part 1, just flood fills the outside and counts that
# way. obviously doesn't work for part 2. left in for fun
def old():
    boundary = set()

    curr = (0,0)

    for d,l,_ in insts:
        dx,dy = dirs[d]
        for _ in range(l):
            x,y = curr
            curr = (x+dx,y+dy)
            boundary.add(curr)

    minx = min(x for x,_ in boundary) - 1
    miny = min(y for _,y in boundary) - 1
    maxx = max(x for x,_ in boundary) + 1
    maxy = max(y for _,y in boundary) + 1

    stack = [(minx,miny)]
    visited = set()

    while len(stack) > 0:
        x,y = stack.pop()

        if x not in range(minx,maxx+1) or y not in range(miny,maxy+1):
            continue

        if (x,y) in boundary:
            continue

        if (x,y) in visited:
            continue

        visited.add((x,y))

        stack.append((x+1,y))
        stack.append((x-1,y))
        stack.append((x,y+1))
        stack.append((x,y-1))


    area = (maxx - minx + 1) * (maxy - miny + 1)
    return area - len(visited)


