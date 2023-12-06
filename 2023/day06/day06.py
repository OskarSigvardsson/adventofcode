import re

with open("../inputs/day06-real.txt", "r") as f:
    lines = f.readlines()
    times = [int(n) for n in re.findall("\d+", lines[0])]
    dists = [int(n) for n in re.findall("\d+", lines[1])]
    races = list(zip(times,dists))

    res = 1
    
    for t,d in races:
        res *= sum(1 for x in (h * (t - h) for h in range(t+1)) if x > d)

    print(f"Part 1: {res}")

    t = int("".join(str(n) for n in times))
    d = int("".join(str(n) for n in dists))

    res = sum(1 for x in (h * (t - h) for h in range(t+1)) if x > d)
    
    print(f"Part 2: {res}")
