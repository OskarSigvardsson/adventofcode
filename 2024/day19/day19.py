from functools import cache

towels,lines = [],[]

with open("../inputs/day19-real.txt") as f:
    towels = [towel for towel in f.readline().split(", ")]
    f.readline()
    lines = [line.strip() for line in f]

@cache
def options(line):
    if line == "": return 1

    return sum(options(line[len(t):]) for t in towels if line.startswith(t))

p1 = sum(options(line) != 0 for line in lines)
p2 = sum(options(line) for line in lines)

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")