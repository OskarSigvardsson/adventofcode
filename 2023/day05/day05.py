import re

def apply_map(n, m):
    for src,dst,count in m:
        if dst <= n < dst + count:
            return src + (n - dst)

    return n

def map_range(r, m):
    result = []
    rb,rc = r

    for src,dst,count in m:
        if rc <= 0: break
            
        if rb < src and rb + rc > src+count:
            result.append((rb, src - rb))
            rb = src
            rc -= src - rb

        if rc <= 0: break

        if rb >= src and rb < src + count:


    

with open("../inputs/day05-real.txt") as f:
    seeds = []
    maps = []

    for l in f:
        if l.strip() == "":
            break
        
        seeds.extend(int(n) for n in re.findall("\d+", l))


    cm = []
    for l in f:
        if l.strip() == "":
            maps.append(sorted(cm))
            cm = []
        
        if m := re.match("(\d+) (\d+) (\d+)", l):
            cm.append(tuple(int(n) for n in m.groups()))
            
    maps.append(cm)

    mapped = []
    for seed in seeds:
        n = seed
        for m in maps:
            n = apply_map(n, m)

        mapped.append(n)

    print("Part 1:", min(mapped))

    ranges = [(start,count) for start,count in zip(seeds[::2], seeds[1::2])]

    for start,count in zip(seeds[::2], seeds[1::2]):
        n = start

        
