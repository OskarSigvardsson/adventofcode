import re

def hash(s):
    v = 0

    for c in s:
        v = (17 * (v + ord(c))) % 256

    return v

with open("../inputs/day15-real.txt", "r") as f:
    entries = f.readline().strip().split(",")

    print(sum(hash(s) for s in entries))

    insts = [re.match(R"(\w+)(=|-)(\d*)", entry).groups() for entry in entries]

    boxes = [[] for _ in range(256)]

    for (label,op,fl) in insts:
        box = hash(label)

        match (op,fl):
            case ("-",''):
                boxes[box] = [(label2,fl2) for (label2,fl2) in boxes[box] if label2 != label]
            case ("=", fl):
                fl = int(fl)
                boxes[box] = [(label,fl) if label == label2 else (label2,fl2) for (label2,fl2) in boxes[box]]

                if (label,fl) not in boxes[box]:
                    boxes[box].append((label,fl))

    focus = 0
    for i,box in enumerate(boxes):
        for j,lens in enumerate(box):
            _,fl = lens

            focus += (i + 1) * (j + 1) * fl

    print(focus)
