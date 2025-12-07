from itertools import product
from copy import deepcopy

grid = []
instructions = []
readingGrid = True

for line in open("../inputs/day15-real.txt"):
    line = line.strip()
    if line == "":
        readingGrid = False
    elif readingGrid:
        grid.append(list(line))
    else:
        instructions.extend(line)

dirs = { '>': ( 1, 0), 'v': ( 0, 1), '<': (-1, 0), '^': ( 0,-1), }

def part1(grid):
    grid = deepcopy(grid)
    w = len(grid[0])
    h = len(grid)

    sx,sy = None,None

    for x,y in product(range(w), range(h)):
        if grid[y][x] == "@":
            sx,sy = x,y
            break

    def move(x,y,dx,dy):
        match grid[y][x]:
            case "#" | "." : return
            case "@" | "O":
                move(x+dx,y+dy,dx,dy)
                if grid[y+dy][x+dx] == ".":
                    grid[y][x],grid[y+dy][x+dx] = grid[y+dy][x+dx],grid[y][x]

    x,y = sx,sy
    for dx,dy in (dirs[inst] for inst in instructions):
        move(x,y,dx,dy)
        if grid[y][x] != "@":
            x,y = x+dx,y+dy

    return sum(100*y+x for x,y in product(range(w),range(h)) if grid[y][x] == "O")


def part2(inputGrid):
    inputGrid = deepcopy(inputGrid)
    grid = []
    repl = { "#": "##", ".": "..", "O": "[]", "@": "@." }

    for line in inputGrid:
        grid.append([])
        for c in line:
            grid[-1].extend(repl[c])

    w = len(grid[0])
    h = len(grid)

    sx,sy = None,None

    for x,y in product(range(w), range(h)):
        if grid[y][x] == "@":
            sx,sy = x,y
            break

    def can_push(x,y,dx,dy):
        match grid[y][x], (dx,dy):
            case "#", _: return False
            case ".", _: return True
            case "@", _: return can_push(x+dx,y+dy,dx,dy)

            case "[", (1,0): return can_push(x+2,y,dx,dy)
            case "]", (-1,0): return can_push(x-2,y,dx,dy)

            case "[", (0,-1): return can_push(x,y-1,dx,dy) and can_push(x+1,y-1,dx,dy)
            case "]", (0,-1): return can_push(x-1,y-1,dx,dy) and can_push(x,y-1,dx,dy)

            case "[", (0,1): return can_push(x,y+1,dx,dy) and can_push(x+1,y+1,dx,dy)
            case "]", (0,1): return can_push(x-1,y+1,dx,dy) and can_push(x,y+1,dx,dy)

            case c,d: print(c,d); assert(False)

    def swap(x1,y1,x2,y2):
        grid[y1][x1],grid[y2][x2] = grid[y2][x2],grid[y1][x1]

    def push(x,y,dx,dy):
        match grid[y][x], (dx,dy):
            case "#", _: assert(False)
            case ".", _: return
            case "@", _: push(x+dx,y+dy,dx,dy)

            case "[",( 1, 0): push(x+2,y  ,dx,dy); swap(x+1,y  ,x+2,y)
            case "]",(-1, 0): push(x-2,y  ,dx,dy); swap(x-1,y  ,x-2,y)

            case "[",( 0,-1): push(x  ,y-1,dx,dy); push(x+1,y-1,dx,dy); swap(x+1,y,x+1,y-1)
            case "]",( 0,-1): push(x-1,y-1,dx,dy); push(x  ,y-1,dx,dy); swap(x-1,y,x-1,y-1)

            case "[",( 0, 1): push(x,  y+1,dx,dy); push(x+1,y+1,dx,dy); swap(x+1,y,x+1,y+1)
            case "]",( 0, 1): push(x-1,y+1,dx,dy); push(x  ,y+1,dx,dy); swap(x-1,y,x-1,y+1)

        swap(x,y,x+dx,y+dy)

    def debug():
        for line in grid:
            print("".join(line))
    x,y = sx,sy
    for dx,dy in (dirs[inst] for inst in instructions):
        if can_push(x,y,dx,dy):
            push(x,y,dx,dy)
            x,y = x+dx,y+dy
        debug()
        input()

    return sum(y*100 + x for x,y in product(range(w),range(h)) if grid[y][x] == '[')

print(f"Part 1: {part1(grid)}")
print(f"Part 2: {part2(grid)}")