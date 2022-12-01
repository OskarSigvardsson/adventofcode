import re
import sys

def debug(coords):
    mx,my = 0,0

    for x,y in coords:
        mx,my = max(x, mx), max(y, my)

    for y in range(my + 1):
        for x in range(mx + 1):
            if (x,y) in coords:
                sys.stdout.write("#")
            else:
                sys.stdout.write(" ")
        print()
        

def fold(coords, axis, pos):
    folded = set()

    for x,y in coords:
        if axis == 'x' and x < pos:
            folded.add((x,y))
        elif axis == 'y' and y < pos:
            folded.add((x,y))
        elif axis == 'x':
            folded.add((pos - (x - pos), y))
        elif axis == 'y':
            folded.add((x, pos - (y - pos)))

    return folded
    
def part1(coords, folds):
    return len(fold(coords, *folds[0]))

def part2(coords, folds):
    for axis, pos in folds:
        coords = fold(coords, axis, pos)

    print("Part 2:")
    debug(coords)
    

with open("input.txt", "r") as f:
    coords = set()
    folds = []

    for line in f:
        if m := re.match(R"(\d+),(\d+)", line):
            coords.add((int(m.group(1)), int(m.group(2))))

        if m := re.match(R"fold along (.)=(\d+)", line):
            folds.append((m.group(1), int(m.group(2))))

    print(f"Part 1: { part1(set(coords), folds) }")
    part2(coords, folds)
