import re
from collections import Counter, defaultdict
from itertools import islice

def part1(polymer, rules, generations):
    for _ in range(generations):
        new_polymer = []

        for c1,c2 in zip(polymer, islice(polymer, 1, None)):
            new_polymer.append(c1)
            new_polymer.append(rules[c1 + c2])

        new_polymer.append(polymer[-1])
        polymer = new_polymer

    counts = Counter(polymer).most_common()

    return counts[0][1] - counts[-1][1]

def dictsum(*dicts):
    s = defaultdict(lambda: 0)

    for d in dicts:
        for k,v in d.items():
            s[k] += v

    return s
        
def part2(polymer, rules, generations):
    memo = {}
    
    # Function that returns the counts of all the elements between two elements.
    # The function is memoized: this is a Dynamic Programming problem: the
    # recursions overlap
    def polycount(c1, c2, gens):
        if gens == 0:
            return { }

        if (c1,c2,gens) in memo:
            return memo[(c1,c2,gens)]

        cm = rules[c1 + c2]

        result = dictsum(
            { cm: 1 },
            polycount(c1, cm, gens - 1),
            polycount(cm, c2, gens - 1))

        memo[(c1,c2,gens)] = result

        return result

    total = {}

    for c1,c2 in zip(polymer, islice(polymer, 1, None)):
        cs = polycount(c1,c2,generations)
        total = dictsum(total, polycount(c1,c2,generations))

    counter = Counter(total)
    counter.update(polymer)

    counts = counter.most_common()

    return counts[0][1] - counts[-1][1]


with open("input.txt", "r") as f:
    seed = list(f.readline().strip())
    f.readline()
    
    rules = {h:t for h,t in (line.strip().split(" -> ") for line in f)}

    print(f"Part 1: { part1(seed, rules, 10)}")
    print(f"Part 2: { part2(seed, rules, 40)}")
