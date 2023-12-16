m = []

with open("../inputs/day16-real.txt", "r") as f:
    m = [line.strip() for line in f]
                    
w = len(m[0])
h = len(m)

up    = ( 0,-1)
down  = ( 0, 1)
left  = (-1, 0)
right = ( 1, 0)

dir_change = {
    ("/", up):    [right],
    ("/", down):  [left],
    ("/", left):  [down],
    ("/", right): [up],

    ("\\", up):    [left],
    ("\\", down):  [right],
    ("\\", left):  [up],
    ("\\", right): [down],

    ("-", up):    [left, right],
    ("-", down):  [left, right],
    ("-", left):  [left],
    ("-", right): [right],

    ("|", up):    [up],
    ("|", down):  [down],
    ("|", left):  [up, down],
    ("|", right): [up, down],

    (".", up):    [up],
    (".", down):  [down],
    (".", left):  [left],
    (".", right): [right],
}

def solve(p,d):
    stack = [(p,d)]
    visited = set()
    energized = set()
    

    while len(stack) > 0:
        p,d = stack.pop()
        x,y = p

        if x not in range(w) or y not in range(h):
            continue
        
        if (p,d) in visited:
            continue

        energized.add(p)
        visited.add((p,d))

        if x not in range(w) or y not in range(h):
            continue
        
        for d2 in dir_change[(m[y][x],d)]:
            dx,dy = d2
            stack.append(((x+dx,y+dy),d2))

    return len(energized)
   
    

part1 = solve((0,0),right)
print(f"Part 1: {part1}")

s1 = max(solve((x,0), down) for x in range(w))
s2 = max(solve((x,h-1), up) for x in range(w))
s3 = max(solve((0,y), right) for y in range(h))
s4 = max(solve((w-1,y), left) for y in range(h))

part2 = max([s1,s2,s3,s4])

print(f"Part 2: {part2}")
