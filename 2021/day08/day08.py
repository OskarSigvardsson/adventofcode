from itertools import chain

with open("input.txt", "r") as f:
    data = [
        (l.strip().split(" "), r.strip().split(" "))
        for l,r in (line.split("|") for line in f)
    ]

def part1(data):
    return sum(1 for x in chain(*(out for _,out in data)) if len(x) in [2,3,4,7])
        

print(f"Part 1: { part1(data) }")
