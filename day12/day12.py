from collections import defaultdict

def part1(m):
    def path(prev):
        if prev[-1] == "end":
            return 1
        else:
            s = 0

            for nxt in m[prev[-1]]:
                if nxt[0] == nxt[0].lower() and nxt in prev:
                    continue

                prev.append(nxt)
                s += path(prev)
                prev.pop()

            return s
            
    return path(["start"])

def part2(m):
    def path(prev, no_revisit):
        if prev[-1] == "end":
            return 1
        else:
            s = 0

            for nxt in m[prev[-1]]:
                if nxt == "start":
                    continue

                is_small = nxt[0] == nxt[0].lower()
                is_revisit = is_small and nxt in prev
                
                if no_revisit and is_revisit:
                    continue

                prev.append(nxt)
                s += path(prev, no_revisit or is_revisit)
                prev.pop()

            return s
            
    return path(["start"], False)

with open("input.txt", "r") as f:
    m = defaultdict(list)

    for line in f:
        a,b = line.strip().split("-")
        m[a].append(b)
        m[b].append(a)

    print(f"Part 1: { part1(m) }")
    print(f"Part 2: { part2(m) }")
