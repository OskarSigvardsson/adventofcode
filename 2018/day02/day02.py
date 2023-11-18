from collections import Counter
from itertools import combinations

def differ(s1,s2):
    return sum(1 for c1,c2 in zip(s1,s2) if c1 != c2)

def common(s1,s2):
    return "".join(c1 for c1,c2 in zip(s1,s2) if c1 == c2)

with open("input.txt") as f:
    counts = [set(Counter(line).values()) for line in f]

    twos = sum(1 for s in counts if 2 in s)
    threes = sum(1 for s in counts if 3 in s)

    print(twos * threes)

with open("input.txt") as f:
    ids = [line.strip() for line in f]

    for s1,s2 in combinations(ids, 2):
        if differ(s1,s2) == 1:
            print(common(s1,s2))
            
