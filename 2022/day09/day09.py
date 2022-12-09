lines = []
dirs = {
    "R": (1,0),
    "U": (0,1),
    "L": (-1,0),
    "D": (0,-1)
}

with open("input.txt") as f:
    for line in f:
        d,c = line.split();
        lines.append((d, int(c)))

def sign(x):
    if x == 0: return 0
    if x > 0: return 1
    if x < 0: return -1

def step(dx,dy,hx,hy,tx,ty):
    hx2,hy2 = hx+dx,hy+dy

    dx2,dy2 = hx2-tx,hy2-ty

    d = dx2**2 + dy2**2

    if d <= 2:
        return hx2,hy2,tx,ty

    return hx2,hy2,tx+sign(dx2),ty+sign(dy2)

def part1():
    visited = set([(0,0)])
    hx,hy,tx,ty = 0,0,0,0
    
    for (d,c) in lines:
        dx,dy = dirs[d]

        for _ in range(c):
            hx,hy,tx,ty = step(dx,dy,hx,hy,tx,ty)
            visited.add((tx,ty))

    return len(visited)

    
def part2():
    visited = set([(0,0)])
    rope = [(0,0)] * 10

    for (d,c) in lines:
        for _ in range(c):
            dx,dy = dirs[d]
            hx,hy = rope[0]

            for i in range(9):
                hx,hy = rope[i]
                tx,ty = rope[i+1]

                hx2,hy2,tx2,ty2 = step(dx,dy,hx,hy,tx,ty)

                rope[i] = (hx2,hy2)

                dx,dy = tx2-tx,ty2-ty

            rope[-1] = (hx+dx,hy+dy)

            visited.add(rope[-1])

    return len(visited)


print(part1())
print(part2())
