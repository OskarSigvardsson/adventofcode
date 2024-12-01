import re

from collections import Counter

ns = [[int(n) for n in re.match(r"(\d+) +(\d+)", line).groups()] for line in open("../inputs/day01-real.txt")]

# matrix transpose
ns1,ns2 = list(zip(*ns))

s1 = sorted(ns1)
s2 = sorted(ns2)

p1 = sum(abs(a - b) for a,b in zip(s1,s2))

print(f"Part 1: {p1}")

# using python is cheating! 
counts = Counter(ns2)

p2 = sum(n * counts[n] for n in ns1)

print(f"Part 2: {p2}")