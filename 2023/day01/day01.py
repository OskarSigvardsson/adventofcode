import re

with open("input.txt") as f:
    numbers = [[int(c) for c in line if c in "0123456789"] for line in f]
    print("Part 1: {}".format(sum(10*ns[0] + ns[-1] for ns in numbers)))

with open("input.txt") as f:
    r = R"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))"
    v = { d: int(d) for d in "0123456789" }
    v['one']   = 1
    v['two']   = 2
    v['three'] = 3
    v['four']  = 4
    v['five']  = 5
    v['six']   = 6
    v['seven'] = 7
    v['eight'] = 8
    v['nine']  = 9

    numbers = [[v[s] for s in re.findall(r, line)] for line in f]
    print("Part 2: {}".format(sum(10*ns[0] + ns[-1] for ns in numbers)))
