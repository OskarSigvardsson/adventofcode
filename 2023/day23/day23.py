import sys

sys.setrecursionlimit(10000)

m = []

with open("../inputs/day23-real.txt", "r") as f:
    m = [line.strip() for line in f]

w,h = len(m[0]),len(m)

memo = {}
seen = set()
def longest_path(p, coming_from = None, indent = 0):
    x,y = p

    if x not in range(w) or y not in range(h):
        return 0

    if m[y][x] == "#":
        return 0

    
    if y == h-1 and x == w-2:
        return 0
    

    if p in memo:
        return memo[p]


    dirs = [(0,-1),(0,1),(-1,0),(1,0)]
    mx = 0
    for (dx,dy) in dirs:
        cx,cy = x+dx,y+dy

        match (m[cy][cx], (dx,dy)):
            case _ if (cx,cy) == coming_from: continue
            case _ if cx not in range(w): continue
            case _ if cy not in range(h): continue

            case ("v",(0,-1)): continue
            case ("^",(0,1)): continue
            case (">",(-1,0)): continue
            case ("<",(1,0)): continue

            case _:
                mx = max(mx, longest_path((cx,cy), p, indent+1))

    memo[p] = 1 + mx

    return 1 + mx
        

def debug2(path):
    print(len(path))
    for y,row in enumerate(m):
        for x,c in enumerate(row):
            if (x,y) in path:
                print("O", end='')
            else:
                print(m[y][x], end='')
    
        print()
    print()

def longest_path2(p, curr_path):
    x,y = p
    
    if y == h-1 and x == w-2:
        return len(curr_path) - 1

    dirs = [(0,-1),(0,1),(-1,0),(1,0)]
    mx = 0
    for (dx,dy) in dirs:
        cx,cy = x+dx,y+dy

        if cx not in range(w) or cy not in range(h):
            continue

        if m[cy][cx] == "#":
            continue
        if (cx,cy) in curr_path:
            continue

        curr_path.add((cx,cy))
        mx = max(mx, longest_path2((cx,cy),curr_path))
        curr_path.remove((cx,cy))
    
    return mx
    
def debug(x,y,x2,y2):
    y -= 1
    print(m[y][x], longest_path((x,y),(x2,y2)))
          
debug(1,1,1,0)
print(longest_path2((1,0),set([(1,0)])))
