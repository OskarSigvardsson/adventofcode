import re

def parse():
    lines = [line.strip() for line in open("../inputs/day13-real.txt")]
    ba = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    bb = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    prize = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    i = 0

    while i < len(lines):
        a = tuple(int(n) for n in ba.match(lines[i]).groups())
        b = tuple(int(n) for n in bb.match(lines[i+1]).groups())
        p = tuple(int(n) for n in prize.match(lines[i+2]).groups())
        i += 4

        yield a,b,p

problems = list(parse())

def solve(a,b,t,adder):
    ax,ay = a
    bx,by = b
    tx,ty = t[0] + adder, t[1] + adder

    c1 = (tx*by - bx*ty) / (ax*by - ay*bx)
    c2 = (ty - c1*ay) / by

    if c1 == int(c1) and c2 == int(c2):
        return int(c1),int(c2)

    return None

p1 = sum(c[0]*3 + c[1] for c in (solve(a,b,p,0) for a,b,p in problems) if c)
p2 = sum(c[0]*3 + c[1] for c in (solve(a,b,p,10000000000000) for a,b,p in problems) if c)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")