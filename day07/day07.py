import math

with open("input.txt", "r") as f:
    ns = [int(n) for n in f.readline().strip().split(',')]

    mn,mx = min(ns), max(ns)
    fuel = math.inf

    for p in range(mn, mx + 1):
        fuel = min(fuel, sum(abs(p - n) for n in ns))

    print(f"Part 1: { fuel }")

    def tri(n):
        return int((n * (n + 1)) / 2)

    fuel = math.inf

    for p in range(mn, mx + 1):
        fuel = min(fuel, sum(tri(abs(p - n)) for n in ns))

    print(f"Part 2: { fuel }")

