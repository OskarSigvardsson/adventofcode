import re
import numpy as np

from numpy.linalg import det, inv
from itertools import permutations, combinations, product

def rotation_mats():
    signs = [
        ( 1, 1, 1),
        ( 1, 1,-1),
        ( 1,-1, 1),
        ( 1,-1,-1),
        (-1, 1, 1),
        (-1, 1,-1),
        (-1,-1, 1),
        (-1,-1,-1)]
    
    mats = []
    for c1,c2,c3 in permutations(np.eye(3)):
        for s1,s2,s3 in signs:
            m = np.column_stack((s1*c1, s2*c2, s3*c3))

            if det(m) > 0:
                yield m

def rotate(scanner):
    for mat in rotation_mats():
        vs = [b @ mat for b in scanner]
        yield vs

def pairs(it):
    for a,b in combinations(it, 2):
        yield a,b
        
def fit(s1, s2):

    d1s = [s1b2 - s1b1 for s1b1,s1b2 in pairs(s1)]
    d2s = [s2b2 - s2b1 for s2b1,s2b2 in pairs(s2)]

    # this is a heuristic, i'm not entirely sure it's always valid, but you'd
    # have to craft some very evil input for it not to be
    if intersections(d1s, d2s) < 12:
        return None

    for s1b1, s1b2 in pairs(s1):
        d1 = s1b2 - s1b1
        
        for s2b1, s2b2 in pairs(s2):
            d2 = s2b2 - s2b1

            if all(np.equal(d1, d2)):
                s2l = s1b1 - s2b1
                trans = [b + s2l for b in s2]

                if intersections(s1, trans) >= 12:
                    return s2l

    return None

def intersections(s1, s2):
    s1s = set(tuple(v) for v in s1)
    s2s = set(tuple(v) for v in s2)

    return len(s1s.intersection(s2s))

def manhattan(d1, d2):
    return sum(abs(c1-c2) for c1,c2 in zip(d1,d2))

with open("input.txt", "r") as f:
    scanners = [] 
    scanner = []
   
    for line in f:
        line = line.strip()

        if line == "":
            scanners.append(scanner)
            scanner = []

        if m := re.match(R"^(-?\d+),(-?\d+),(-?\d+)$", line):
            scanner.append(np.array([float(g) for g in m.groups()]))
        
    scanners.append(scanner)

    deltas = {0: np.zeros(3)}
    nomatch = set()

    while len(deltas) < len(scanners):
        found = False
        print(sorted(list(deltas.keys())))

        for i1,s1 in enumerate(scanners):
            if i1 not in deltas:
                continue

            for i2,s2 in enumerate(scanners):
                if i2 in deltas:
                    continue

                if (i1,i2) in nomatch:
                    continue

                for rot in rotate(s2):
                    if (d := fit(s1, rot)) is not None:
                        deltas[i2] = deltas[i1] + d
                        scanners[i2] = rot

                        found = True
                        break
                else:
                    nomatch.add((i1,i2))

                if found: break


    beacons = set()

    for i,s in enumerate(scanners):
        d = np.array(deltas[i])

        for b in s:
            beacons.add(tuple(d + np.array(b)))

    print(len(beacons))
    print(max(manhattan(d1, d2) for d1,d2 in combinations(deltas.values(), 2)))
