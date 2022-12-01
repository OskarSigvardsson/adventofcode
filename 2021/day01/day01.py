
# part 1
with open("input.txt", "r") as f:
    lines = f.readlines()
    print(sum(1 if int(a) < int(b) else 0 for a,b in zip(lines, lines[1:])))


# part 2
with open("input.txt", "r") as f:
    lines = [int(l) for l in f.readlines()]
    w1 = zip(lines[0:], lines[1:], lines[2:])
    w2 = zip(lines[1:], lines[2:], lines[3:])
    print(sum(1 if sum(a) < sum(b) else 0 for a,b in zip(w1,w2)))
