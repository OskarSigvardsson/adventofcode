import re
from itertools import cycle
import math

with open("../inputs/day08-real.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]
    lrm = { "L": 0, "R": 1 }
    insts = [lrm[c] for c in lines[0]]
    m = {}
    
    for line in lines[2:]:
        s,l,r = re.match(r"(...) = \((...), (...)\)", line).groups()
        m[s] = (l,r)

    loc = "AAA"
    i = 0

    for inst in cycle(insts):
        i += 1
        loc = m[loc][inst]
        if loc == "ZZZ":
            break

    print("Part 1: {}".format(i))

with open("../inputs/day08-real.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]
    lrm = { "L": 0, "R": 1 }
    insts = [lrm[c] for c in lines[0]]
    m = {}
    
    for line in lines[2:]:
        s,l,r = re.match(r"(...) = \((...), (...)\)", line).groups()
        m[s] = (l,r)

    memo = {}
        
    def dist_to_z(start, ip):
        if (start, ip) in memo:
            return memo[(start, ip)]

        c = 0
        loc = start
        i = ip
        
        while loc[-1] != "Z":
            loc = m[loc][insts[i]]
            c += 1
            i = (i + 1) % len(insts)

        memo[(start,ip)] = c
        return c

    def advance(start, ip, count):
        if count == 0: return start

        if (start,ip,count) in memo:
            return memo[(start,ip,count)]

        loc = start
        ip2 = ip
        i = 0

        while i < count:
            loc = m[loc][insts[ip2]]
            ip2 = (ip2 + 1) % len(insts)
            i += 1

            memo[(start,ip2,count)] = loc

        return loc

    ghosts = [loc for loc in m.keys() if loc[-1] == "A"]
    ds = [dist_to_z(ghost, 0) for ghost in ghosts]

    # BAD SOLUTION THAT JUST HAPPENS TO WORK
    print(math.lcm(*[dist_to_z(ghost, 0) for ghost in ghosts]))

    # REAL SOLUTION. could be made much faster with clever optimizations, but
    # this works if you leave your computer on for a bit
    ip = 0
    count = 0
    p = 0

    while not all(ghost[-1] == "Z" for ghost in ghosts):
        adv = max(dist_to_z(ghost, ip) for ghost in ghosts)

        for i in range(len(ghosts)):
            ghosts[i] = advance(ghosts[i], ip, adv)

        ip = (ip + adv) % len(insts)
        count += adv

        p += 1
        if p % 1000000 == 0:
            print(count)
            
    print(count)

