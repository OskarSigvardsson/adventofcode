import re

from collections import defaultdict

wires = []

with open("input.txt", "r") as f:
    for line in f:
        wires.append([(g[0], int(g[1])) for g in re.findall(r"([RLUD])(\d+)", line)])


board = defaultdict(int)
dirs = {
    'R': (1,0),
    'L': (-1,0),
    'U': (0,1),
    'D': (0,-1),
}
steps = [{},{}]
inters = set()

for wi,wire in enumerate(wires):
    pos = (0,0)
    step = 0
    for (d,l) in wire:
        for i in range(l):
            step += 1
            pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
            board[pos] = board[pos] | (1 << wi)

            steps[wi][pos] = step

            if board[pos] == 3:
                inters.add(pos)

print(min(steps[0][p] + steps[1][p] for p in inters))
