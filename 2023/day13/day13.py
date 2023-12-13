def find_mirror(rows, but_not = None):
    for i in range(1,len(rows)):
        if i == but_not:
            continue
        
        mirror = True

        for o in range(len(rows)):
            if i - o < 0 or i + o - 1 >= len(rows):
                break

            if rows[i-o] != rows[i+o-1]:
                mirror = False
                break

        if mirror:
            return i

    return None

def smudge_test(rows):
    ref = find_mirror(rows)
    
    def flip(i, j):
        assert(rows[i][j] in ".#")
        
        rows[i][j] = "." if rows[i][j] == "#" else "#"

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            flip(i, j)
            n = find_mirror(rows, but_not = ref)
            flip(i, j)

            if n is not None and n != ref:
                return n
           
    return None

def transpose(rows):
    return list(list(t) for t in zip(*rows))

with open("../inputs/day13-real.txt", "r") as f:
    maps = []
    curr = []

    for line in f:
        line = line.strip()

        if line == "":
            maps.append(curr)
            curr = []
        else:
            curr.append(list(line))

    if len(curr) > 0:
        maps.append(curr)


    part1 = sum(100*n for n in (find_mirror(m) for m in maps) if n is not None)
    part1 += sum(n for n in (find_mirror(transpose(m)) for m in maps) if n is not None)
    
    print(f"Part 1: {part1}")

    part2 = sum(100*n for n in (smudge_test(m) for m in maps) if n is not None)
    part2 += sum(n for n in (smudge_test(transpose(m)) for m in maps) if n is not None)
    
    print(f"Part 2: {part2}")
