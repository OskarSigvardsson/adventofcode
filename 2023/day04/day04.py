import re
from collections import defaultdict
from itertools import product

with open("../inputs/day04-real.txt") as f:
    ns = [tuple(set(int(s) for s in re.findall("\d+", part)) for part in line.split(":")[1].split("|")) for line in f]
    common = [len(a & b) for a,b in ns]
    scores = [0 if c == 0 else 2**(c-1) for c in common]

    print("Part 1: {}".format(sum(scores)))

    counts = [1] * len(ns)

    for i in range(len(counts)):
        for j in range(common[i]):
            counts[i+j+1] += counts[i]

    print("Part 2: {}".format(sum(counts)))
