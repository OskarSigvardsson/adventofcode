import re
import z3

from fractions import Fraction
from itertools import combinations

hails = []

with open("../inputs/day24-real.txt", "r") as f:
    num = R" *(-?\d+)"
    pattern = f"{num}, {num}, {num} @ {num}, {num}, {num}"
    matches = [re.match(pattern, line) for line in f]
    hails = [tuple(Fraction(n) for n in m.groups()) for m in matches]



def intersect2d(h1, h2):
    x1p,y1p,_,x1v,y1v,_ = h1
    x2p,y2p,_,x2v,y2v,_ = h2

    if x1v*y2v - x2v*y1v == 0:
        return None
    
    # thank you built-in Emacs computer algebra system!
    t1 = (y2v*(x1p - x2p) / x2v + y2p - y1p) / (y1v - x1v*y2v / x2v)
    t2 = (y2p - y1p - y1v*(x2p - x1p) / x1v) / (x2v*y1v / x1v - y2v)

    return (t1, t2, x2p + t2*x2v, y2p + t2*y2v)

def part1(minc, maxc):
    isects = (isect for isect in (intersect2d(h1,h2) for h1,h2 in combinations(hails, 2)) if isect)
    isects = ((x,y) for (t1,t2,x,y) in isects if t1 >= 0 and t2 >= 0)
    count = sum(1 for x,y in isects if minc <= x <= maxc and minc <= y <= maxc)

    return count

def part2():
    # thank you, Microsoft Research!
    x1p,y1p,z1p,x1v,y1v,z1v = [int(n) for n in hails[0]]
    x2p,y2p,z2p,x2v,y2v,z2v = [int(n) for n in hails[1]]
    x3p,y3p,z3p,x3v,y3v,z3v = [int(n) for n in hails[2]]

    # 9 variables...
    x0p = z3.Int('x0p')
    y0p = z3.Int('y0p')
    z0p = z3.Int('z0p')
    x0v = z3.Int('x0v')
    y0v = z3.Int('y0v')
    z0v = z3.Int('z0v')
    t1 = z3.Int('t1')
    t2 = z3.Int('t2')
    t3 = z3.Int('t3')

    s = z3.Solver()
    
    # 9 equations...
    # if a solution exist, this should be all we need, and z3 should be able to find it
    s.add(x1p + t1*x1v == x0p + t1*x0v)
    s.add(y1p + t1*y1v == y0p + t1*y0v)
    s.add(z1p + t1*z1v == z0p + t1*z0v)
    s.add(x2p + t2*x2v == x0p + t2*x0v)
    s.add(y2p + t2*y2v == y0p + t2*y0v)
    s.add(z2p + t2*z2v == z0p + t2*z0v)
    s.add(x3p + t3*x3v == x0p + t3*x0v)
    s.add(y3p + t3*y3v == y0p + t3*y0v)
    s.add(z3p + t3*z3v == z0p + t3*z0v)

    # crank it, z3!
    s.check()
    m = s.model()
    #print(m)
    return sum(m[v].as_long() for v in [x0p,y0p,z0p])

p1 = part1(200000000000000, 400000000000000)
p2 = part2()

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
