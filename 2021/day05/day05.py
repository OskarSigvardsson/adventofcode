import re
from collections import Counter

def debug(c):
    """Debug function, prints the grid. Not used in final solution"""
    grid = [['.' for _ in range(10)] for _ in range(10)]

    for coord,value in c.items():
        x,y = coord
        grid[y][x] = str(value)

    for line in grid:
        print("".join(line))
    
def part1(coords):
    c = Counter()
    
    for x1,y1,x2,y2 in coords:
        if x1 == x2:
            c.update((x1,y) for y in range(min(y1,y2), max(y1,y2)+1))

        if y1 == y2:
            c.update((x,y1) for x in range(min(x1,x2), max(x1,x2)+1))

    return len([coord for coord,count in c.items() if count >= 2])
    
def part2(coords):
    c = Counter()
    
    def sgn(x):
        """Sign helper, returns -1, 0 or 1 depending x's sign"""
        return 0 if x == 0 else int(x/abs(x))
    
    for x1,y1,x2,y2 in coords:
        tx,ty = x2 - x1, y2 - y1  # <- total change
        d = max(abs(tx),abs(ty))  # <- number of "steps" in the line, zero-based
        dx,dy = sgn(tx), sgn(ty)  # <- change per step

        c.update((x,y) for x,y in ((x1 + dx*i,y1 + dy*i) for i in range(d+1)))

    return len([coord for coord,count in c.items() if count >= 2])

    
with open("input.txt") as f:
    r = re.compile(R"(\d+),(\d+) -> (\d+),(\d+)")
    coords = [tuple(int(s) for s in r.match(line).groups()) for line in f]

    print(f"Part 1: { part1(coords) }")
    print(f"Part 2: { part2(coords) }")
