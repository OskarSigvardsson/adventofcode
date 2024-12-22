from collections import defaultdict

ns = [int(line) for line in open("../inputs/day22-real.txt")]

def gen(sn):
    sn = ((sn * 64) ^ sn) % 16777216
    sn = ((sn // 32) ^ sn) % 16777216
    sn = ((sn * 2048) ^ sn) % 16777216
    return sn

def seq(n):
    for _ in range(2001):
        yield n % 10
        n = gen(n)

def fivewise(iterable):
    it = iter(iterable)
    a,b,c,d,e = next(it), next(it), next(it), next(it), next(it)
    yield (a,b,c,d,e)

    for i in it:
        a,b,c,d,e = b,c,d,e,i
        yield (a,b,c,d,e)

def diffs(n):
    seen = set()
    for a,b,c,d,e in fivewise(seq(n)):
        t = (b-a,c-b,d-c,e-d)
        if t in seen: continue
        seen.add(t)
        yield t, e

def part1(ns):
    p1 = 0
    for n in ns:
        for _ in range(2000):
            n = gen(n)
        p1 += n
    return p1

def part2(ns):
    score = defaultdict(int)

    for n in ns:
        for d,v in diffs(n):
            score[d] += v

    return max(score.values())

print(f"Part 1: {part1(ns)}")
print(f"Part 2: {part2(ns)}")
