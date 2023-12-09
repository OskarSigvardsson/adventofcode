from itertools import pairwise
    
def interpolate(seq):
    if all(n == 0 for n in seq):
        return 0

    return seq[-1] + interpolate([b - a for a,b in pairwise(seq)])

def interpolate_rev(seq):
    if all(n == 0 for n in seq):
        return 0

    return seq[0] - interpolate_rev([b - a for a,b in pairwise(seq)])
    

    
with open("../inputs/day09-real.txt", "r") as f:
    seqs = [[int(n.strip()) for n in line.strip().split(" ")] for line in f]

    s = sum(interpolate(seq) for seq in seqs)
    print(f"Part 1: {s}");

    s = sum(interpolate_rev(seq) for seq in seqs)

    print(f"Part 2: {s}");
