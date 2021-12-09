from math import prod

def part1(m, w, h):
    def lowpoint(x,y):
        return ((y + 1 >= h or m[y][x] < m[y+1][x])
            and (x + 1 >= w or m[y][x] < m[y][x+1])
            and (y - 1 <  0 or m[y][x] < m[y-1][x])
            and (x - 1 <  0 or m[y][x] < m[y][x-1]))
            
    return sum(m[y][x]+1 for x in range(w) for y in range(h) if lowpoint(x,y))

def part2(m, w, h):
    stack = []

    def floodfill(x, y):
        count = 0
        stack.clear()
        stack.append((x,y))

        while len(stack) > 0:
            x,y = stack.pop()

            if x < 0 or y < 0 or x >= w or y >= h:
                continue

            if m[y][x] == 9:
                continue

            m[y][x] = 9
            count += 1

            stack.append((x, y + 1))
            stack.append((x, y - 1))
            stack.append((x + 1, y))
            stack.append((x - 1, y))
    
        return count
    
    basins = []

    for (x,y) in ((x,y) for x in range(w) for y in range(h)):
        basins.append(floodfill(x,y))
    
    return prod(sorted(basins)[-3:])

with open("input.txt", "r") as f:
    m = [[int(c) for c in line.strip()] for line in f]

    w = len(m[0])
    h = len(m)

    print(f"Part 1: { part1(m, w, h) }")
    print(f"Part 2: { part2(m, w, h) }")
