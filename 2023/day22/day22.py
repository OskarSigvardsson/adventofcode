import re

from itertools import product

# settles a single block. checks if there's anything underneath and moves it down if not
# NOTE: this mutably updates both block and filled. very terrible, but faster than copying, i suppose
def settle_block(block, filled):
    x1,y1,z1,x2,y2,z2 = block

    maxdrop = z1

    assert(x1 <= x2)
    assert(y1 <= y2)
    assert(z1 <= z2)
    
    for x,y in product(range(x1,x2+1),range(y1,y2+1)):
        drop = 0

        for d in range(1,z1):
            if (x,y,z1-d) in filled:
                break

            drop = d

        maxdrop = min(maxdrop,drop)

    if maxdrop > 0:
        for bx,by,bz in product(range(x1,x2+1),range(y1,y2+1),range(z1,z2+1)):
            #assert((bx,by,bz) in filled)
            filled.remove((bx,by,bz))

        for bx,by,bz in product(range(x1,x2+1),range(y1,y2+1),range(z1-maxdrop,z2+1-maxdrop)):
            #assert((bx,by,bz) not in filled)
            filled.add((bx,by,bz))

        block[:] = [x1,y1,z1-maxdrop,x2,y2,z2-maxdrop]
        
    return maxdrop > 0

# zaps a single block and then settles the rest. returns the list of blocks that settled as a result
# does not mutate its input, copies it instead. so slow-ish. 
def zap_check(zap, blocks, filled):
    blocks = [block[:] for block in blocks]
    filled = set(filled)
    x1,y1,z1,x2,y2,z2 = blocks[zap]

    for bx,by,bz in product(range(x1,x2+1),range(y1,y2+1),range(z1,z2+1)):
        #assert((bx,by,bz) in filled)
        filled.remove((bx,by,bz))

    fell = set()
    
    while True:
        stable = True

        for i,block in enumerate(blocks):
            if i == zap: continue

            settled = settle_block(block, filled)

            if settled:
                stable = False
                fell.add(i)

        if stable:
            break

    return fell
    
with open("../inputs/day22-real.txt", "r") as f:
    matches = (re.match(R"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line) for line in f)
    blocks = [[int(n) for n in mtch.groups()] for mtch in matches]

    filled = set()
    
    for block in blocks:
        x1,y1,z1,x2,y2,z2 = block

        for bx,by,bz in product(range(x1,x2+1),range(y1,y2+1),range(z1,z2+1)):
            # assert((bx,by,bz) not in filled)
            filled.add((bx,by,bz))

    while True:
        stable = True

        for block in blocks:
            stable &= not settle_block(block, filled)

        if stable: break

    part1 = 0
    part2 = 0

    for zap in range(len(blocks)):
        fell = zap_check(zap, blocks, filled)

        if len(fell) == 0:
            part1 += 1 
        part2 += len(fell)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
